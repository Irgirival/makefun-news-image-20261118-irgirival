#!/usr/bin/env python3
"""WORLD FRONT PAGE -- the world news of Wednesday, November 18, 2026.

A one-page newspaper front page drawn entirely in code with the Python
standard library only. Renders at 2x supersampling, downsamples to
1024x1024, and writes a deterministic PNG to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png).

Stories (all reported Wednesday, November 18, 2026):
  LEAD  APEC summit opens in Shenzhen; Xi and Putin meet, Trump flies in
        for the first three-way summit of the US, China and Russia.
  QUAD  Quad leaders unveil a new joint plan in Manila.
  STORM Cyclone Akvan bears down on India's east coast.
  CHIPS Nvidia's board rejects Jensen Huang's return as CEO after a
        record $115.8 billion quarter.
  EUROPE The EU proposes a 45 billion euro loan for Ukraine in 2027.
  OBIT  US civil rights leader Jesse Jackson dies at 84.
  TICKER Dhoni retires from the IPL; COP31 launches LeadIT 3.0;
        Ukraine launches its biggest drone attack of the war.
"""

import os
import struct
import zlib

S = 2                      # supersampling factor
W, H = 1024 * S, 1024 * S  # working canvas, downsampled to 1024x1024

PAPER = (246, 241, 230)
INK = (20, 20, 20)
NAVY = (16, 36, 62)
CRIMSON = (166, 25, 46)
GOLD = (201, 151, 28)
TEAL = (14, 107, 107)
GREY = (90, 88, 80)
LIGHT = (255, 255, 255)
CREAM = (250, 247, 238)
RULE = (180, 172, 150)

# ---------------------------------------------------------------- font
# Hand-built 5x7 bitmap font, '#' = ink. Uppercase + digits + punctuation.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '*': ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
}

CHAR_W, CHAR_H = 5, 7


def text_width(text, scale):
    """Pixel width of text at the given integer scale (working canvas px)."""
    return len(text) * (CHAR_W + 1) * scale - scale


def wrap(text, scale, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(w * h * 3)
        self.fill(bg)

    def fill(self, color):
        r, g, b = color
        self.buf[0::3] = bytes([r]) * (self.w * self.h)
        self.buf[1::3] = bytes([g]) * (self.w * self.h)
        self.buf[2::3] = bytes([b]) * (self.w * self.h)

    def px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = color

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        r, g, b = color
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            n = x1 - x0
            self.buf[base:base + n * 3:3] = bytes([r]) * n
            self.buf[base + 1:base + n * 3 + 1:3] = bytes([g]) * n
            self.buf[base + 2:base + n * 3 + 2:3] = bytes([b]) * n

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def circle(self, cx, cy, r, color):
        # Filled disc via horizontal spans (midpoint rows).
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, color, thick=2):
        for k in range(thick):
            rr = r - k
            for a in range(360):
                import math
                x = int(cx + rr * math.cos(math.radians(a)))
                y = int(cy + rr * math.sin(math.radians(a)))
                self.px(x, y, color)

    def text(self, x, y, s, scale, color):
        """Draw uppercase text; unknown chars render as space."""
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for row in range(CHAR_H):
                bits = glyph[row]
                for col in range(CHAR_W):
                    if bits[col] == '1':
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += (CHAR_W + 1) * scale
        return cx

    def text_center(self, cx, y, s, scale, color):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, color)

    def downsample(self):
        """Box-average S x S blocks -> 1024x1024 RGB bytes."""
        ow, oh = self.w // S, self.h // S
        out = bytearray(ow * oh * 3)
        for oy in range(oh):
            for ox in range(ow):
                acc = [0, 0, 0]
                for dy in range(S):
                    for dx in range(S):
                        i = ((oy * S + dy) * self.w + ox * S + dx) * 3
                        acc[0] += self.buf[i]
                        acc[1] += self.buf[i + 1]
                        acc[2] += self.buf[i + 2]
                o = (oy * ow + ox) * 3
                n = S * S
                out[o] = acc[0] // n
                out[o + 1] = acc[1] // n
                out[o + 2] = acc[2] // n
        return bytes(out), ow, oh


def write_png(path, rgb, w, h):
    """Deterministic PNG: filter 0, zlib level 9, no ancillary chunks."""
    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw.append(0)
        raw += rgb[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        return c + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ---------------------------------------------------------------- layout
# All coordinates are working-canvas pixels (2048 x 2048); the page is
# downsampled to 1024 x 1024 at the end. Margins and gutters in px.
MX = 56            # side margin
CW = W - 2 * MX    # content width


def skyline(cv, x, y, w, h, color):
    """A simple Shenzhen tower silhouette: rectangles of varied heights."""
    towers = [(0.00, 0.55), (0.07, 0.80), (0.14, 0.45), (0.21, 0.95),
              (0.29, 0.60), (0.36, 0.75), (0.44, 0.40), (0.51, 1.00),
              (0.59, 0.65), (0.66, 0.85), (0.74, 0.50), (0.81, 0.70),
              (0.88, 0.45), (0.95, 0.60)]
    tw = w // len(towers)
    for fx, fh in towers:
        th = int(h * fh)
        cv.rect(x + int(fx * w), y + h - th, tw - 4, th, color)
    # antenna on the tallest tower
    cv.vline(x + int(0.51 * w) + tw // 2 - 2, y - 14, 16, color, 3)


def flag_strip(cv, x, y, w, h):
    """Three flag bands for the summit: China, United States, Russia."""
    third = w // 3
    # China: red field, gold corner
    cv.rect(x, y, third - 6, h, (222, 41, 16))
    cv.rect(x + 8, y + 8, 26, 26, GOLD)
    # United States: red/white stripes with blue canton
    ux = x + third
    for i in range(7):
        cv.rect(ux, y + i * (h // 7), third - 6, h // 7 + 1,
                (178, 34, 52) if i % 2 == 0 else LIGHT)
    cv.rect(ux, y, (third - 6) * 2 // 5, h * 3 // 7, (60, 59, 110))
    # Russia: white / blue / red horizontal bands
    rx = x + 2 * third
    cv.rect(rx, y, third - 6, h // 3, LIGHT)
    cv.rect(rx, y + h // 3, third - 6, h // 3, (0, 57, 166))
    cv.rect(rx, y + 2 * h // 3, third - 6, h - 2 * (h // 3), (213, 0, 50))
    labels = [("CHINA", x), ("UNITED STATES", ux), ("RUSSIA", rx)]
    for name, fx in labels:
        cv.text(fx + 4, y + h + 10, name, 2, INK)
    # outline so the white band of the Russian flag stays visible
    cv.rect(x, y, w - 6, 2, INK)
    cv.rect(x, y + h - 2, w - 6, 2, INK)
    cv.rect(x, y, 2, h, INK)
    cv.rect(x + w - 8, y, 2, h, INK)


def panel(cv, x, y, w, h, kicker, kcolor, headline, body, icon):
    """One grid story panel: kicker bar, headline, body, small icon."""
    cv.rect(x, y, w, h, CREAM)
    cv.rect(x, y, w, 10, kcolor)
    cv.rect(x, y, 4, h, kcolor)
    cv.text(x + 24, y + 30, kicker, 3, kcolor)
    hy = y + 78
    for line in wrap(headline, 5, w - 48 - 170):
        cv.text(x + 24, hy, line, 5, INK)
        hy += 5 * 8 + 10
    by = hy + 14
    for line in wrap(body, 3, w - 48):
        cv.text(x + 24, by, line, 3, (60, 58, 50))
        by += 3 * 8 + 8
    icon(cv, x + w - 150, y + 34)


def icon_quad(cv, x, y):
    # Four dots linked in a diamond: the Quad.
    pts = [(x + 60, y), (x + 120, y + 60), (x + 60, y + 120), (x, y + 60)]
    for i in range(4):
        ax, ay = pts[i]
        bx, by = pts[(i + 1) % 4]
        steps = 60
        for t in range(steps + 1):
            cv.px(ax + (bx - ax) * t // steps, ay + (by - ay) * t // steps,
                  NAVY)
    for px_, py_ in pts:
        cv.circle(px_, py_, 14, NAVY)


def icon_storm(cv, x, y):
    # Cyclone spiral: concentric rings, offset centres.
    cv.ring(x + 60, y + 60, 58, TEAL, 6)
    cv.ring(x + 72, y + 60, 40, TEAL, 6)
    cv.ring(x + 60, y + 60, 22, TEAL, 6)
    cv.circle(x + 60, y + 60, 8, TEAL)


def icon_chip(cv, x, y):
    # A chip: square die, pins, inner square.
    cv.rect(x + 20, y + 20, 80, 80, INK)
    cv.rect(x + 40, y + 40, 40, 40, GOLD)
    for i in range(4):
        cv.rect(x + 28 + i * 20, y + 6, 8, 14, INK)
        cv.rect(x + 28 + i * 20, y + 100, 8, 14, INK)
        cv.rect(x + 6, y + 28 + i * 20, 14, 8, INK)
        cv.rect(x + 100, y + 28 + i * 20, 14, 8, INK)


def icon_euro(cv, x, y):
    # A coin: gold disc with a bold "45" and a euro-style bar.
    cv.circle(x + 60, y + 60, 58, GOLD)
    cv.circle(x + 60, y + 60, 46, (232, 196, 90))
    cv.text(x + 22, y + 30, "45", 6, NAVY)


def render():
    cv = Canvas(W, H, PAPER)

    # ---- masthead: navy band, title, gold rule, date line ----
    cv.rect(0, 0, W, 280, NAVY)
    cv.text_center(W // 2, 40, "WORLD FRONT PAGE", 9, LIGHT)
    cv.rect(MX, 180, CW, 6, GOLD)
    cv.text_center(W // 2, 208, "WEDNESDAY, NOVEMBER 18, 2026", 5, GOLD)
    cv.text(MX, 208, "ONE DAY", 4, (150, 170, 195))
    cv.text(W - MX - text_width("ONE PAGE", 4), 208, "ONE PAGE", 4,
            (150, 170, 195))

    # ---- lead story: APEC summit ----
    ly, lh = 304, 500
    cv.rect(MX, ly, CW, lh, LIGHT)
    cv.rect(MX, ly, 14, lh, CRIMSON)
    cv.rect(MX, ly, CW, 3, CRIMSON)
    cv.rect(MX, ly + lh - 3, CW, 3, CRIMSON)
    cv.text(MX + 40, ly + 34, "APEC SUMMIT OPENS - SHENZHEN, CHINA", 4,
            CRIMSON)
    hy = ly + 96
    for line in wrap("XI AND PUTIN MEET AS TRUMP FLIES IN FOR FIRST "
                     "THREE-WAY SUMMIT", 6, CW - 80):
        cv.text(MX + 40, hy, line, 6, INK)
        hy += 6 * 8 + 12
    by = hy + 22
    for line in wrap(
            "CHINA AND RUSSIA OPENED THE APEC SUMMIT IN SHENZHEN ON "
            "WEDNESDAY, A DAY BEFORE THE FIRST EVER TRILATERAL MEETING "
            "OF XI JINPING, VLADIMIR PUTIN AND DONALD TRUMP.",
            4, CW - 80):
        cv.text(MX + 40, by, line, 4, (60, 58, 50))
        by += 4 * 8 + 10
    gy = by + 26
    skyline(cv, MX + 40, gy, CW - 80, 44, (200, 192, 168))
    flag_strip(cv, MX + 40, gy + 52, CW - 80, 48)

    # ---- 2 x 2 grid of stories ----
    gy0 = ly + lh + 24
    gh = 370
    gw = (CW - 24) // 2
    panel(cv, MX, gy0, gw, gh, "QUAD - MANILA", NAVY,
          "QUAD LEADERS UNVEIL NEW JOINT PLAN",
          "DONALD TRUMP ARRIVED IN MANILA FOR QUAD TALKS BEFORE "
          "FLYING ON TO CHINA FOR THE APEC SUMMIT.",
          icon_quad)
    panel(cv, MX + gw + 24, gy0, gw, gh, "WEATHER - INDIA", TEAL,
          "CYCLONE AKVAN BEARS DOWN ON INDIA",
          "THE SEVERE STORM HEADS FOR THE EAST COAST, WITH "
          "EVACUATIONS UNDER WAY IN ODISHA.",
          icon_storm)
    panel(cv, MX, gy0 + gh + 24, gw, gh, "TECH - NVIDIA", INK,
          "NVIDIA BOARD SAYS NO TO HUANG RETURN",
          "THE BOARD REJECTED ITS FOUNDER RETURNING AS CHIEF AFTER "
          "A RECORD 115.8 BILLION DOLLAR QUARTER.",
          icon_chip)
    panel(cv, MX + gw + 24, gy0 + gh + 24, gw, gh, "EUROPE - UKRAINE",
          CRIMSON, "EU PROPOSES 45 BILLION EURO LOAN FOR UKRAINE",
          "URSULA VON DER LEYEN ANNOUNCED THE 2027 LOAN TO COVER "
          "AROUND TWO THIRDS OF KYIV FINANCING NEEDS.",
          icon_euro)

    # ---- bottom strip: obituary + ticker ----
    by0 = gy0 + 2 * gh + 24 + 24
    bh = 230
    bw = (CW - 24) // 2
    cv.rect(MX, by0, bw, bh, NAVY)
    cv.text(MX + 28, by0 + 28, "OBITUARY", 3, GOLD)
    cv.text(MX + 28, by0 + 76, "JESSE JACKSON", 5, LIGHT)
    cv.text(MX + 28, by0 + 128, "DIES AT 84", 5, LIGHT)
    oy = by0 + 182
    for line in wrap("CIVIL RIGHTS LEADER, DEAD AT 84.", 3, bw - 56):
        cv.text(MX + 28, oy, line, 3, (190, 200, 215))
        oy += 3 * 8 + 8
    # ticker panel beside it
    tx = MX + bw + 24
    cv.rect(tx, by0, bw, bh, CRIMSON)
    cv.text(tx + 28, by0 + 28, "ALSO TODAY", 3, GOLD)
    ty = by0 + 82
    for item in ("DHONI RETIRES FROM THE IPL",
                 "COP31: INDIA AND SWEDEN LAUNCH LEADIT 3.0",
                 "UKRAINE LAUNCHES ITS BIGGEST DRONE ATTACK"):
        cv.rect(tx + 28, ty + 6, 14, 14, GOLD)
        for line in wrap(item, 3, bw - 90):
            cv.text(tx + 56, ty, line, 3, LIGHT)
            ty += 3 * 8 + 8
        ty += 14

    # ---- footer ----
    fy = by0 + bh + 30
    cv.hline(MX, fy, CW, RULE, 3)
    cv.text_center(W // 2, fy + 20,
                   "ALL STORIES REPORTED WEDNESDAY, NOVEMBER 18, 2026",
                   3, GREY)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
    out = out_dir if out_dir.endswith(".png") else os.path.join(out_dir,
                                                                 "entry.png")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    cv = render()
    rgb, w, h = cv.downsample()
    n = write_png(out, rgb, w, h)
    print(f"wrote {out} {w}x{h} {n} bytes")


if __name__ == "__main__":
    main()
