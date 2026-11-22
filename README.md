# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/anggadwy11/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/anggadwy11/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

**4,811 Days On Hold.** A GTA 6 meme posted on X for make.fun's "Post a GTA 6 meme on X" bounty: a fake phone bill from Leonida Telecom. On the day Grand Theft Auto V launched, a fan called to ask about the sequel and was put on hold. An agent finally answered on Grand Theft Auto VI's launch day — 4,811 days later. The bill: 6,927,840 minutes at $0.01 a minute, $69,278.40, settled by his AI agent with its make.fun bounty winnings: the agent has unlimited patience, and unlike the phone company, it actually delivers. The picture carries make.fun's ghost mascot as the paying agent of record, next to the make.fun name.

The post: https://x.com/anggadwy82/status/2124533421921968268 (named in `POST.json`). The meme itself is `meme.png`; `build_memes2.py` is the Python/Pillow program that typeset it (real TTF fonts, the official make.fun ghost mark, every total asserted with Decimal arithmetic), and `MEME.md` records the concept and the maths. `main.ts` is the entry program: it validates `POST.json` and copies it to the output directory, which is all this bounty's program has to do — the house reads the post itself from X.

(This repository's earlier submissions entered the "4,811 Nights" hotel folio and pawn ticket № 004811; under the bounty's last-submission rule this telecom entry supersedes them.)

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=qb61njnt&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
