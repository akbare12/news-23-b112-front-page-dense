#!/usr/bin/env python3
"""news-23 b112 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    for p in (os.path.join(FONT_DIR, name),
              "/usr/share/fonts/truetype/liberation/" + name):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
RED = (178, 24, 24)
DARKRED = (140, 16, 16)
NAVY = (16, 38, 84)
GOLD = (198, 148, 28)
CREAM = (250, 244, 228)
LGRAY = (238, 238, 238)
MGRAY = (200, 200, 200)
DGRAY = (90, 90, 90)
GREEN = (34, 96, 44)
MAPGREEN = (178, 208, 160)
TEAL = (0, 110, 110)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)


def text(x, y, s, f, fill, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def text_w(s, f):
    return d.textlength(s, font=f)


def wrap(s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rect(x0, y0, x1, y1, fill, outline=None, width=1):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)


def center_text(cx, y, s, f, fill):
    d.text((cx, y), s, font=f, fill=fill, anchor="ma")


# ---------------- masthead ----------------
rect(0, 0, W, 56, BLACK)
text(16, 4, "THE WORLD TODAY", SERIF_B(44), WHITE)
text(W - 16, 18, "MONDAY 23 NOVEMBER 2026", SANS_B(15), GOLD, anchor="ra")

# ---------------- kicker ----------------
rect(0, 56, W, 78, RED)
center_text(W // 2, 60, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
            SANS_B(13), WHITE)

# ---------------- number strip: 5 cols x 2 rows ----------------
NUMBERS = [
    ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"), ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL STABILISATION FUND"), ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"), ("12,000", "CLEARED IN MANCHESTER"),
    ("264 kg", "EXPLOSIVES SEIZED"), ("$107.3B", "ANTHROPIC IPO"),
]
NX0, NY0, NCW = 8, 80, 201
for i, (val, lab) in enumerate(NUMBERS):
    col, row = i % 5, i // 5
    x = NX0 + col * NCW
    y = NY0 + row * 24
    text(x, y, val, SANS_B(16), RED if col == 0 else NAVY)
    text(x, y + 15, lab, SANS(8), DGRAY)

# ---------------- region bar ----------------
REGIONS = [("ASIA-PACIFIC 7", 7, (16, 38, 84)), ("AMERICAS 8", 8, RED),
           ("MIDDLE EAST 6", 6, (0, 110, 110)), ("EUROPE 5", 5, (90, 60, 140)),
           ("AFRICA 3", 3, GREEN), ("WORLD 2", 2, (90, 90, 90))]
rx = 8
for name, cnt, col in REGIONS:
    w = round(1008 * cnt / 31)
    rect(rx, 128, rx + w - 1, 145, col)
    center_text(rx + w // 2, 131, name, SANS_B(10), WHITE)
    rx += w

# ---------------- UTC strip ----------------
rect(0, 146, W, 161, LGRAY)
text(8, 149, "THE DAY IN UTC   \u00b700:00 Kospi dives   \u00b705:30 Guterres opens   \u00b709:00 Power Index   \u00b712:00 Paris 2% tax   \u00b715:00 Kyiv missiles",
     SANS(10), BLACK)
text(W - 8, 149, "~ APPROX", SANS(10), DGRAY, anchor="ra")

# ---------------- heroes ----------------
HX = [8, 344, 680]
HW = 328


def hero(x, scene_fn, strip_label, headline, body, source, chip="REPORTED"):
    # scene
    scene_fn(x, 162, HW, 118)
    # black strip under scene
    rect(x, 280, x + HW, 294, BLACK)
    text(x + 6, 283, strip_label, SANS_B(10), WHITE)
    # headline (2 lines max), clear of the strip
    hl = wrap(headline, SERIF_B(18), HW - 4)
    hy = 299
    for ln in hl[:2]:
        text(x + 2, hy, ln, SERIF_B(18), BLACK)
        hy += 21
    # body (2 lines)
    bl = wrap(body, SANS(11), HW - 4)
    by = 343
    for ln in bl[:2]:
        text(x + 2, by, ln, SANS(11), BLACK)
        by += 14
    # source + chip row
    text(x + 2, 371, source, SANS(10), DGRAY)
    cw = text_w(chip, SANS_B(9)) + 10
    rect(x + HW - cw, 369, x + HW, 380, NAVY if chip == "REPORTED" else RED)
    center_text(x + HW - cw // 2, 371, chip, SANS_B(9), WHITE)


def scene_kospi(x, y, w, h):
    rect(x, y, x + w, y + h, (8, 22, 54))
    # buildings with lit windows
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 30:
        bw = rnd.randint(22, 38)
        bh = rnd.randint(38, 88)
        by = y + h - bh
        rect(bx, by, bx + bw, y + h, (16, 34, 70))
        for wy in range(by + 6, y + h - 6, 12):
            for wx in range(bx + 4, bx + bw - 4, 10):
                if rnd.random() < 0.55:
                    rect(wx, wy, wx + 4, wy + 6, (255, 214, 90))
        bx += bw + 4
    # big -3.3% top-left, chart line below it
    text(x + 10, y + 6, "-3.3%", SANS_B(34), WHITE)
    pts = [(x + 20, y + 62), (x + 70, y + 70), (x + 120, y + 66), (x + 170, y + 82),
           (x + 220, y + 78), (x + 265, y + 96), (x + 310, y + 104)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE, outline=(255, 140, 40), width=2)


def scene_guterres(x, y, w, h):
    rect(x, y, x + w, y + h, (10, 64, 34))
    text(x + 12, y + 8, "150", SANS_B(46), GOLD)
    for i, ln in enumerate(["DELEGATES", "BACK A RISK", "FRAMEWORK"]):
        text(x + 12, y + 58 + i * 19, ln, SANS_B(17), GOLD)
    # globe right
    cx, cy, r = x + w - 62, y + 58, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 224, 190), outline=(255, 255, 255), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(90, 140, 100), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(90, 140, 100), width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(90, 140, 100), width=1)


def scene_power(x, y, w, h):
    rect(x, y, x + w, y + h, CREAM)
    text(x + 8, y + 6, "NARROWEST SINCE 2018", SANS_B(10), BLACK)
    text(x + w - 8, y + 6, "GAP 5.3", SANS_B(11), RED, anchor="ra")
    bars = [("78.9", "US", NAVY, 78.9), ("73.6", "CHINA", RED, 73.6), ("40.5", "INDIA", GOLD, 40.5)]
    bw, gap = 62, 34
    bx = x + 22
    for val, lab, col, v in bars:
        bh = int(v * 0.62)
        by = y + h - 26 - bh
        text(bx + bw // 2, by - 18, val, SANS_B(15), BLACK, anchor="ma")
        rect(bx, by, bx + bw, y + h - 26, col)
        text(bx + bw // 2, y + h - 24, lab, SANS_B(11), BLACK, anchor="ma")
        bx += bw + gap


hero(HX[0], scene_kospi, "KOSPI 4,708.54  \u00b7  -161 PTS",
     "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE")
hero(HX[1], scene_guterres, "UN  \u00b7  BRIDGETOWN",
     "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS")
hero(HX[2], scene_power, "ASIA POWER INDEX 2026",
     "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE")

# ---------------- cards header ----------------
rect(0, 384, W, 402, BLACK)
text(8, 387, "MORE OF THE DAY  \u2014  10 STORIES", SANS_B(12), WHITE)

CARDS = [
    ("AMERICAS", RED, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED"),
    ("AMERICAS", RED, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", TEAL, "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", NAVY, "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", (150, 110, 0), "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", (150, 110, 0), "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", (90, 60, 140), "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", TEAL, "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", (90, 60, 140), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (90, 60, 140), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
CW, CGAP, CH, CROW = 196, 6, 68, 72
for i, (cat, col, head, body, src, chip) in enumerate(CARDS):
    c, r = i % 5, i // 5
    x = 8 + c * (CW + CGAP)
    y = 406 + r * CROW
    rect(x, y, x + CW, y + CH, WHITE, outline=MGRAY, width=1)
    rect(x, y, x + CW, y + 14, col)
    text(x + 4, y + 2, cat, SANS_B(9), WHITE)
    text(x + CW - 4, y + 2, str(i + 1), SANS_B(9), WHITE, anchor="ra")
    hl = wrap(head, SANS_B(11), CW - 8)
    hy = y + 17
    for ln in hl[:2]:
        text(x + 4, hy, ln, SANS_B(11), BLACK)
        hy += 12
    text(x + 4, y + 43, body, SANS(10), BLACK)
    text(x + 4, y + 56, src, SANS(9), DGRAY)
    cc = NAVY if chip == "REPORTED" else RED
    cw = text_w(chip, SANS_B(9)) + 10
    rect(x + CW - cw, y + 52, x + CW, y + 63, cc)
    center_text(x + CW - cw // 2, y + 54, chip, SANS_B(9), WHITE)

# ---------------- map + ALSO header ----------------
rect(0, 554, W, 572, BLACK)
text(8, 557, "WHERE IT HAPPENED", SANS_B(12), WHITE)
text(344, 557, "ALSO ON MONDAY", SANS_B(12), WHITE)

# ---------------- map ----------------
MAPX, MAPY = 8, 576
# Americas blob
d.polygon([(30, 610), (150, 610), (158, 720), (122, 852), (58, 862), (26, 752)], fill=MAPGREEN)
# Europe blob
d.polygon([(168, 592), (242, 592), (246, 662), (172, 668)], fill=MAPGREEN)
# Africa blob
d.polygon([(172, 678), (246, 678), (252, 772), (206, 802), (176, 742)], fill=MAPGREEN)
# Asia blob
d.polygon([(256, 602), (326, 602), (330, 732), (286, 792), (250, 702)], fill=MAPGREEN)

PINS = [(305, 628, 1), (100, 822, 2), (296, 652, 3), (80, 692, 4), (110, 657, 5),
        (240, 626, 6), (196, 630, 7), (186, 600, 8), (222, 604, 9), (168, 622, 10),
        (250, 686, 11), (230, 716, 12), (210, 762, 13)]
for px, py, n in PINS:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    center_text(px, py - 7, str(n), SANS_B(9), WHITE)

text(8, 868, "Pins 1\u201313:  1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing  \u00b7  4 Washington", SANS(9), BLACK)
text(8, 880, "5 New York  \u00b7  6 Kyiv  \u00b7  7 Paris  \u00b7  8 London  \u00b7  9 Warsaw", SANS(9), BLACK)
text(8, 892, "10 Manchester  \u00b7  11 Beirut  \u00b7  12 Gaza  \u00b7  13 Khartoum", SANS(9), BLACK)

# ---------------- ALSO list ----------------
ALSO = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after Antalya pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
    "23. Bahrain: strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe [CLAIM]",
    "25. Sudan: defences down drones [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(ALSO):
    col, row = i // 9, i % 9
    x = 344 + col * 340
    y = 580 + row * 36
    if "[CLAIM]" in item:
        main, tag = item.split(" [")
        text(x, y, main, SANS(11), BLACK)
        text(x + text_w(main + " ", SANS(11)), y, "[" + tag, SANS_B(11), RED)
    else:
        text(x, y, item, SANS(11), BLACK)

# ---------------- DATE CHECK ----------------
rect(8, 914, 1016, 962, WHITE, outline=RED, width=2)
text(16, 919, "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u2014  STORIES DATED 23 NOV ONLY",
     SANS_B(12), RED)
text(16, 938, "LEFT OUT \u2014 NOT 23 NOV:  Dems reach 258 (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo captured (22 Nov)  \u00b7  EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)",
     SANS(10), BLACK)
text(16, 950, "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
     SANS(10), BLACK)

# ---------------- footer ----------------
text(8, 970, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
     SANS(9), DGRAY)
text(8, 983, "CHIPS: REPORTED = confirmed by wires  \u00b7  CLAIM = one side\u2019s claim, not independently confirmed  \u00b7  ONGOING = still developing.",
     SANS(9), DGRAY)
text(8, 996, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
     SANS(9), DGRAY)
center_text(W // 2, 1010, "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
            SANS_B(11), GOLD)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
