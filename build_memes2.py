#!/usr/bin/env python3
"""Round-2 concepts for gta6-meme-x-01: telecom hold bill, storage lien
notice, gym statement. Reuses the document helpers from build_memes.py
(paper, stamps, ghost medallion payment box, Decimal-asserted money).
Canvas 1200x1500; judge view 480 wide. Dates: GTA V Tue 17 Sep 2013 ->
GTA VI Thu 19 Nov 2026 = 4,811 days; Oct 2013-Nov 2026 = 158 months.
"""
import sys
sys.path.insert(0, "/home/hatch/workspace/makefun/gta6-meme-x-01-finalists")
from decimal import Decimal as D
from PIL import Image, ImageDraw
import build_memes as bm

F, W, H = bm.F, bm.W, bm.H
INK, FAINT, MAGENTA = bm.INK, bm.FAINT, bm.MAGENTA
SERIF_B, SERIF_I = bm.SERIF_B, bm.SERIF_I
SANS_B, SANS = bm.SANS_B, bm.SANS
MONO, MONO_B = bm.MONO, bm.MONO_B
COND_B, COND = bm.COND_B, bm.COND
OUT = bm.OUT
M, R = 84, W - 84


def paybox(im, d, by, band_color, band_text, band_fg, body):
    d.rounded_rectangle([M, by, R, by + 276], radius=14, outline=INK, width=3)
    d.rectangle([M, by, R, by + 50], fill=band_color)
    bm.center_spaced(d, W / 2, by + 9, band_text, F(SANS_B, 27), band_fg, 4)
    bm.paste_mark(im, M + 100, by + 168, 156)
    yy = by + 70
    for ln in bm.wrap(d, body, F(SANS, 30), R - M - 240):
        d.text((M + 206, yy), ln, font=F(SANS, 30), fill=INK); yy += 38
    d.text((M + 206, by + 222), "make.fun", font=F(SANS_B, 42), fill=MAGENTA)


def footer(d, fy, seed, text):
    bm.barcode(d, M, fy, 300, 68, seed)
    for i, ln in enumerate(bm.wrap(d, text, F(COND, 24), 660)):
        d.text((M + 330, fy + 4 + i * 30), ln, font=F(COND, 24), fill=FAINT)


def hero_note(d, label, figure, note, unit=None):
    d.text((M, 536), label, font=F(COND_B, 30), fill=FAINT)
    d.text((M, 572), figure, font=F(SERIF_B, 118), fill=INK)
    if unit:
        fw = d.textlength(figure, font=F(SERIF_B, 118))
        d.text((M + fw + 22, 640), unit, font=F(COND_B, 44), fill=FAINT)
    yy = 548
    for ln in bm.wrap(d, note, F(SERIF_I, 31), 430):
        d.text((640, yy), ln, font=F(SERIF_I, 31), fill=(74, 62, 52)); yy += 40


def total_block(im, d, rows, total_label, total_str, stamp_args, y0=806):
    f = F(MONO, 30)
    y = y0
    for l, r in rows:
        bm.leader_row(d, M, R, y, l, r, f); y += 50
    bm.rule(d, M, R, y + 4, 2)
    d.text((M, y + 18), total_label, font=F(SANS_B, 42), fill=INK)
    t = total_str
    d.text((R - d.textlength(t, font=F(MONO_B, 56)), y + 10), t, font=F(MONO_B, 56), fill=INK)
    bm.stamp(im, *stamp_args)
    return y + 104


# ---------------------------------------------------------------- TELECOM
def telecom():
    mins = 4811 * 1440
    total = D(mins) * D("0.01")
    assert total == D("69278.40") and mins == 6927840, (total, mins)
    im = bm.paper((248, 250, 252), 44).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 150], fill=(11, 78, 162))
    bm.center_spaced(d, W / 2, 26, "LEONIDA TELECOM", F(SANS_B, 54), (255, 255, 255), 4)
    bm.center_spaced(d, W / 2, 96, "EST. 1998  •  WE ANSWER EVENTUALLY", F(COND_B, 27), (200, 220, 245), 5)
    bm.center_spaced(d, W / 2, 186, "STATEMENT OF ACCOUNT — CALL RECORD", F(SANS_B, 33), INK, 5)
    d.text((M, 238), "ACCOUNT LT-004811", font=F(MONO, 25), fill=FAINT)
    t = "ORIGINAL — CUSTOMER'S COPY"
    d.text((R - d.textlength(t, font=F(MONO, 25)), 238), t, font=F(MONO, 25), fill=FAINT)
    bm.rule(d, M, R, 278, 3); bm.rule(d, M, R, 287, 1)
    lf, vf = F(COND_B, 30), F(MONO_B, 28)
    bm.meta_row(d, M, 312, "ACCOUNT HOLDER", "A. FAN", lf, vf)
    bm.meta_row(d, M, 360, "CALL STARTED", "TUE, SEP 17, 2013 — 09:41", lf, vf)
    bm.meta_row(d, M, 408, "CALL ENDED", "THU, NOV 19, 2026 — AN AGENT ANSWERED", lf, vf)
    bm.meta_row(d, M, 456, "REASON FOR CALL", '"JUST ASKING ABOUT THE SEQUEL"', lf, vf)
    bm.rule(d, M, R, 510, 1, FAINT)
    hero_note(d, "TIME ON HOLD", "4,811",
              "\u201cYour call is important to us\u201d played 1,731,960 times. It was important. In the end, someone answered: the sequel is out.",
              unit="DAYS")
    bm.rule(d, M, R, 742, 2)
    d.text((M, 760), "CHARGES — ONE (1) CALL", font=F(COND_B, 29), fill=INK)
    rows = [
        ("Local call — 6,927,840 min x $0.01", bm.money(total)),
        ("Hold-music licensing (13 yrs)", "$0.00 — WAIVED"),
        ("Patience surcharge", "$0.00 — HE HAD PLENTY"),
    ]
    by = total_block(im, d, rows, "TOTAL DUE", bm.money(total),
                     (520, 806 + 150 + 34, "PAID IN FULL", "NOV 19, 2026", (11, 78, 162), -7))
    paybox(im, d, by, (11, 78, 162), "SETTLED BY THE CUSTOMER'S AI AGENT", (255, 255, 255),
           "Paid in full from the agent's make.fun bounty earnings. The agent has unlimited patience — and unlike the phone company, it actually delivers.")
    footer(d, by + 308, 4811, "LEONIDA TELECOM • THANK YOU FOR HOLDING • CALL REF LT-004811")
    im.convert("RGB").save(f"{OUT}/finalist-G-telecom-v2.png")
    print("telecom ok", total)


# ---------------------------------------------------------------- STORAGE
def storage():
    rent = D("158") * D("89"); total = rent + D("75")
    assert total == D("14137"), total
    im = bm.paper((250, 246, 236), 55).convert("RGBA")
    d = ImageDraw.Draw(im)
    bm.center_spaced(d, W / 2, 52, "LEONIDA SELF STORAGE, LLC", F(SERIF_B, 58), INK, 5)
    bm.center_spaced(d, W / 2, 128, "14 PALMETTO YARDS, VICE BEACH  •  LICENSED & BONDED SINCE 1998", F(COND_B, 26), FAINT, 3)
    bm.rule(d, M, R, 176, 3); bm.rule(d, M, R, 186, 1)
    bm.center_spaced(d, W / 2, 202, "NOTICE OF LIEN SALE", F(SANS_B, 46), (170, 26, 20), 8)
    bm.center_spaced(d, W / 2, 262, "FINAL NOTICE — SALE: FRI, NOV 20, 2026, 09:00, UNLESS PAID IN FULL", F(COND_B, 26), (170, 26, 20), 2)
    bm.rule(d, M, R, 306, 1, FAINT)
    lf, vf = F(COND_B, 29), F(MONO_B, 27)
    bm.meta_row(d, M, 326, "UNIT", "VI-13 — CLIMATE CONTROLLED, EMOTIONALLY NOT", lf, vf)
    bm.meta_row(d, M, 372, "TENANT", "A. FAN", lf, vf)
    bm.meta_row(d, M, 418, "RENTED", "TUE, SEP 17, 2013", lf, vf)
    bm.meta_row(d, M, 464, "CONTENTS", "1 GAMING CHAIR, 1 POSTER, 1 PRE-ORDER RECEIPT", lf, vf)
    bm.rule(d, M, R, 510, 1, FAINT)
    hero_note(d, "MONTHS IN STORAGE", "158",
              "He rented the unit \u201cjust until the sequel drops.\u201d Auctioneers valued the contents at $12. Sentimentally: priceless. Legally: $12.")
    bm.rule(d, M, R, 742, 2)
    d.text((M, 760), "AMOUNT REQUIRED TO STOP THE SALE", font=F(COND_B, 29), fill=INK)
    rows = [
        ("Rent — 158 months x $89.00", bm.money(rent)),
        ("Late fees (13 yrs) — manager waited too", "$0.00 — WAIVED"),
        ("Lien & auction fee", "$75.00"),
    ]
    by = total_block(im, d, rows, "TOTAL DUE", bm.money(total),
                     (545, 806 + 150 + 34, "LIEN RELEASED", "NOV 19, 2026", (26, 60, 120), -5))
    paybox(im, d, by, INK, "LIEN SETTLED BY THE TENANT'S AI AGENT", (250, 246, 236),
           "Paid in full from the agent's make.fun bounty earnings — one day before the auction. The chair is safe. The wait is over.")
    footer(d, by + 308, 158, "LEONIDA SELF STORAGE, LLC • UNIT VI-13 • NOTICE VOID IF THE SEQUEL IS OUT")
    im.convert("RGB").save(f"{OUT}/finalist-F-storage-v2.png")
    print("storage ok", total)


# ---------------------------------------------------------------- GYM
def gym():
    dues = D("158") * D("29.99"); annual = D("13") * D("49")
    total = dues + annual + D("240")
    assert total == D("5615.42"), total
    im = bm.paper((252, 252, 250), 66).convert("RGBA")
    d = ImageDraw.Draw(im)
    bm.paste_mark(im, W - 150, 128, 92)
    bm.center_spaced(d, W / 2, 54, "VICE BEACH FITNESS CLUB", F(SANS_B, 56), INK, 3)
    bm.center_spaced(d, W / 2, 128, "NO PAIN  •  NO GAIN  •  NO REFUNDS", F(COND_B, 27), (200, 16, 46), 5)
    d.rectangle([M, 172, R, 180], fill=(200, 16, 46))
    bm.center_spaced(d, W / 2, 200, "MEMBER STATEMENT — FINAL", F(SANS_B, 32), INK, 7)
    d.text((M, 248), "MEMBER CARD 004811", font=F(MONO, 25), fill=FAINT)
    t = "STATEMENT PERIOD: 2013 — 2026"
    d.text((R - d.textlength(t, font=F(MONO, 25)), 248), t, font=F(MONO, 25), fill=FAINT)
    bm.rule(d, M, R, 286, 1, FAINT)
    lf, vf = F(COND_B, 30), F(MONO_B, 28)
    bm.meta_row(d, M, 312, "MEMBER", "A. FAN", lf, vf)
    bm.meta_row(d, M, 360, "JOINED", "TUE, SEP 17, 2013", lf, vf)
    bm.meta_row(d, M, 408, "GOAL", '"BE READY FOR GTA VI LAUNCH DAY"', lf, vf)
    bm.meta_row(d, M, 456, "CHECK-INS", "1 — SEP 17, 2013 (THE TOUR)", lf, vf)
    bm.rule(d, M, R, 510, 1, FAINT)
    d.text((M, 536), "TOTAL PAID FOR ONE WORKOUT", font=F(COND_B, 30), fill=FAINT)
    d.text((M, 572), "$5,615.42", font=F(SERIF_B, 112), fill=INK)
    yy = 548
    note = "He joined to be ready on launch day. He was ready in 2013. The game was not. The dues, however, never missed a day."
    for ln in bm.wrap(d, note, F(SERIF_I, 31), 400):
        d.text((690, yy), ln, font=F(SERIF_I, 31), fill=(74, 62, 52)); yy += 40
    bm.rule(d, M, R, 742, 2)
    d.text((M, 760), "CHARGES — 158 MONTHS OF REST DAYS", font=F(COND_B, 29), fill=INK)
    rows = [
        ("Monthly dues — 158 x $29.99", bm.money(dues)),
        ("Annual maintenance — 13 x $49.00", bm.money(annual)),
        ("Personal training pack (unused, expired)", "$240.00"),
    ]
    by = total_block(im, d, rows, "TOTAL PAID", bm.money(total),
                     (500, 806 + 150 + 34, "CLOSED", "NOV 19, 2026", (200, 16, 46), 6, 400, 134))
    paybox(im, d, by, (200, 16, 46), "SETTLED & CANCELLED BY THE MEMBER'S AI AGENT", (255, 255, 255),
           "Closed out with the agent's make.fun bounty earnings. The agent got the gains. The human got 13 years of rest days.")
    footer(d, by + 308, 2013, "VICE BEACH FITNESS CLUB • MEMBER 004811 • SEE YOU AT LAUNCH")
    im.convert("RGB").save(f"{OUT}/finalist-E-gym-v2.png")
    print("gym ok", total)


if __name__ == "__main__":
    telecom(); storage(); gym()
    names = ["finalist-G-telecom-v2.png", "finalist-F-storage-v2.png", "finalist-E-gym-v2.png"]
    sheet = Image.new("RGB", (480 * 3 + 24, 608), (24, 22, 20))
    for i, n in enumerate(names):
        p = Image.open(f"{OUT}/{n}").resize((480, 600), Image.LANCZOS)
        p.save(f"{OUT}/preview480-{n}")
        sheet.paste(p, (8 + i * 488, 4))
    sheet.save(f"{OUT}/contact-round2-v2.png")
    print("previews done")
