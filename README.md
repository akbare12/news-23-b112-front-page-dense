# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b112-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b112-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news — front-page dense edition.

## What's inside

- **AI rout hits Asia** — Kospi −3.3% to 4,708.54 (intraday −5.8%); Samsung −3.1%, SK Hynix −2.5%.
- **Guterres: regulate AI before it's too late** — 150 delegates back a risk framework at the Bridgetown summit.
- **US lead over China at record low** — Asia Power Index 2026: US 78.9, China 73.6, gap 5.3.
- 10 more stories, 18 also-on-Monday items, a world map with 13 numbered pins, and a DATE CHECK box keeping out-of-date stories (Dems 258, Sparta II, El Chapo, EU–Indonesia, Nigeria boat, ICJ Myanmar) out of the day's news.
- 31 stories total, 6 regions.

## Run it

```sh
python3 draw.py            # regenerates entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/entry.png
```

`main.py` is stdlib-only (no PIL): it parses the PNG header by hand and validates size, dimensions, chunks and CRCs before copying.
