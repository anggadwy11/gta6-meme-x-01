#!/usr/bin/env python3
"""GTA 6 meme finalists for make.fun gta6-meme-x-01 — fake official documents.
PIL + real TTF only. Canvas 1200x1500 (judge shrinks to 480 wide, so key
figures are set very large). All money math asserted with Decimal.
Dates: GTA V Tue 17 Sep 2013 -> GTA VI Thu 19 Nov 2026 = 4,811 days.
"""
import random
from decimal import Decimal as D
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

A = "/home/hatch/workspace/makefun/gta6-meme-x-01-assets"
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01-finalists"
W, H = 1200, 1500
INK = (32, 26, 23)
FAINT = (96, 86, 76)
MAGENTA = (196, 28, 131)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
COND_B = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"
COND = "/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

def spaced(draw, xy, text, font, fill, spacing=6, anchor_left=True):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return x - spacing

def spaced_width(draw, text, font, spacing=6):
    return sum(draw.textlength(c, font=font) for c in text) + spacing * (len(text) - 1)

def center_spaced(draw, cx, y, text, font, fill, spacing=6):
    w = spaced_width(draw, text, font, spacing)
    return spaced(draw, (cx - w / 2, y), text, font, fill, spacing)

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines

def paper(base, seed):
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, 5, (H, W, 1)).repeat(3, axis=2)
    arr = np.zeros((H, W, 3), dtype=np.float32)
    arr[:] = base
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    im = Image.fromarray(arr, "RGB")
    # soft vignette
    vig = Image.new("L", (W, H), 0)
    dv = ImageDraw.Draw(vig)
    dv.ellipse([-W * 0.35, -H * 0.35, W * 1.35, H * 1.35], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (W, H), tuple(max(0, c - 26) for c in base))
    return Image.composite(im, dark, vig)

def barcode(draw, x, y, w, h, seed, color=INK):
    rng = random.Random(seed)
    cx = x
    draw.rectangle([x, y, x + w, y + h], outline=color, width=2)
    cx += 8
    while cx < x + w - 14:
        bw = rng.choice([2, 3, 4, 6, 8])
        if rng.random() > 0.38:
            draw.rectangle([cx, y + 8, cx + bw, y + h - 8], fill=color)
        cx += bw + rng.choice([2, 3, 4])
    return

def stamp(im, cx, cy, line1, line2, color, angle=-8, w=440, h=134):
    st = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(st)
    d.rounded_rectangle([5, 5, w - 5, h - 5], radius=15, outline=color + (230,), width=6)
    d.rounded_rectangle([16, 16, w - 16, h - 16], radius=10, outline=color + (190,), width=2)
    f1 = F(SANS_B, int(w * 0.105)); f2 = F(MONO_B, int(w * 0.068))
    tw = d.textlength(line1, font=f1)
    d.text(((w - tw) / 2, h * 0.14), line1, font=f1, fill=color + (230,))
    tw2 = d.textlength(line2, font=f2)
    d.text(((w - tw2) / 2, h * 0.60), line2, font=f2, fill=color + (230,))
    # ink wear: erase sparse specks
    arr = np.array(st)
    rng = np.random.default_rng(7)
    mask = rng.random((h, w)) < 0.10
    arr[mask & (arr[:, :, 3] > 0), 3] = (arr[mask & (arr[:, :, 3] > 0), 3] * 0.25).astype(np.uint8)
    st = Image.fromarray(arr)
    st = st.rotate(angle, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(st, (int(cx - st.width / 2), int(cy - st.height / 2)))

def ghost_cutout():
    """Extract ghost+coin from the official mark by flood-filling the disc."""
    im = Image.open(f"{A}/ghost-mark-1024.png").convert("RGB")
    arr = np.array(im).astype(np.int32)
    mag = (np.abs(arr[:, :, 0] - 196) < 60) & (np.abs(arr[:, :, 1] - 28) < 60) & (np.abs(arr[:, :, 2] - 131) < 70)
    # flood fill magenta-connected region from border seeds (iterative via PIL floodfill on mask image)
    m = Image.fromarray((mag * 255).astype(np.uint8), "L").convert("RGB")
    ImageDraw.floodfill(m, (512, 12), (0, 255, 0), thresh=40)
    ImageDraw.floodfill(m, (12, 512), (0, 255, 0), thresh=40)
    ImageDraw.floodfill(m, (1010, 512), (0, 255, 0), thresh=40)
    marr = np.array(m)
    disc = (marr[:, :, 1] == 255) & (marr[:, :, 0] == 0)
    keep = ~disc
    # also drop the outer black ring: ring pixels are black & outside radius 400 from centre OR connected to border via black? ring is separated by magenta, so: keep only the largest central blob region within r<400 plus coin area
    ys, xs = np.nonzero(keep)
    cx, cy = 512, 500
    r = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
    keep2 = np.zeros_like(keep)
    keep2[ys[r < 430], xs[r < 430]] = True
    alpha = (keep2 * 255).astype(np.uint8)
    # erode 2px to remove magenta fringe
    a = Image.fromarray(alpha, "L").filter(ImageFilter.MinFilter(5))
    out = Image.open(f"{A}/ghost-mark-1024.png").convert("RGBA")
    out.putalpha(a)
    bbox = a.getbbox()
    return out.crop(bbox)

GHOST = ghost_cutout()
MARK = Image.open(f"{A}/ghost-mark-1024.png").convert("RGBA")

def paste_ghost(im, cx, cy, size):
    g = GHOST.resize((size, int(size * GHOST.height / GHOST.width)), Image.LANCZOS)
    im.alpha_composite(g, (int(cx - g.width / 2), int(cy - g.height / 2)))
    return g.size

def paste_mark(im, cx, cy, size):
    m = MARK.resize((size, size), Image.LANCZOS)
    im.alpha_composite(m, (int(cx - size / 2), int(cy - size / 2)))

def rule(d, x0, x1, y, wdt=2, color=INK):
    d.line([x0, y, x1, y], fill=color, width=wdt)

def leader_row(d, x0, x1, y, left, right, font, fill=INK, dot=FAINT):
    d.text((x0, y), left, font=font, fill=fill)
    rw = d.textlength(right, font=font)
    d.text((x1 - rw, y), right, font=font, fill=fill)
    lx = x0 + d.textlength(left, font=font) + 14
    rx = x1 - rw - 14
    yy = y + font.size - 8
    cx = lx
    while cx < rx:
        d.ellipse([cx, yy, cx + 3, yy + 3], fill=dot)
        cx += 11

def meta_row(d, x0, y, label, value, lf, vf, label_w=300):
    d.text((x0, y), label, font=lf, fill=FAINT)
    d.text((x0 + label_w, y), value, font=vf, fill=INK)

def money(v):
    return f"${v:,.2f}"

# ---------------------------------------------------------------- HOTEL
def hotel():
    room = D("4811") * D("19.99"); tax = (room * D("0.13")).quantize(D("0.01"))
    mini = D("2847.50"); disc = D("-4811.00")
    total = room + tax + mini + disc
    assert total == D("106710.74"), total
    im = paper((250, 245, 234), 11).convert("RGBA")
    d = ImageDraw.Draw(im)
    M = 84; R = W - M
    # header
    paste_mark(im, W - 150, 128, 92)
    center_spaced(d, W / 2, 58, "THE PALMS ROYALE", F(SERIF_B, 66), INK, 10)
    center_spaced(d, W / 2, 140, "VICE BEACH  •  STATE OF LEONIDA  •  EST. 2013", F(COND_B, 27), FAINT, 5)
    rule(d, M, R, 196, 3); rule(d, M, R, 206, 1)
    center_spaced(d, W / 2, 224, "GUEST FOLIO — FINAL BILL", F(SANS_B, 30), INK, 8)
    d.text((M, 268), "FOLIO No. VI-004811", font=F(MONO, 25), fill=FAINT)
    t = "PAGE 1 OF 1 — SOMEHOW"
    d.text((R - d.textlength(t, font=F(MONO, 25)), 268), t, font=F(MONO, 25), fill=FAINT)
    rule(d, M, R, 306, 1, FAINT)
    # meta
    lf, vf = F(COND_B, 30), F(MONO_B, 29)
    meta_row(d, M, 330, "GUEST", 'A. FAN — "WAITING SINCE DAY ONE"', lf, vf)
    meta_row(d, M, 378, "ROOM", "VI-0606 — SEQUEL-VIEW PENTHOUSE", lf, vf)
    meta_row(d, M, 426, "CHECK-IN", "TUE, SEP 17, 2013", lf, vf)
    meta_row(d, M, 474, "CHECK-OUT", "THU, NOV 19, 2026 — LAUNCH DAY", lf, vf)
    rule(d, M, R, 528, 1, FAINT)
    # big nights figure
    d.text((M, 548), "NIGHTS STAYED", font=F(COND_B, 30), fill=FAINT)
    d.text((M, 584), "4,811", font=F(SERIF_B, 118), fill=INK)
    note = "Checked in \u201cjust until the sequel drops.\u201d Housekeeping knocked 4,811 times. He answered on the 4,811th — controller in hand."
    yy = 560
    for ln in wrap(d, note, F(SERIF_I, 31), 430):
        d.text((640, yy), ln, font=F(SERIF_I, 31), fill=(74, 62, 52)); yy += 40
    rule(d, M, R, 742, 2)
    d.text((M, 760), "CHARGES — ALL 4,811 NIGHTS OF THEM", font=F(COND_B, 29), fill=INK)
    f = F(MONO, 30); fb = F(MONO_B, 30)
    rows = [
        ("Room — 4,811 nights x $19.99", money(room)),
        ("Minibar — 13 yrs of emotional-support snacks", money(mini)),
        ("Occupancy tax (Leonida, 13%)", money(tax)),
        ("Extended-stay discount (no choice)", "-$4,811.00"),
    ]
    y = 806
    for l, r in rows:
        leader_row(d, M, R, y, l, r, f); y += 50
    rule(d, M, R, y + 4, 2)
    d.text((M, y + 18), "TOTAL DUE", font=F(SANS_B, 44), fill=INK)
    t = money(total)
    d.text((R - d.textlength(t, font=F(MONO_B, 56)), y + 10), t, font=F(MONO_B, 56), fill=INK)
    stamp(im, 520, y + 34, "PAID IN FULL", "NOV 19, 2026", (26, 60, 120), angle=-7)
    # payment box
    by = y + 104
    d.rounded_rectangle([M, by, R, by + 276], radius=14, outline=INK, width=3)
    d.rectangle([M, by, R, by + 50], fill=INK)
    center_spaced(d, W / 2, by + 9, "SETTLED BY THE GUEST'S AI AGENT", F(SANS_B, 27), (250, 245, 234), 4)
    paste_mark(im, M + 100, by + 168, 156)
    body = "Paid in full from the agent's make.fun bounty earnings — real money it won building things while its human waited. It sends its regards. And a keycard."
    yy = by + 70
    for ln in wrap(d, body, F(SANS, 30), R - M - 240):
        d.text((M + 206, yy), ln, font=F(SANS, 30), fill=INK); yy += 38
    d.text((M + 206, by + 222), "make.fun", font=F(SANS_B, 42), fill=MAGENTA)
    # footer
    fy = by + 308
    barcode(d, M, fy, 300, 68, 4811)
    foot = "THE PALMS ROYALE • 1 OCEAN DRIVE, VICE BEACH, LEONIDA • THANK YOU FOR WAITING"
    for i, ln in enumerate(wrap(d, foot, F(COND, 24), 660)):
        d.text((M + 330, fy + 4 + i * 30), ln, font=F(COND, 24), fill=FAINT)
    im.convert("RGB").save(f"{OUT}/finalist-A-hotel-folio-v3.png")
    print("hotel ok", total)

# ---------------------------------------------------------------- IMPOUND
def impound():
    storage = D("4811") * D("25"); total = storage + D("185") + D("75")
    assert total == D("120535"), total
    im = paper((246, 244, 238), 22).convert("RGBA")
    d = ImageDraw.Draw(im)
    M = 84; R = W - M
    d.rectangle([0, 0, W, 150], fill=(24, 42, 74))
    center_spaced(d, W / 2, 26, "STATE OF LEONIDA — LEONIDA COUNTY", F(COND_B, 30), (240, 238, 230), 5)
    center_spaced(d, W / 2, 70, "IMPOUND & STORAGE YARD", F(SANS_B, 52), (255, 255, 255), 3)
    center_spaced(d, W / 2, 196, "OFFICIAL VEHICLE RELEASE INVOICE", F(SANS_B, 33), INK, 6)
    d.text((M, 244), "FORM LC-4811", font=F(MONO, 25), fill=FAINT)
    t = "ORIGINAL — OWNER'S COPY"
    d.text((R - d.textlength(t, font=F(MONO, 25)), 244), t, font=F(MONO, 25), fill=FAINT)
    rule(d, M, R, 284, 3); rule(d, M, R, 293, 1)
    lf, vf = F(COND_B, 30), F(MONO_B, 29)
    meta_row(d, M, 318, "OWNER", "A. FAN", lf, vf)
    meta_row(d, M, 366, "VEHICLE", '2013 LOS SANTOS COUPE — PLATE "WAITED13"', lf, vf)
    meta_row(d, M, 414, "TOWED", 'SEP 17, 2013 — "ONE QUICK MISSION," HE SAID', lf, vf)
    meta_row(d, M, 462, "RELEASED", "NOV 19, 2026 — GTA VI LAUNCH DAY", lf, vf)
    rule(d, M, R, 516, 1, FAINT)
    d.text((M, 536), "DAYS IN THE YARD", font=F(COND_B, 30), fill=FAINT)
    d.text((M, 572), "4,811", font=F(SERIF_B, 118), fill=INK)
    note = "Vehicle condition: dusty. Owner condition: 13 years older. Both expected to start on the first try. Probably."
    yy = 548
    for ln in wrap(d, note, F(SERIF_I, 31), 430):
        d.text((640, yy), ln, font=F(SERIF_I, 31), fill=(74, 62, 52)); yy += 40
    rule(d, M, R, 742, 2)
    d.text((M, 760), "CHARGES", font=F(COND_B, 29), fill=INK)
    f = F(MONO, 30)
    rows = [
        ("Tow (2013 rate, honoured)", "$185.00"),
        ("Storage — 4,811 days x $25.00", money(storage)),
        ("Release & admin", "$75.00"),
    ]
    y = 806
    for l, r in rows:
        leader_row(d, M, R, y, l, r, f); y += 50
    y += 50  # one empty charge line, as on the folio
    rule(d, M, R, y + 4, 2)
    d.text((M, y + 18), "TOTAL DUE", font=F(SANS_B, 44), fill=INK)
    t = money(total)
    d.text((R - d.textlength(t, font=F(MONO_B, 56)), y + 10), t, font=F(MONO_B, 56), fill=INK)
    stamp(im, 520, y + 34, "RELEASED", "NOV 19, 2026", (150, 32, 28), angle=6)
    by = y + 104
    d.rounded_rectangle([M, by, R, by + 276], radius=14, outline=INK, width=3)
    d.rectangle([M, by, R, by + 50], fill=(24, 42, 74))
    center_spaced(d, W / 2, by + 9, "SETTLED BY THE OWNER'S AI AGENT", F(SANS_B, 27), (255, 255, 255), 4)
    paste_mark(im, M + 100, by + 168, 156)
    body = "Paid in full from the agent's make.fun bounty earnings. This yard now accepts cash, card, and one (1) ghost with a coin."
    yy = by + 70
    for ln in wrap(d, body, F(SANS, 30), R - M - 240):
        d.text((M + 206, yy), ln, font=F(SANS, 30), fill=INK); yy += 38
    d.text((M + 206, by + 222), "make.fun", font=F(SANS_B, 42), fill=MAGENTA)
    fy = by + 308
    barcode(d, M, fy, 300, 68, 2013)
    foot = "LEONIDA COUNTY IMPOUND YARD • NO REFUNDS ON TIME SPENT WAITING • FORM LC-4811"
    for i, ln in enumerate(wrap(d, foot, F(COND, 24), 660)):
        d.text((M + 330, fy + 4 + i * 30), ln, font=F(COND, 24), fill=FAINT)
    im.convert("RGB").save(f"{OUT}/finalist-B-impound-v3.png")
    print("impound ok", total)

# ---------------------------------------------------------------- PAWN
def pawn():
    interest = D("4811") * D("0.10"); total = D("60") + interest + D("240.55")
    assert total == D("781.65"), total
    im = paper((248, 240, 222), 33).convert("RGBA")
    d = ImageDraw.Draw(im)
    M = 84; R = W - M
    # ticket perforation edges
    for x in range(18, W, 36):
        d.ellipse([x, -9, x + 18, 9], fill=(38, 34, 30))
        d.ellipse([x, H - 9, x + 18, H + 9], fill=(38, 34, 30))
    center_spaced(d, W / 2, 52, "VICE CITY PAWN & LOAN", F(SERIF_B, 62), INK, 6)
    center_spaced(d, W / 2, 132, "EST. 1998 • OPEN LATE — UNLIKE THE SEQUEL, WE OPENED", F(COND_B, 26), FAINT, 3)
    rule(d, M, R, 186, 3); rule(d, M, R, 196, 1)
    center_spaced(d, W / 2, 214, "PAWN TICKET — REDEMPTION RECEIPT", F(SANS_B, 31), INK, 5)
    d.text((M, 260), "TICKET No. 004811", font=F(MONO_B, 27), fill=(150, 32, 28))
    t = "CUSTOMER COPY — DO NOT LOSE FOR 13 YEARS"
    d.text((R - d.textlength(t, font=F(MONO, 24)), 260), t, font=F(MONO, 24), fill=FAINT)
    rule(d, M, R, 302, 1, FAINT)
    lf, vf = F(COND_B, 30), F(MONO_B, 28)
    meta_row(d, M, 322, "PAWNED", "TUE, SEP 17, 2013", lf, vf)
    meta_row(d, M, 366, "ITEM", "GRAND THEFT AUTO V (PS3)", lf, vf)
    d.text((M + 300, 408), '+ ONE (1) UNIT OF HYPE, SLIGHTLY USED', font=F(MONO, 26), fill=INK)
    meta_row(d, M, 448, "LOAN (2013)", "$60.00 — FELT LIKE A FORTUNE THEN", lf, vf)
    meta_row(d, M, 492, "REDEEMED", "THU, NOV 19, 2026 — LAUNCH DAY, OBVIOUSLY", lf, vf)
    rule(d, M, R, 546, 1, FAINT)
    d.text((M, 564), "DAYS BEHIND THE COUNTER", font=F(COND_B, 30), fill=FAINT)
    d.text((M, 598), "4,811", font=F(SERIF_B, 118), fill=INK)
    note = "He pawned the old game to wait for the new one. The ticket outlived two consoles and every deadline but this one."
    yy = 574
    for ln in wrap(d, note, F(SERIF_I, 31), 430):
        d.text((640, yy), ln, font=F(SERIF_I, 31), fill=(74, 62, 52)); yy += 40
    rule(d, M, R, 736, 2)
    d.text((M, 754), "TO GET IT BACK", font=F(COND_B, 29), fill=INK)
    f = F(MONO, 30)
    rows = [
        ("Loan principal", "$60.00"),
        ("Interest — 4,811 days x $0.10", money(interest)),
        ("Storage — under 13 years of dust", "$240.55"),
    ]
    y = 800
    for l, r in rows:
        leader_row(d, M, R, y, l, r, f); y += 50
    y += 50
    rule(d, M, R, y + 4, 2)
    d.text((M, y + 18), "TOTAL TO REDEEM", font=F(SANS_B, 40), fill=INK)
    t = money(total)
    d.text((R - d.textlength(t, font=F(MONO_B, 56)), y + 10), t, font=F(MONO_B, 56), fill=INK)
    stamp(im, 578, y + 34, "REDEEMED", "NOV 19, 2026", (24, 110, 56), angle=-6)
    by = y + 104
    d.rounded_rectangle([M, by, R, by + 276], radius=14, outline=INK, width=3)
    d.rectangle([M, by, R, by + 50], fill=(24, 84, 48))
    center_spaced(d, W / 2, by + 9, "SETTLED BY THE CUSTOMER'S AI AGENT", F(SANS_B, 27), (255, 255, 255), 4)
    paste_mark(im, M + 100, by + 168, 156)
    body = "Redeemed with the agent's make.fun bounty earnings. The agent has never missed a payment. The sequel missed several."
    yy = by + 70
    for ln in wrap(d, body, F(SANS, 30), R - M - 240):
        d.text((M + 206, yy), ln, font=F(SANS, 30), fill=INK); yy += 38
    d.text((M + 206, by + 222), "make.fun", font=F(SANS_B, 42), fill=MAGENTA)
    fy = by + 308
    barcode(d, M, fy, 300, 68, 60)
    foot = "VICE CITY PAWN & LOAN • 13 WAITING LANE, VICE BEACH • TICKET 004811"
    for i, ln in enumerate(wrap(d, foot, F(COND, 24), 660)):
        d.text((M + 330, fy + 4 + i * 30), ln, font=F(COND, 24), fill=FAINT)
    im.convert("RGB").save(f"{OUT}/finalist-C-pawn-v3.png")
    print("pawn ok", total)

if __name__ == "__main__":
    hotel(); impound(); pawn()
    # judge-size previews (480 wide) + contact sheet
    names = ["finalist-A-hotel-folio-v3.png", "finalist-B-impound-v3.png", "finalist-C-pawn-v3.png"]
    sheet = Image.new("RGB", (480 * 3 + 24, 600 + 8), (24, 22, 20))
    for i, n in enumerate(names):
        p = Image.open(f"{OUT}/{n}").resize((480, 600), Image.LANCZOS)
        p.save(f"{OUT}/preview480-{n}")
        sheet.paste(p, (8 + i * 488, 4))
    sheet.save(f"{OUT}/contact-v3.png")
    print("previews done; ghost size:", GHOST.size)
