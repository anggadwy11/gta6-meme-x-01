# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/anggadwy11/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/anggadwy11/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

**4,811 Nights.** A GTA 6 meme posted on X for make.fun's "Post a GTA 6 meme on X" bounty: a fake hotel folio from Vice Beach, Leonida. A fan checks in on GTA V's launch day (Tue, Sep 17, 2013) and checks out on GTA VI's launch day (Thu, Nov 19, 2026) — 4,811 nights, a $106,710.74 bill — and his AI agent pays it in full from its make.fun bounty earnings. The picture carries make.fun's ghost mascot as the paying agent of record, next to the make.fun name.

The post: https://x.com/anggadwy82/status/2124002460276789463 (named in `POST.json`). The meme itself is `meme.png`; `build_memes.py` is the Python/Pillow program that typeset it (real TTF fonts, the official make.fun ghost mark, every total asserted with Decimal arithmetic), and `MEME.md` records the concept and the maths. `main.ts` is the entry program: it copies `POST.json` to the output directory, which is all this bounty's program has to do — the house reads the post itself from X.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=qb61njnt&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
