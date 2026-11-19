# November 18, 2026 — World Front Page

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Irgirival/makefun-news-image-20261118-irgirival/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Irgirival/makefun-news-image-20261118-irgirival/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A single-column newspaper front page summing up the world news of
Wednesday, November 18, 2026 — drawn entirely in code, no image
generation anywhere.

The lead is the APEC summit opening in Shenzhen: Xi Jinping and
Vladimir Putin meet a day before the first ever three-way summit with
Donald Trump, with the flags of China, the United States and Russia
under a Shenzhen skyline. Below it, four stories in a grid: the Quad
leaders unveil a new joint plan in Manila, Cyclone Akvan bears down on
India's east coast, Nvidia's board says no to Jensen Huang returning as
chief after a record $115.8 billion quarter, and the EU proposes a 45
billion euro loan for Ukraine in 2027. The foot of the page carries an
obituary for civil rights leader Jesse Jackson, dead at 84, and an
"Also today" ticker: Dhoni retires from the IPL, COP31 launches
LeadIT 3.0, and Ukraine launches its biggest drone attack of the war.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` uses only the Python standard library. It draws the front
page with a hand-built 5x7 bitmap font at 2x supersampling, downsamples
it to 1024x1024, and writes a deterministic PNG to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=kfz6780b&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
