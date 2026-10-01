#!/usr/bin/env python3
"""Build the October 2026 Our Special Village newsletter (T404/T397/T398/T400).

Writes newsletter-october-subscriber-preview.html (MailerLite/email: 600px + merge
tags), index.html (hosted browser preview: wider desktop layout + real link
destinations), newsletter-october-2026.txt, and deadlines-october-2026.html.

T404: Three things to know this month — all three items use title 18px /
body 16px (Fall break, voter, clocks). Item 3 was 16/15 because CLOCKS
omitted featured=True. Section heading (21px) and date chips unchanged.
T400: Sensory Spooktacular sits in chronological order in The month ahead
(Sun Oct 25 before Sat Oct 31 Evergreen; Little Luminaries and Cultivate Play).
T410: Free TicketsCandy registration link on Spooktacular. Oct 1: its on-site +
sponsor copy shows openly above the button (expanders don't open in Outlook or Gmail).
Oct 1 (Taylor): this first Village Hall is free, so the ticket says "Free for every
family" instead of the pay-what-you-can boxes. tools/outlook-copy.py makes the
send-it-yourself Outlook copy. Later Oct 1 (Taylor): We Rock's Trick&Treat&Play joins
The month ahead (Sat Oct 31, morning, before Evergreen). The Frist's Sensory Sunday Hour
(Sun Oct 11) is gone: its event page is 404 and the Frist's own calendar, which runs into
late 2027, lists no Sensory Sunday Hour (Oct 11 is a regular Family Sunday).
T430: Wall of Hope returns between New in the library and One question,
answered. Sept 30: the story is Nicole's ("His love needs no words.", from the
site), not Taylor's. Every Wall of Hope signs off with the name, then
Murfreesboro: "✎ Nicole, Murfreesboro". No date. Short share invitation under the card.
T429: Calendar rows for Hickok adds that were missing from The month ahead.
Chronological: rEcess (Sat Oct 3, before Game Day), Dollywood (Wed Oct 21),
Gallatin HOSA Trunk or Treat (Thu Oct 22), Caleb's Friends (Sun Oct 25, after
Spooktacular), Pegram Fall Fest (Thu Oct 29). Evergreen Trunk or Treat keeps
its row and gains the street address plus the flyer blurb. Amanda Rains
Village Hall is Sat Nov 14 and stays out of this October issue.
T398: Village Hall guest block lists only ACCESS website + email (no other
Mercedes/ACCESS contacts).
T397: Village Hall guest photo is the IMG_7283 family photo (children’s
faces already covered) at art/mercedes-family-hearts-160.jpg. New filename
so Cloudflare/browser cache of the T393 headshot dies. Bio still says two
neurodivergent children. ACCESS blurb kept. ACCESS logo omitted so T394
layout stays: title on its own row; photo left of the description, not the
title; desktop title left; mobile title centered.
T394: Village Hall Mercedes title (name + role) sits on its own row above
the photo. Photo is left of her description (bio), vertically centered
with that copy — not left of the title. Desktop/browser-wide: title left-
aligned. Mobile: title centered so “Greater Nashville” stays on one line.
Photo+bio stay a two-column row on mobile (not stacked above the title).
T393: Headshot filename retired from this newsletter (was
art/mercedes-headshot-160.jpg).
T389: We Rock card eyebrow is IN PERSON · WEEKLY · FREE (drop GROUP). Online
Parent Group already says ONLINE · WEEKLY · FREE. No other copy/layout changes.
T388: Desktop/browser-wide title left-align (was name/role next to photo).
T387: Bio says two neurodivergent children (not one child with Autism).
T386: 988 in the footer is a tel: link, matching STEP TN / Disability Rights TN.
T385: Footer names 988 as the Suicide & Crisis Lifeline.
Keeps T379 last polish, T375, T373 spacing, T372 hierarchy/mobile, T367, T365.

Edit this file and run it. Do not hand-edit the generated HTML.

    python3 tools/build-october-2026.py
"""
import argparse
import os
import re

PAGES = "https://tmacocx.github.io/osv-newsletter-october-preview/"
SITE = "https://ourspecialvillagetn.com"
BROWSER_VIEW_URL = PAGES
BROWSER_UNSUB_URL = f"{SITE}/newsletter"
WRTS_URL = "https://werockthespectrummurfreesboro.com/"
ACCESS_URL = "https://www.accessyouredu.com/"
ACCESS_EMAIL = "access.your.education@gmail.com"
MERCEDES_PHOTO = "mercedes-family-hearts-160.jpg"

# Site look (ourspecialvillagetn.com, rebuilt 2026-09-29): navy, cream and gold; Outfit headings,
# Mulish body, Patrick Hand notes; paper cards, pins, tape and cork. Each section wears the costume
# the site's newsletter page promises for it ("What's inside"): the deadlines are a tag on a string,
# the month ahead is a calendar page, library guides are books with a ribbon, the hopeful story is
# a note pinned to the Wall of Hope board, the question is an index card and Village Hall is the
# hall's own bunting, notice board and ticket. Decorations Gmail can't draw from CSS (bunting,
# pins, tape, stamp, hills, taped photos) are the site's own CSS drawn to pictures by
# tools/render-decor.mjs into art/decor/ and each issue's art/ folder.
# Taylor's rule: no word links. a(), tel() and navy_a() all draw buttons.
CREAM = "#f7f1e2"
WHITE = "#fffcf5"      # paper
NOTE = "#fffdf7"       # letter / note paper
BLUSH = "#f4dccd"      # brick-soft
INK = "#1d2c4c"        # navy
BODY = "#3a4760"
MUTED = "#56637a"
ACCENT = "#a9542f"     # brick
BRICK_INK = "#8f4424"
HAIR = "#eadfc8"
RULE = "#eee4cf"
GOLD = "#d7a43e"
GOLD_DEEP = "#b4861f"  # button edge
GOLD_INK = "#8e6614"   # handwritten notes on paper
GOLD_SOFT = "#f3e5c0"
GOLD_DARK = "#7a5b13"
SAND = "#efe9da"       # on-dark text
ON_DARK_MUTED = "#b9c4d8"
NAVY_DEEP = "#14203a"
BLUE_INK = "#3c5378"
BLUE_SOFT = "#e4e9f2"
CORK = "#ecd9ae"
CORK_FRAME = "#c99a45"
CORK_EDGE = "#a67a2c"
SAGE = "#7d8f63"
SAGE_SOFT = "#e1e7d2"
SAGE_INK = "#55653e"
SHADOW = "0 1px 2px rgba(29,44,76,.05),0 12px 28px -16px rgba(29,44,76,.3)"
PAPER_SHADOW = "0 1px 1px rgba(60,40,10,.06),0 22px 34px -22px rgba(60,40,10,.55)"

FONT = "Mulish,'Segoe UI',Helvetica,Arial,sans-serif"
DISPLAY = "Outfit,Arial,sans-serif"
HAND = "'Patrick Hand','Bradley Hand',cursive"

CLASS_FOR = {INK: "os-ink", BODY: "os-body", MUTED: "os-muted", ACCENT: "os-accent",
             GOLD: "os-gold", SAND: "os-sand", CREAM: "os-cream", WHITE: "os-white", GOLD_INK: "os-goldink"}
T = 'role="presentation" cellpadding="0" cellspacing="0"'

SUBJECT = "October: sensory-friendly events + deadlines"
PREHEADER = ("Fall break starts Oct 5. Three things to know this month, a featured Discovery Center night, "
             "two new guides, and one IEP question answered.")

DECOR = "decor/"   # under each issue's art folder


def table(inner, bg=None, style="", cls="", width="100%", attrs=""):
    w = f' width="{width}"' if width else ""
    wcss = "width:100%;" if width == "100%" else (f"width:{width}px;" if width else "")
    bga = f' bgcolor="{bg}"' if bg else ""
    bgc = f"background-color:{bg};" if bg else ""
    c = f' class="{cls}"' if cls else ""
    return f'<table {T}{c}{w}{bga}{attrs} style="{wcss}{bgc}{style}">{inner}</table>'


def img(src, width, alt="", height=None, style="", cls="", fluid=True):
    h = f' height="{height}"' if height else ""
    c = f' class="{cls}"' if cls else ""
    size = f"width:100%;max-width:{width}px;height:auto;" if fluid else f"width:{width}px;height:{height}px;" if height else f"width:{width}px;"
    return f'<img{c} src="{src}" width="{width}"{h} alt="{alt}" style="display:block;border:0;{size}{style}">'


def hand(text, size=21, color=GOLD_INK, margin="0", align="left"):
    """Patrick Hand note, like the site's eyebrows (tilted -2deg where the client allows)."""
    al = "" if align == "left" else f"text-align:{align};"
    return (f'<p class="os-hand {CLASS_FOR.get(color, "")}" style="margin:{margin};font:400 {size}px/{size + 3}px {HAND};'
            f'color:{color};{al}">{text}</p>')


_PILLS_ONLY = re.compile(r'^(?:\s|&nbsp;|&middot;)*(?:<a class="os-pill[^"]*" href="[^"]*"[^>]*>.*?</a>(?:\s|&nbsp;|&middot;)*)+$')


def p(text, size=16, lh=24, color=BODY, weight=400, margin="0", extra="", cls=""):
    """Paragraph. Body copy inherits Mulish from the wrapper cell (lighter email).

    Bold titles (15px+) are Outfit 600; small bold brick/gold labels ("Featured") are
    Patrick Hand notes; a line made only of buttons becomes a button row.
    """
    if weight == 700 and size <= 14 and color in (ACCENT, GOLD) and "<" not in text and "text-align:center" not in extra:
        return hand(text, 21, GOLD_INK if color == ACCENT else GOLD, margin)
    if _PILLS_ONLY.match(text):
        pills = re.findall(r'<a class="os-pill.*?</a>', text)
        return f'<div style="margin:{margin};">' + "".join(pills) + '</div>'
    classes = " ".join(c for c in [CLASS_FOR.get(color, ""), cls] if c)
    if weight == 700 and size >= 15:   # titles: Outfit 600, one shorthand keeps the email light
        fnt = f"font:600 {size}px/{lh}px {DISPLAY};"
    else:
        fnt = f"font-size:{size}px;line-height:{lh}px;" + (f"font-weight:{weight};" if weight != 400 else "")
    return f'<p class="{classes}" style="margin:{margin};{fnt}color:{color};{extra}">{text}</p>'


def pill(href, label, kind="ghost", margin="8px 8px 0 0", small=False, nowrap=True):
    """Site buttons: ghost (paper, navy outline on a navy edge), gold (.btn), phone (brick-soft,
    like Urgent Help) and dark (gold outline on navy)."""
    pad = "3px 11px" if small else "6px 15px"
    fs = "600 14px/18px" if not small else "600 14px/18px"
    ws = "" if nowrap else "white-space:normal;"
    if kind == "dark":
        cls, st = "os-gold", f"border:2px solid {GOLD};color:{GOLD};"
    elif kind == "gold":
        cls, st = "os-ink", f"background-color:{GOLD};border:2px solid {GOLD};border-bottom:4px solid {GOLD_DEEP};color:{INK};"
    elif kind == "phone":
        cls, st = "os-brick", f"background-color:{BLUSH};border:2px solid {BLUSH};border-bottom:4px solid #e2bba4;color:{BRICK_INK};"
    else:
        cls, st = "os-ink", f"background-color:{WHITE};border:2px solid {INK};border-bottom-width:4px;color:{INK};"
    return (f'<a class="os-pill {cls}" href="{href}" style="display:inline-block;margin:{margin};padding:{pad};'
            f'border-radius:99px;font:{fs} {DISPLAY};text-decoration:none;{ws}{st}">{label}</a>')


def pill_row(links, margin="4px 0 0 0", on_dark=False, kind=None):
    k = kind or ("dark" if on_dark else "ghost")
    return f'<div style="margin:{margin};">' + "".join(pill(h, lab, k) for h, lab in links) + '</div>'


def b(text, color=INK):
    return f'<b class="{CLASS_FOR.get(color, "")}" style="color:{color};font-weight:700;">{text}</b>'


def a(href, label, nowrap=True):
    """Taylor: no word links. Every link is a button, even inside a sentence."""
    return pill(href, label, margin="2px 0", small=True, nowrap=nowrap)


def navy_a(href, label, nowrap=True):
    return pill(href, label, "dark", margin="8px 8px 0 0", nowrap=nowrap)


def tel(number_display, number_tel):
    return pill(f"tel:{number_tel}", f'<span style="font-size:9px;vertical-align:1px;">&#9679;</span>&nbsp;{number_display}',
                "phone", margin="2px 0", small=True)


def sp(h):
    return f'<tr><td style="font-size:0;line-height:0;height:{h}px;">&nbsp;</td></tr>'


def major_sp():
    """52px desktop / 40px mobile between sections (.os-sec)."""
    return '<tr><td class="os-sec" style="font-size:0;line-height:52px;height:52px;">&nbsp;</td></tr>'


def padrow(inner, pad="0 34px"):
    return f'<tr><td class="os-pad" align="left" style="padding:{pad};">{inner}</td></tr>'


def fullrow(inner):
    """Edge-to-edge picture across the 600px email (bunting, landscapes, footer hills)."""
    return f'<tr><td style="padding:0;font-size:0;line-height:0;">{inner}</td></tr>'


def anchor(id_):
    return f'<a id="{id_}" name="{id_}" style="display:block;height:0;line-height:0;font-size:0;">&nbsp;</a>'


def h2(title, margin="4px 0 0 0", size=30, lh=35, align="left", color=INK):
    al = "" if align == "left" else f"text-align:{align};"
    return (f'<h2 class="os-h2 {CLASS_FOR.get(color, "")}" style="margin:{margin};font:600 {size}px/{lh}px {DISPLAY};'
            f'color:{color};letter-spacing:-0.5px;{al}">{title}</h2>')


def section_head(id_, title, intro=None, eyebrow=None):
    out = anchor(id_) + (hand(eyebrow) if eyebrow else "") + h2(title, "2px 0 0 0" if eyebrow else "0")
    if intro:
        out += p(intro, 16, 24, BODY, 400, margin="6px 0 0 0")
    return padrow(out)


def card(inner, pad="16px 20px 16px 20px", bg=WHITE, radius="20px", cls=""):
    return table(f'<tr class="os-card-body"><td class="os-cardpad" align="left" style="padding:{pad};">{inner}</td></tr>',
                 bg, f"border-radius:{radius};", f"os-card os-sh {cls}".strip())


def paper(inner, pad="18px 22px", bg=NOTE, radius="8px", cls="", top="", bottom=""):
    """A sheet of the site's paper (newsletter.css .nl-item): soft brown shadow, small radius."""
    return table(top + f'<tr><td class="os-cardpad" align="left" style="padding:{pad};">{inner}</td></tr>' + bottom,
                 bg, f"border-radius:{radius};", f"os-card os-psh {cls}".strip())


def top_bar(label, view_href):
    """The site's navy top bar: a line of words and one gold button."""
    return table(f'<tr><td align="center" style="padding:9px 12px;font:600 14px/22px {DISPLAY};color:{SAND};">'
                 f'<span class="os-sand">{label}</span>&nbsp;&nbsp; '
                 f'<a class="os-ink" href="{view_href}" style="display:inline-block;padding:3px 14px;border-radius:99px;'
                 f'background-color:{GOLD};color:{INK};font:600 13px/18px {DISPLAY};text-decoration:none;white-space:nowrap;">'
                 'View in browser</a></td></tr>', INK, "border-radius:14px;", "os-navy")


def masthead(mark_src):
    """Site header lockup: pin mark + Outfit wordmark, centered."""
    return (f'<table {T} align="center" style="border-collapse:collapse;margin:0 auto;"><tr>'
            f'<td style="padding:0 10px 0 0;vertical-align:middle;">{img(mark_src, 40, "", 40, fluid=False)}</td>'
            f'<td class="os-ink os-mast-word" style="vertical-align:middle;font:600 22px/26px {DISPLAY};color:{INK};letter-spacing:-0.2px;white-space:nowrap;">'
            'Our Special Village</td></tr></table>')


def site_header(art, site):
    """The site header: pin and wordmark on the left, the brick Urgent Help button on the right."""
    urgent = (f'<a class="os-pill os-brick" href="{site}/crisis" style="display:inline-block;padding:6px 14px;border-radius:99px;'
              f'background-color:{BLUSH};border:1px solid #e2bba4;color:{BRICK_INK};font:600 14px/18px {DISPLAY};text-decoration:none;">'
              f'<span style="color:{ACCENT};font-size:10px;vertical-align:1px;">&#9679;</span>&nbsp; Urgent Help</a>')
    return (f'<table {T} width="100%" style="width:100%;"><tr>'
            f'<td valign="middle">{masthead(art("osv-mark-80.png"))}</td>'
            f'<td align="right" valign="middle">{urgent}</td></tr></table>')


SKY_FALLBACK = {"fall": "#f3e2c8", "winter": "#efe1d0"}


def hero(art, title_html, season="fall",
         place="Murfreesboro &amp; surrounding areas &middot; Tennessee",
         tagline="It takes a village. Welcome to ours.",
         land_alt="Illustration of the village in autumn: homes, neighbors walking the path, and rolling Middle Tennessee hills."):
    """The homepage hero (home.css .home-hero): golden-hour sky, the place line between two gold
    rules, a big title with the gold swash, the handwritten tagline, then the hills and the village."""
    sky, bg = art("hero-sky.jpg"), SKY_FALLBACK.get(season, "#f3e2c8")
    rule_td = f'<td class="os-hrule" width="26" style="width:26px;"><div style="height:2px;background-color:{GOLD};border-radius:2px;font-size:0;line-height:0;">&nbsp;</div></td>'
    place_row = (f'<table {T} align="center" style="margin:0 auto;"><tr>{rule_td}'
                 f'<td class="os-place" style="padding:0 10px;font:800 12px/16px {FONT};letter-spacing:2px;text-transform:uppercase;color:{GOLD_DARK};text-align:center;">{place}</td>'
                 f'{rule_td}</tr></table>')
    text = (place_row
            + f'<h1 class="os-hero-h1 os-ink" style="margin:14px 0 0 0;font:600 46px/48px {DISPLAY};color:{INK};letter-spacing:-1.4px;text-align:center;">{title_html}</h1>'
            + f'<p class="os-hand os-ink os-tagline" style="margin:10px 0 0 0;font:400 28px/32px {HAND};color:{INK};text-align:center;">{tagline}</p>'
            + f'<div style="margin:0 0 4px 0;line-height:0;font-size:0;text-align:center;">'
              f'<img src="{art(DECOR + "swoosh.png")}" width="150" height="14" alt="" style="display:inline-block;width:150px;height:14px;border:0;"></div>')
    return (f'<tr><td class="os-hero-sky os-pad" align="center" bgcolor="{bg}" background="{sky}" '
            f"style=\"background-color:{bg};background-image:url('{sky}');background-size:100% 100%;background-position:center bottom;"
            f'background-repeat:no-repeat;border-radius:28px 28px 0 0;padding:30px 24px 6px 24px;">{text}</td></tr>'
            + fullrow(img(art("hero-land.jpg"), 600, land_alt, style="max-width:none;", cls="os-hero")))


def dusk_band(art, id_, eyebrow, title, inner):
    """The homepage's dusk (home.css .dusk): sunset over the lamp-lit village, a starry navy night
    holding the section, and the wave back to cream."""
    stars = art(DECOR + "stars.png")
    return (fullrow(img(art(DECOR + "dusk-top.png"), 600, "", style="max-width:none;"))
            + f'<tr><td class="os-navy os-pad" bgcolor="{NAVY_DEEP}" background="{stars}" '
              f"style=\"background-color:{NAVY_DEEP};background-image:url('{stars}');background-repeat:repeat;padding:4px 34px 30px 34px;\">"
            + anchor(id_) + hand(eyebrow, 22, GOLD, "0")
            + h2(title, "2px 0 18px 0", color=WHITE)
            + inner + '</td></tr>'
            + fullrow(img(art(DECOR + "dusk-wave.png"), 600, "", style="max-width:none;")))


def letter(art, h1_text, paras_html, name="Dr. Taylor Hickok", cred="Founder &middot; SLP &middot; AuDHD parent"):
    """Taylor's note as the site's stamped, postmarked airmail letter (newsletter.css .nl-card)."""
    byline = (f'<table {T} style="border-collapse:collapse;"><tr>'
              f'<td style="padding:0 12px 0 0;vertical-align:middle;">'
              f'<img class="os-intro-photo" src="{art("taylor-hickok-160.jpg")}" width="68" height="68" alt="Dr. Taylor Hickok, founder of Our Special Village." '
              f'style="display:block;width:68px;height:68px;border:3px solid #ffffff;border-radius:50%;"></td>'
              f'<td style="vertical-align:middle;">'
              + p(name, 16, 20, INK, 700)
              + p(cred, 13, 18, MUTED, 400, margin="2px 0 0 0", extra="white-space:nowrap;", cls="os-cred")
              + '</td></tr></table>')
    head_row = (f'<table {T} width="100%" style="width:100%;border-collapse:collapse;"><tr>'
                f'<td valign="middle" style="vertical-align:middle;">{byline}</td>'
                f'<td class="os-stamp" width="112" align="right" valign="top" style="width:112px;vertical-align:top;line-height:0;">'
                f'{img(art(DECOR + "stamp.png"), 112, "", 88, fluid=False)}</td></tr></table>')
    title = (f'<h1 class="os-h1 os-ink" style="margin:12px 0 12px 0;font:600 34px/38px {DISPLAY};'
             f'color:{INK};letter-spacing:-0.8px;">{h1_text}</h1>') if h1_text else '<div style="height:14px;font-size:0;line-height:0;">&nbsp;</div>'
    body = (head_row
            + title
            + paras_html
            + p("With love,", 16, 24, BODY, 400, margin="12px 0 2px 0")
            + f'<img class="os-sig" src="{art("signature-taylor.png")}" width="96" height="55" alt="Taylor" '
              f'style="display:block;width:96px;height:auto;margin:0 0 0 8px;border:0;font:italic 22px Georgia,serif;color:{ACCENT};">')
    edge = lambda f, r: (f'<tr><td style="padding:0;font-size:0;line-height:0;">'
                         f'{img(art(DECOR + f), 532, "", style=f"max-width:100%;border-radius:{r};")}</td></tr>')
    return paper(body, "18px 24px 18px 24px", NOTE, "8px", top=edge("airmail-top.png", "8px 8px 0 0"),
                 bottom=edge("airmail-bottom.png", "0 0 8px 8px"))


def stops_block(art, chips):
    """In this issue: the site's "Stay connected" stops, Taylor's pictograms on the painted path."""
    cells = "".join(
        f'<td class="os-stop" width="25%" valign="top" align="center" style="width:25%;vertical-align:top;">'
        f'<a href="{href}" style="display:block;text-decoration:none;color:{INK};">'
        f'{img(art(f"stop-{i + 1}.png"), 133, "", style="width:100%;max-width:none;")}'
        f'<span class="os-stoplabel os-ink" style="display:block;padding:2px 4px 0;font:600 15px/19px {DISPLAY};color:{INK};">{label}</span></a></td>'
        for i, (href, label) in enumerate(chips))
    return (hand("In this issue", 22, GOLD_INK, "0 0 2px 0", "center")
            + f'<table {T} class="os-stops" width="100%" style="width:100%;border-collapse:collapse;table-layout:fixed;"><tr>{cells}</tr></table>')


def tag_card(art, inner):
    """Deadline watch as the site's paper tag, eyelet and string at the top."""
    top = (f'<tr><td align="right" style="padding:0 20px 0 0;font-size:0;line-height:0;">'
           f'{img(art(DECOR + "tag-eyelet.png"), 30, "", 42, fluid=False, style="display:inline-block;")}</td></tr>')
    return paper(inner, "0 20px 8px 20px", BLUSH, "8px 36px 8px 8px", top=top)


def fact_pills(first, rest):
    """The site's hero fact pills: a navy one with a gold dot, then paper ones."""
    base = f"display:inline-block;margin:0 6px 8px 0;padding:6px 14px;border-radius:99px;font:600 14px/18px {DISPLAY};"
    out = (f'<span class="os-white" style="{base}background-color:{INK};color:{WHITE};border-bottom:3px solid {NAVY_DEEP};">'
           f'<span style="color:{GOLD};font-size:10px;vertical-align:1px;">&#9679;</span>&nbsp; {first}</span>')
    for r in rest:
        out += f'<span class="os-ink" style="{base}background-color:{WHITE};color:{INK};border:1px solid #d6d9df;">{r}</span>'
    return f'<div style="margin:0;">{out}</div>'


def board(art, inner, pad="22px 16px 20px 16px"):
    """Cork notice board with the gold frame (village-hall.css .vh-board, hope.css .hw-board)."""
    cork = art(DECOR + "cork.png")
    inside = table(f'<tr><td class="os-boardpad" align="left" style="padding:{pad};">{inner}</td></tr>', CORK,
                   f"background-image:url('{cork}');border-radius:20px;", "os-board", attrs=f' background="{cork}"')
    return table(f'<tr><td style="padding:9px;">{inside}</td></tr>', CORK_FRAME,
                 f"border:3px solid {CORK_EDGE};border-radius:30px;", "os-sh")


def pins_row(art, left="pin-brick.png", right=None, center=False):
    if center:
        return (f'<tr><td align="center" style="padding:8px 0 0 0;font-size:0;line-height:0;">'
                f'{img(art(DECOR + left), 32, "", 34, fluid=False, style="display:inline-block;")}</td></tr>')
    r = (f'<td align="right">{img(art(DECOR + right), 32, "", 34, fluid=False, style="display:inline-block;")}</td>' if right else "")
    return (f'<tr><td style="padding:6px 12px 0 12px;font-size:0;line-height:0;"><table {T} width="100%" style="width:100%;border-collapse:collapse;"><tr>'
            f'<td align="left">{img(art(DECOR + left), 32, "", 34, fluid=False, style="display:inline-block;")}</td>{r}</tr></table></td></tr>')


def dashed(margin="16px 0 14px 0", color="#eadcb4"):
    return f'<div style="margin:{margin};border-top:2px dashed {color};font-size:0;line-height:0;height:0;"></div>'


def guest_block(g, art, first=True, photo_src=None, placeholder=None):
    """One guest on the Village Hall poster: name, organisation, taped photo, bio, buttons."""
    if photo_src:
        photo = img(photo_src, 170, g.get("photo_alt", ""), style="margin:0 auto;", cls="os-guestphoto")
    else:
        photo = table(f'<tr><td align="center" valign="middle" style="height:190px;padding:6px;">'
                      f'{placeholder or ""}</td></tr>', "#fff1b8", "border:1px dashed #b8912f;border-radius:6px;",
                      width="150", attrs=' align="center"')
    links = g.get("links") or []
    return ((dashed("18px 0 16px 0") if not first else "")
            + f'<p class="os-ink os-vh-guestname" style="margin:0;font:600 25px/29px {DISPLAY};color:{INK};letter-spacing:-0.4px;">{g["name"]}</p>'
            + f'<p class="os-vh-guestrole" style="margin:4px 0 12px 0;font:500 16px/21px {DISPLAY};color:{BLUE_INK};">{g["role"]}</p>'
            + f'<table {T} class="os-vh-guest" width="100%" style="width:100%;border-collapse:collapse;"><tr>'
            f'<td class="os-col os-col-photo" width="170" valign="top" style="width:170px;vertical-align:top;padding:0 14px 0 0;">{photo}</td>'
            f'<td class="os-col os-vh-guestblurb" valign="top" style="vertical-align:top;">'
            + p(g["bio"], 15, 23, BODY, 400)
            + (f'<div class="os-vh-contact" style="margin:6px 0 0 0;">' + "".join(pill(h, lab, nowrap=False) for h, lab in links) + '</div>' if links else "")
            + '</td></tr></table>')


def poster(art, eyebrow, topic, guests_html, about):
    """This month's guest pinned to the notice board (village-hall.css .vh-poster)."""
    inner = (hand(eyebrow)
             + table(f'<tr><td class="os-ink" style="padding:12px 16px;font:600 19px/25px {DISPLAY};color:{INK};">{topic}</td></tr>',
                     GOLD_SOFT, "border-radius:12px;margin:6px 0 18px 0;")
             + guests_html
             + dashed()
             + p(about, 15, 23, INK, 700, extra="font-family:inherit;font-weight:700;"))
    return paper(inner, "0 22px 22px 22px", WHITE, "6px", "os-tl", top=pins_row(art, "pin-brick.png", "pin-gold.png"))


def ticket(art, button_html, bottom_html):
    """Register and pay as the site's evening ticket (group.css .grp-ticket): notches and a tear line."""
    notch = lambda f: (f'<td width="16" style="width:16px;font-size:0;line-height:0;">'
                       f'{img(art(DECOR + f), 16, "", 32, fluid=False)}</td>')
    tear = (f'<tr>{notch("notch-l.png")}<td valign="middle" style="vertical-align:middle;padding:0 6px;">'
            f'<div style="border-top:3px dashed #666e7e;height:0;font-size:0;line-height:0;"></div></td>{notch("notch-r.png")}</tr>')
    return table(f'<tr><td colspan="3" align="center" style="padding:24px 22px 18px 22px;">{button_html}</td></tr>'
                 + tear
                 + f'<tr><td colspan="3" class="os-cardpad" style="padding:16px 22px 22px 22px;">{bottom_html}</td></tr>',
                 INK, "border-radius:26px;", "os-navy os-tsh")


def calendar_page(art, inner):
    """The month ahead as the site's calendar page: navy band with gold binding rings."""
    return table(f'<tr><td style="padding:0;font-size:0;line-height:0;">{img(art(DECOR + "calendar-top.png"), 532, "", style="max-width:100%;")}</td></tr>'
                 f'<tr><td class="os-cardpad os-psh" bgcolor="{NOTE}" style="background-color:{NOTE};border-radius:0 0 8px 8px;padding:2px 18px 6px 18px;">{inner}</td></tr>',
                 cls="os-cal")


BOOK_COLORS = [("gold", GOLD), ("blue", "#8fa5c6"), ("brick", ACCENT), ("sage", SAGE)]


def book(art, label, art_html, rest, n=0):
    """A library guide as a book on the homepage shelf (home.css .book): coloured spine,
    matching ribbon, and a wooden shelf under it."""
    name, color = BOOK_COLORS[n % len(BOOK_COLORS)]
    head = (f'<table {T} width="100%" style="width:100%;"><tr>'
            f'<td valign="bottom" style="padding:12px 8px 8px 0;">{hand(label, 20)}</td>'
            f'<td width="14" align="right" valign="top" style="width:14px;line-height:0;">'
            f'{img(art(DECOR + f"ribbon-{name}.png"), 14, "", 34, fluid=False)}</td></tr></table>')
    return (table(f'<tr class="os-card-body"><td class="os-cardpad" align="left" style="padding:0 16px 16px 16px;">{head}{art_html}{rest}</td></tr>',
                  NOTE, f"border-radius:6px 16px 16px 6px;border-left:16px solid {color};", "os-card os-psh")
            + shelf())


def shelf():
    return (f'<div class="os-shelf" style="margin:12px 0 0 0;height:9px;background-color:{CORK_FRAME};'
            f'border-bottom:4px solid #9d7128;border-radius:3px;font-size:0;line-height:0;">&nbsp;</div>')


def story_note(art, eyebrow, title, photo_html, paras_html, byline):
    """The hopeful story pinned to the Wall of Hope board (hope.css .hope-story)."""
    inner = (hand(eyebrow)
             + f'<p class="os-ink" style="margin:2px 0 0 0;font:600 27px/32px {DISPLAY};color:{INK};letter-spacing:-0.5px;">{title}</p>'
             + (f'<div style="margin:14px 0 8px 0;text-align:center;">{photo_html}</div>' if photo_html else "")
             + paras_html
             + hand(byline, 25, GOLD_INK, "14px 0 0 0"))
    fold = (f'<tr><td align="right" style="padding:6px 0 0 0;font-size:0;line-height:0;">'
            f'{img(art(DECOR + "fold.png"), 34, "", 34, fluid=False, style="display:inline-block;border-radius:0 0 6px 0;")}</td></tr>')
    return paper(inner, "4px 24px 0 24px", NOTE, "6px", "os-tl", top=pins_row(art, center=True), bottom=fold)


def share_note(title, text, button_html):
    """The dashed "add yours" note from the Wall of Hope board."""
    plus = table(f'<tr><td align="center" class="os-white" style="height:32px;font:700 22px/32px {DISPLAY};color:#ffffff;">+</td></tr>',
                 GOLD_DEEP, "border-radius:16px;", width="32", attrs=' align="center"')
    inner = table(f'<tr><td align="center" style="padding:16px 16px 18px 16px;text-align:center;">'
                  + plus + hand(title, 24, INK, "8px 0 0 0", "center")
                  + p(text, 15, 22, BODY, 400, margin="6px 0 0 0", extra="text-align:center;")
                  + f'<div style="margin:6px 0 0 0;">{button_html}</div></td></tr>', None,
                  "border:2px dashed #c8b07a;border-radius:4px;")
    return paper(inner, "8px", NOTE, "4px", "os-tr")


def index_card(art, head_html, ruled_html, foot_html):
    """One question, answered as the site's index card: red header line, blue rules, a "?"."""
    ruled = art(DECOR + "ruled.png")
    return table(f'<tr><td class="os-cardpad" style="padding:18px 22px 14px 22px;">{head_html}</td></tr>'
                 f'<tr><td class="os-cardpad os-ruled" bgcolor="{NOTE}" background="{ruled}" '
                 f"style=\"background-color:{NOTE};background-image:url('{ruled}');border-top:2px solid #d8b19d;padding:0 22px 0 22px;\">{ruled_html}</td></tr>"
                 f'<tr><td class="os-cardpad" style="padding:14px 22px 16px 22px;">{foot_html}</td></tr>',
                 NOTE, "border-radius:8px;", "os-card os-psh")


def question_mark():
    return (f'<td width="30" align="right" valign="top" class="os-tr os-blue" style="width:30px;vertical-align:top;'
            f'font:400 40px/40px {HAND};color:{BLUE_INK};">?</td>')


def rows_table(rows_html):
    return (f'<table {T} width="100%" style="width:100%;border-collapse:collapse;">' + "".join(rows_html) + '</table>')


def row(chip_html, content_html, last=False, featured=False, tight=False, line=RULE):
    border = "" if last else f"border-bottom:1px solid {line};"
    return (f'<tr><td class="os-rule" style="padding:14px 0;{border}">'
            f'<table {T} width="100%" style="width:100%;border-collapse:collapse;">'
            f'<tr><td width="62" style="width:62px;vertical-align:top;padding:0 12px 0 0;">{chip_html}</td>'
            f'<td style="vertical-align:top;">{content_html}</td></tr></table></td></tr>')


_MONTH_ABBR = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
_NON_OCT_MONTHS = tuple(m for m in _MONTH_ABBR if m != "Oct")
_LEADING_DASHES = ("&ndash;", "&mdash;", "–", "—", "-")


def format_chip_range_end(label):
    """Calendar-tile secondary date line. Keep one line via nbsp.

    T382 / T367 §4: never show a leading en-dash or hyphen before a
    non-October month (Nov, Dec, Jan, …). Mid-range dashes in body copy
    (5:00–9:00 PM, Oct 15–Dec 7) are unrelated and stay put.
    """
    if not isinstance(label, str):
        return label
    text = label[3:] if label.startswith("to ") else label
    for prefix in _LEADING_DASHES:
        if text.startswith(prefix):
            rest = text[len(prefix):].lstrip()
            month = rest.replace("&nbsp;", " ").split()[0] if rest else ""
            if month in _NON_OCT_MONTHS:
                text = rest
            break
    if " " in text and "&nbsp;" not in text:
        text = text.replace(" ", "&nbsp;")
    return text


def chip(top, big=None, bottom=None, year=False):
    """Calendar page like the site's event pins: navy weekday band, big Outfit day, gold month."""
    nw = ""  # .os-chip td keeps each line on one line (see head())
    shell = (f'<table {T} class="os-chip" width="62" bgcolor="#ffffff" style="width:62px;border-collapse:separate;'
             f'background-color:#ffffff;border:2px solid {INK};border-radius:12px;">')
    band = (f'<tr><td class="os-navy" align="center" bgcolor="{INK}" style="background-color:{INK};padding:3px 2px 2px 2px;'
            f'border-radius:9px 9px 0 0;font:600 11px/14px {DISPLAY};letter-spacing:1px;text-transform:uppercase;color:{GOLD};{nw}">{top}</td></tr>')
    if big is None:
        return (shell + band + f'<tr><td align="center" style="padding:8px 2px 9px 2px;font:600 13px/17px {DISPLAY};color:{INK};{nw}">'
                f'{bottom}</td></tr></table>')
    bottom = format_chip_range_end(bottom)
    bs = 10 if "&ndash;" in (bottom or "") or "&nbsp;" in (bottom or "") else 11
    return (shell + band
            + f'<tr><td align="center" style="padding:3px 2px 0 2px;font:600 24px/27px {DISPLAY};color:{INK};{nw}">{big}</td></tr>'
            f'<tr><td align="center" style="padding:0 2px 5px 2px;font:600 {bs}px/14px {DISPLAY};letter-spacing:.8px;'
            f'text-transform:uppercase;color:{GOLD_DARK};{nw}">{bottom}</td></tr></table>')


def item(title, lines, featured=False, label=None, first=True):
    out = ""
    if label:
        out += p(label, 13, 18, ACCENT, 700, margin=("0 0 4px 0" if first else "14px 0 4px 0"))
        tmargin = "0"
    else:
        tmargin = "0" if first else "14px 0 0 0"
    tsize, tlh = (18, 25) if featured else (16, 23)
    out += p(title, tsize, tlh, INK, 700, margin=tmargin, extra="")
    bsize, blh = (16, 24) if featured else (15, 22)
    for ln in lines:
        out += p(ln, bsize, blh, BODY, 400, margin="4px 0 0 0")
    return out


def button(href, label, fill, text_color, align="left"):
    """The site's .btn: a pill sitting on a darker edge."""
    align_attr = f' align="{align}"' if align != "left" else ""
    margin = "margin:0 auto;" if align == "center" else ""
    edge = GOLD_DEEP if fill == GOLD else NAVY_DEEP
    kind = "os-btn-gold" if fill == GOLD else "os-btn-navy"
    return (f'<table {T} class="os-btn {kind}"{align_attr} bgcolor="{fill}" style="border-collapse:separate;background-color:{fill};'
            f'border-radius:999px;border-bottom:4px solid {edge};{margin}">'
            f'<tr><td align="center" style="padding:13px 28px 12px 28px;">'
            f'<a href="{href}" style="display:block;font:600 17px/20px {DISPLAY};color:{text_color};text-decoration:none;">{label}</a></td></tr></table>')


def secondary_tags_text(parts):
    """Small sage tag: ONLINE · WEEKLY · FREE."""
    return (f'<p style="margin:0 0 8px 0;"><span style="display:inline-block;padding:3px 9px;border-radius:6px;'
            f'background-color:{SAGE_SOFT};font-size:11px;line-height:14px;color:{SAGE_INK};font-weight:800;letter-spacing:0.8px;">'
            + " &middot; ".join(parts) + '</span></p>')


def good_to_know(items):
    """Checklist with the site's round check marks."""
    rows = "".join(
        f'<tr><td valign="top" style="width:26px;padding:1px 8px {"0" if i == len(items) - 1 else "8px"} 0;vertical-align:top;">'
        f'<span style="display:inline-block;width:18px;height:18px;border-radius:9px;background-color:{SAGE_SOFT};color:{SAGE_INK};'
        f'font:800 11px/18px Arial,sans-serif;text-align:center;">&#10003;</span></td>'
        f'<td valign="top" style="padding:0 0 {"0" if i == len(items) - 1 else "8px"} 0;vertical-align:top;">{p(t, 15, 22, BODY, 400)}</td></tr>'
        for i, t in enumerate(items))
    return (f'<table {T} width="100%" style="width:100%;border-collapse:collapse;margin:14px 0 0 0;">'
            f'<tr><td style="padding:12px 0 0 0;border-top:2px dashed #eadcb4;">'
            + p("Good to know", 15, 22, INK, 700, margin="0 0 8px 0")
            + f'<table {T} width="100%" style="width:100%;border-collapse:collapse;">{rows}</table></td></tr></table>')


def group_cta(href, label):
    """Full-width navy button (site .btn in navy)."""
    return (f'<table {T} class="os-btn os-btn-navy" width="100%" bgcolor="{INK}" style="width:100%;border-collapse:separate;'
            f'background-color:{INK};border-radius:999px;border-bottom:4px solid {NAVY_DEEP};">'
            f'<tr><td align="center" style="padding:13px 18px 12px 18px;">'
            f'<a href="{href}" style="display:block;font:600 17px/20px {DISPLAY};color:{CREAM};text-decoration:none;text-align:center;">{label}</a></td></tr></table>')


def group_card(badges, name, meta_pairs, blurb, good_items, btn_href, btn_label,
               audience=None, secondary=None, cost_note=None, art=None, tilt="os-tl"):
    """Support group as a taped note: tag, name, the site's fact pills, blurb, checklist, button."""
    head = secondary_tags_text(secondary) if secondary else ""
    labels = [lab for _, lab in meta_pairs]
    inner = (head
             + p(name, 19, 25, INK, 700, margin="0 0 10px 0")
             + fact_pills(labels[0], labels[1:])
             + p(blurb, 15, 23, BODY, 400, margin="6px 0 0 0")
             + good_to_know(good_items)
             + '<div class="os-card-cta os-sg-cta" style="margin:20px 0 0 0;">' + group_cta(btn_href, btn_label) + '</div>')
    top = (f'<tr><td align="center" style="padding:0;font-size:0;line-height:0;">'
           f'{img(art(DECOR + "tape-cream.png"), 100, "", 35, fluid=False, style="display:inline-block;")}</td></tr>') if art else ""
    return paper(inner, "4px 18px 18px 18px", NOTE, "8px", tilt, top=top)


def browser_cols(*pieces, gap=16):
    """Stacked in email and on phones; side by side only in the wide browser view."""
    items = "".join(
        f'<div class="os-browser-col" style="display:block;width:100%;margin:{"0" if i == len(pieces) - 1 else f"0 0 {gap}px 0"};'
        f'vertical-align:top;box-sizing:border-box;">{piece}</div>' for i, piece in enumerate(pieces))
    return f'<div class="os-browser-cols" style="display:block;width:100%;">{items}</div>'


def story_img(src, width, alt, radius=12, link=None, extra_style=""):
    im = img(src, width, alt, style=f"border-radius:{radius}px;{extra_style}")
    return f'<a href="{link}" style="display:block;text-decoration:none;">{im}</a>' if link else im


def step(n, text, last=False, ruled=True):
    """Numbered step. On the index card each line sits on a 28px ruled line."""
    pad = "0" if (last or ruled) else "0 0 12px 0"
    lh = 28 if ruled else 24
    return (f'<tr><td style="padding:{pad};"><table {T} width="100%" style="width:100%;border-collapse:collapse;"><tr>'
            f'<td width="30" style="width:30px;vertical-align:top;padding:1px 10px 0 0;">'
            f'<table {T} class="os-stepbg" width="26" bgcolor="{GOLD}" style="width:26px;border-collapse:separate;background-color:{GOLD};border-radius:13px;"><tr>'
            f'<td align="center" style="padding:0;height:26px;font:600 14px/26px {DISPLAY};color:{INK};">{n}</td></tr></table></td>'
            f'<td style="vertical-align:top;">{p(text, 16, lh, BODY, 400)}</td></tr></table></td></tr>')


def free_note():
    """October's Village Hall is free (Taylor, Oct 1): no pay-what-you-can boxes."""
    heading = p("Free for every family", 17, 22, WHITE, 700, extra="text-align:center;")
    support = p("Our first Village Hall is free. Register to save your seat.",
                13, 19, SAND, 400, margin="6px 0 0 0", extra="text-align:center;", cls="os-pay-note")
    note = p("The meeting link is emailed to registrants.", 12, 18, ON_DARK_MUTED, 400, margin="12px 0 0 0", extra="text-align:center;")
    return heading + support + note


def price_boxes():
    """Choose what you can pay: four boxes (2x2 on phones)."""
    boxes = [("$0", "Welcome"), ("$10", "Helps"), ("$20", "Suggested"), ("$35", "Pay it forward")]
    cells = []
    for i, (amt, label) in enumerate(boxes):
        pad = "0 5px 0 0" if i == 0 else ("0 0 0 5px" if i == 3 else "0 5px")
        inner = table(f'<tr><td class="os-paybox" align="center" valign="middle" style="padding:7px 4px;vertical-align:middle;">'
                      + p(amt, 18, 21, INK, 700, extra="text-align:center;")
                      + p(label, 11, 14, BODY, 400, margin="2px 0 0 0", extra="text-align:center;")
                      + '</td></tr>', BLUE_SOFT, "border-radius:10px;border-bottom:3px solid #b9c4d8;", "os-paybox")
        cells.append(f'<td class="os-paycell" width="25%" valign="middle" style="width:25%;padding:{pad};vertical-align:middle;">{inner}</td>')
    heading = p("Choose what you can pay", 17, 22, WHITE, 700, extra="text-align:center;")
    support = p("Every family is welcome&ndash;choose $0, or give more to help cover another seat.",
                13, 19, SAND, 400, margin="6px 0 0 0", extra="text-align:center;", cls="os-pay-note")
    grid = (f'<table {T} class="os-paygrid" width="100%" style="width:100%;border-collapse:separate;margin:12px 0 0 0;table-layout:fixed;"><tr>'
            + "".join(cells) + '</tr></table>')
    note = p("The meeting link is emailed to registrants.", 12, 18, ON_DARK_MUTED, 400, margin="12px 0 0 0", extra="text-align:center;")
    return f'<div class="os-pay-wrap" style="width:100%;">{heading}{support}{grid}</div>' + note


def disclose(lines):
    """Extra event lines, always shown: expanders don't open in Outlook or Gmail."""
    return list(lines)


def about_card(art, about_text, links):
    """About the Village: a taped family snapshot beside the words."""
    photo = img(art(DECOR + "about-print.jpg"), 190, "Taylor, her husband, and their daughter at a bowling alley.",
                style="margin:0 auto;", cls="os-aboutphoto")
    words = (h2("About Our Special Village", "0", 22, 27)
             + p(about_text, 15, 23, BODY, 400, margin="8px 0 0 0")
             + pill_row(links, margin="6px 0 0 0"))
    body = (f'<table {T} width="100%" style="width:100%;border-collapse:collapse;"><tr>'
            f'<td class="os-col os-col-photo" width="190" valign="middle" style="width:190px;vertical-align:middle;padding:0 12px 0 0;">{photo}</td>'
            f'<td class="os-col" valign="middle" style="vertical-align:middle;">{words}</td></tr></table>')
    return paper(body, "8px 20px 18px 12px", WHITE, "20px")


def numbers_card(art, lines):
    """Numbers worth keeping on a pinned note (hope.css .nl-item--note colour)."""
    inner = hand("Numbers worth keeping", 23, GOLD_INK, "0 0 6px 0") + "".join(p(t, 15, 26, BODY, 400, margin="6px 0 0 0") for t in lines)
    return paper(inner, "2px 22px 18px 22px", "#fbf0cf", "4px", "os-tr", top=pins_row(art, "pin-blue.png", center=True))


def forward_line(site):
    return (p("Know a family who could use this? Forward it along. Anyone can join at", 15, 22, BODY, 400,
              extra="text-align:center;")
            + f'<div style="margin:6px 0 0 0;text-align:center;">{pill(f"{site}/newsletter", "ourspecialvillagetn.com/newsletter", "gold", "4px 0 0 0")}</div>')


def footer_rows(art, site, unsub_href):
    """The site's footer under its dusk hills: navy, the pin in a paper circle, gold buttons."""
    brand = (f'<table {T} style="border-collapse:collapse;"><tr>'
             f'<td style="padding:0 10px 0 0;vertical-align:middle;">'
             f'<img src="{art("osv-mark-80.png")}" width="44" height="44" alt="" style="display:block;width:44px;height:44px;border:0;'
             f'border-radius:22px;background-color:{WHITE};"></td>'
             f'<td class="os-white" style="vertical-align:middle;font:600 21px/24px {DISPLAY};color:{WHITE};white-space:nowrap;">Our Special Village</td></tr></table>')
    inner = (brand
             + p("Our Special Village &middot; Murfreesboro and surrounding areas, Tennessee", 14, 21, WHITE, 700, margin="14px 0 6px 0",
                 extra="font-family:inherit;font-weight:700;")
             + p("Local businesses and practices help keep the Village free and ad-free.", 13, 20, ON_DARK_MUTED, 400, cls="os-footnote")
             + pill_row([(f"{site}/sponsors", "Sponsorship options")], "2px 0 14px 0", on_dark=True)
             + p("You are receiving this because you joined the newsletter list at ourspecialvillagetn.com.", 13, 20, ON_DARK_MUTED, 400,
                 cls="os-footnote")
             + pill_row([(unsub_href, "Unsubscribe in one click"), (f"{site}/privacy", "Privacy"), (f"{site}/contact", "Contact")],
                        "2px 0 14px 0", on_dark=True)
             + p("Our Special Village is owned and operated by Little Luminaries Therapy Services, PLLC<br>1810 Ward Dr, Suite 101, Murfreesboro, TN 37129",
                 13, 19, ON_DARK_MUTED, 400, cls="os-footnote"))
    return (fullrow(img(art(DECOR + "foot-hills.png"), 600, "", style="max-width:none;"))
            + f'<tr><td class="os-navy os-pad os-footer" bgcolor="{NAVY_DEEP}" style="background-color:{NAVY_DEEP};'
              f'border-radius:0 0 28px 28px;padding:10px 34px 30px 34px;">{inner}</td></tr>')


SPOOK_ON_SITE = (
    "On site: local resources trunk-or-treat; mobile sensory room; sensory tables "
    "and activities; singing pumpkins and foggy bubbles; food and treats available."
)
SPOOK_THANKS = "Thanks to location sponsors Little Luminaries and Cultivate Play."
SPOOK_DETAILS = [SPOOK_ON_SITE, SPOOK_THANKS]
SPOOK_REG_URL = "https://ticketscandy.com/e/sensory-space-presents-sensory-spooktacular-2026-21025"
# T429 flyer / organizer links. No external page for Gallatin, Caleb's, or Pegram.
GALLATIN_FLYER = f"{SITE}/assets/event-flyers/gallatin-hosa-special-needs-trunk-or-treat-2026.png"
CALEB_FLYER = f"{SITE}/assets/event-flyers/calebs-friends-halloween-party-2026.png"
PEGRAM_FLYER = f"{SITE}/assets/event-flyers/special-needs-family-fall-fest-2026.png"
RECESS_MAIL = "mailto:rebecca.whitaker@ottercreek.org"
DOLLYWOOD_URL = "https://dreamcooperative.com/"
EVERGREEN_URL = "https://evergreenls.org/trunkortreat/"
EVERGREEN_BLURB = "Fun, fellowship, and safe Halloween activities where everyone matters."
WEROCK_HALLOWEEN_URL = "https://ecom.roller.app/werockthespectrummurfreesboro/booknow/en-us/product/2093802?date=2026-10-31"
WEROCK_HALLOWEEN_BLURB = ("Kept inside this year: a sensory-friendly Halloween that&rsquo;s dye-free and stress-free, "
                          "with sensory bins, crafts, games, and pizza.")

# T429 drive times: OSRM from Murfreesboro Public Square, rounded up to 5 minutes.
# Gallatin High School 55.5 -> About 60 min. Dollywood 252.7 -> About 4 hours 15 min.
# Pegram 63.4 -> About 65 min. Otter Creek, Brentwood 40.3 -> About 45 min.
# Antioch 29.2 confirms the existing About 30 min. Heroes Den is in Murfreesboro.

SECONDARY_EVENTS = [
    # T429: first Saturday respite, before Game Day the same afternoon.
    dict(chip=chip("Sat", "3", "Oct"),
         title="rEcess &middot; Otter Creek Church",
         meta="8:00&ndash;11:45 AM &middot; Otter Creek Church, 409 Franklin Road, Brentwood &middot; About 45 min",
         note="Monthly respite with 99 Balloons. Kids and siblings stay for activities while parents step out.",
         link=(RECESS_MAIL, "Reserve a spot")),
    dict(chip=chip("Sat", "3", "Oct"),
         title="Game Day &middot; Autism Tennessee",
         meta="12:00&ndash;3:00 PM &middot; Nashville &middot; Free, food provided &middot; About 45 min",
         sensory="indoor, small-group games for autistic kids, teens, and adults; families welcome.",
         link=("https://autismtn.org/events/EventDetails.aspx?id=2003814", "Register")),
    dict(chip=chip("Oct", "16", "Nov 1"),
         title="Boo at the Zoo &middot; Nashville Zoo",
         meta="Nightly 5:00&ndash;9:00 PM &middot; $19&ndash;$23 ages 2+, parking $10 &middot; About 35 min",
         sensory="free Zooper Packs and a social story; Mon&ndash;Wed quietest.",
         link=("https://www.nashvillezoo.org/boo", "Tickets and social story")),
    # T429: Hickok flyer IMG_9695 (Agents #416). Rain date stays in the meta, not the chip.
    dict(chip=chip("Wed", "21", "Oct"),
         title="Special Needs &amp; Neurodiverse Day at Dollywood &middot; Dream Cooperative",
         meta=("All day &middot; rain date Wed Oct 28 &middot; Dollywood, Pigeon Forge &middot; "
               "$70 per person, due Oct 2 &middot; About 4 hours 15 min"),
         note="RSVP by texting Heidi at (931) 265-5376.",
         link=(DOLLYWOOD_URL, "Details")),
    dict(chip=chip("Thu", "22", "Oct"),
         title="Gallatin HOSA Special Needs Trunk or Treat",
         meta=("4:30&ndash;6:30 PM &middot; Gallatin High School, 700 Dan P. Herron Drive, Gallatin &middot; "
               "About 60 min"),
         note="Touch-A-Truck after treats.",
         link=(GALLATIN_FLYER, "Details")),
    # T400: Sun Oct 25 before Sat Oct 31; Details expands in-place (not /events).
    # T410: free TicketsCandy registration CTA alongside Details.
    # T429: Caleb's Friends is the same Sunday, after the 1:00 PM Spooktacular.
    dict(chip=chip("Sun", "25", "Oct"),
         title="Sensory Spooktacular",
         meta=("1:00&ndash;4:00 PM (sensory-sensitive hour 1:00&ndash;2:00 PM) &middot; "
               "Little Luminaries and Cultivate Play, 1810 Ward Dr, Murfreesboro &middot; "
               "Free, tickets limited"),
         link=(SPOOK_REG_URL, "Free registration"),
         disclose=SPOOK_DETAILS),
    dict(chip=chip("Sun", "25", "Oct"),
         title="Caleb&rsquo;s Friends Halloween Party",
         meta=("2:00 PM &middot; Heroes Den, 1257 Broad Street, Murfreesboro &middot; "
               "Teens and young adults with disabilities"),
         note="Costume Contest &middot; Candy &middot; Games &middot; Dancing.",
         link=(CALEB_FLYER, "Details")),
    dict(chip=chip("Thu", "29", "Oct"),
         title="Special Needs Family Fall Fest &middot; Pegram Church of Christ",
         meta="6:00&ndash;7:00 PM &middot; 5019 WalkUp Road, Pegram, TN &middot; About 65 min",
         note="Indoors with trick-or-treat and games.",
         link=(PEGRAM_FLYER, "Details")),
    # Oct 1 (Taylor): We Rock's indoor Halloween, from their post. Same booking link as the site's
    # events calendar (Roller "Spooktacular 2026", Sat Oct 31). Morning, so before Evergreen.
    dict(chip=chip("Sat", "31", "Oct"),
         title="Trick&amp;Treat&amp;Play &middot; We Rock the Spectrum Murfreesboro",
         meta=("Trick-or-treating 9:30 AM, Halloween play 10:00 AM&ndash;12:00 PM &middot; "
               "820 N Thompson Lane, Murfreesboro &middot; $20 per child, $10 per sibling, adults free"),
         note=WEROCK_HALLOWEEN_BLURB,
         link=(WEROCK_HALLOWEEN_URL, "Book your ticket")),
    dict(chip=chip("Sat", "31", "Oct"),
         title="Evergreen Trunk or Treat &middot; Evergreen Life Services",
         meta="1:00&ndash;3:00 PM &middot; 6050 Dana Way, Antioch, TN &middot; Free &middot; About 30 min",
         note=EVERGREEN_BLURB,
         sensory="outdoors; trunks, games, and booths built for IDD families.",
         link=(EVERGREEN_URL, "Details")),
]

MONSTERS_URL = "https://www.explorethedc.org/event/monsters-in-the-museum/"
DEADLINES_URL = f"{PAGES}deadlines-october-2026.html"
EVENTS_CAL_URL = f"{SITE}/events"

RCS_CAL = "https://www.rcschools.net/o/rcs/page/rcs-academic-calendars"
MCS_CAL = "https://www.cityschools.net/calendar"
DST_URL = "https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst"
# Taylor's rule: spell out RCS / MCS, and buttons instead of word links.
FALL_BREAK = item(
    "Fall break, Oct 5 to 9: Rutherford County and Murfreesboro City Schools",
    ["Both districts are closed all week. Rutherford County Schools conferences Tue Oct 20; Murfreesboro City "
     "Schools conferences Tue Nov 3 (no school). Ask for IEP progress data then."], featured=True) + pill_row(
    [(RCS_CAL, "Rutherford County Schools calendar"), (MCS_CAL, "Murfreesboro City Schools calendar")])
VOTER = item(
    "Voter registration deadline: Mon&nbsp;Oct&nbsp;5",
    ["For the Nov 3 election. Register or update your address at GoVoteTN.gov by Mon Oct 5. Early voting Oct 14 to 29. "
     "Voters with a disability can request a mail ballot by Sat Oct 24."], featured=True, first=True) + pill_row(
    [("https://govotetn.gov/", "GoVoteTN")])
# T404: same 18/16 title/body as Fall break + voter (featured=True).
CLOCKS = item(
    "Clocks fall back one hour on Sun Nov 1",
    ["Daylight saving time ends at 2:00 AM. If sleep is fragile at your house, shift bedtime 10 to 15 minutes a night the week before."],
    featured=True) + pill_row([(DST_URL, "How daylight saving time works")])

TAG_RULE = "#e6c3ae"


def deadlines_oct5_block():
    """Fall break + voter under one date tile, separated by 14px + hairline."""
    return (
        FALL_BREAK
        + f'<div style="margin:14px 0 14px 0;border-top:1px solid {TAG_RULE};font-size:0;line-height:0;height:1px;">&nbsp;</div>'
        + VOTER.replace('margin="14px 0 0 0"', 'margin="0"').replace("14px 0 4px 0", "0")
    )


TOP_DEADLINE_ROWS = [
    row(chip("Mon", "5", "Oct"), deadlines_oct5_block(), featured=True, line=TAG_RULE),
    row(chip("Sun", "1", "Nov"), CLOCKS, last=True, line=TAG_RULE),
]

# T355: her "October in Our Special Village" intro (audience = parents/caregivers of ND children).
# Em dashes from her draft become en dashes (newsletter ban).
NOTE_PARAS = [
    ("Welcome to Our Special Village! I&rsquo;m Dr. Taylor Hickok, a local speech-language "
     "pathologist, parent of an AuDHD child, and founder of this community."),
    ("I created Our Special Village after seeing how often families of neurodivergent children "
     "were left trying to navigate services, schools, therapies, and community resources on "
     "their own. Too many parents were asking the same questions without one clear place to "
     "find answers."),
    ("This month&rsquo;s newsletter brings together local events, practical resources, and "
     "opportunities to connect with other families. I hope it saves you a little time &ndash; and "
     "reminds you that you do not have to figure everything out alone."),
]
NOTE_TEXT = " ".join(NOTE_PARAS)  # plain-text export
ALONE_PHRASE = "you do not have to figure everything out alone"
IN_THIS_ISSUE = "Fall break &middot; Parent support &middot; Sensory-friendly events &middot; New resources"

ABOUT = ("A village for families like ours in Murfreesboro and surrounding areas: free guides, a local "
         "Resource Directory, sensory-friendly events, and a parent community. Built around autism and open "
         "to every kind of difference and disability.")

NUMBERS = [
    f'{tel("988", "988")} {b("Suicide &amp; Crisis Lifeline")} &middot; Call or text any hour.',
    f'{b("STEP TN")} (IEP help): {tel("800-280-7837", "+18002807837")} / Espa&ntilde;ol {tel("800-975-2919", "+18009752919")}',
    f'{b("Disability Rights TN:")} {tel("800-342-1660", "+18003421660")}',
]


def head():
    css = """
:root{color-scheme:light only;supported-color-schemes:light;}
a[x-apple-data-detectors]{color:inherit !important;text-decoration:none !important;}
u + #os-body a{text-decoration:none;}
.os-pill,.os-chip td{white-space:nowrap;}
.os-hl{background-image:linear-gradient(180deg,transparent 60%,#ebc97e 60%,#ebc97e 90%,transparent 90%);border-radius:4px;}
.os-sh{box-shadow:SHADOW;}
.os-psh{box-shadow:PAPER_SHADOW;}
.os-tsh{box-shadow:0 30px 50px -30px rgba(20,32,58,.7);}
.os-hand{transform:rotate(-2deg);transform-origin:left bottom;}
.os-tl{transform:rotate(-.6deg);}
.os-tr{transform:rotate(.8deg);}
.os-pay-note{white-space:nowrap;}
.os-sec{height:52px !important;line-height:52px !important;font-size:0 !important;}
@media only screen and (min-width:700px){
  .os-wrap{max-width:880px !important;width:100% !important;}
  .os-browser-cols{display:flex !important;flex-direction:row !important;gap:16px !important;align-items:stretch !important;width:100% !important;}
  .os-browser-col{flex:1 1 0 !important;width:auto !important;margin:0 !important;display:flex !important;flex-direction:column !important;}
  .os-browser-col > table.os-card{flex:1 1 auto !important;height:100% !important;}
  .os-browser-col > table.os-card > tbody{height:100% !important;}
  .os-browser-col > table.os-card > tbody > tr.os-card-body{height:100% !important;}
  .os-browser-col > table.os-card td.os-cardpad{height:100% !important;vertical-align:top !important;display:flex !important;flex-direction:column !important;box-sizing:border-box !important;}
  .os-card-cta,.os-equal-pair .os-sg-cta{margin-top:auto !important;padding-top:20px !important;}
  .os-tiny,.os-footer p{font-size:14px !important;line-height:21px !important;}
}
@media only screen and (max-width:699px){
  .os-sec{height:40px !important;line-height:40px !important;}
}
@media only screen and (max-width:620px){
  html,body{width:100% !important;overflow-x:hidden !important;-webkit-text-size-adjust:100% !important;}
  .os-wrap{width:100% !important;max-width:100% !important;}
  .os-pad{padding-left:20px !important;padding-right:20px !important;}
  .os-cardpad{padding-left:16px !important;padding-right:16px !important;}
  .os-boardpad{padding:18px 10px 16px 10px !important;}
  .os-h1{font-size:28px !important;line-height:32px !important;}
  .os-hero-h1{font-size:35px !important;line-height:38px !important;letter-spacing:-0.8px !important;}
  .os-tagline{font-size:23px !important;line-height:27px !important;}
  .os-place{font-size:10.5px !important;letter-spacing:1.3px !important;padding:0 !important;}
  .os-hrule{display:none !important;}
  .os-mast-word{font-size:18px !important;}
  .os-h2{font-size:25px !important;line-height:30px !important;}
  .os-col{display:block !important;width:100% !important;max-width:100% !important;padding:0 !important;}
  .os-col-photo{padding:0 0 14px 0 !important;text-align:center !important;}
  .os-guestphoto,.os-aboutphoto{margin:0 auto !important;}
  .os-stoplabel{font-size:13px !important;line-height:16px !important;}
  .os-stamp{width:80px !important;}
  .os-stamp img{width:80px !important;height:63px !important;}
  .os-cred{font-size:12px !important;white-space:normal !important;}
  .os-pill{white-space:normal !important;}
  .os-intro-photo{width:56px !important;height:56px !important;}
  p{overflow-wrap:break-word;}
  .os-chip td{white-space:nowrap !important;}
  .os-pay-wrap{text-align:center !important;}
  .os-pay-note{white-space:normal !important;}
  .os-paygrid tr{display:flex !important;flex-wrap:wrap !important;width:100% !important;}
  .os-paycell{display:block !important;width:50% !important;max-width:50% !important;box-sizing:border-box !important;padding:0 4px 8px 0 !important;}
  .os-paycell:nth-child(even){padding:0 0 8px 4px !important;}
}
@media only screen and (max-width:359px){
  .os-stoplabel{font-size:12px !important;}
  .os-cred{font-size:11px !important;}
}
""".replace("PAPER_SHADOW", PAPER_SHADOW).replace("SHADOW", SHADOW)
    dark = f"""
[data-ogsb] .os-bg{{background-color:{CREAM} !important;}} [data-ogsb] .os-card{{background-color:{NOTE} !important;}} [data-ogsb] .os-navy,[data-ogsb] .os-btn-navy{{background-color:{INK} !important;}} [data-ogsb] .os-btn-gold,[data-ogsb] .os-stepbg{{background-color:{GOLD} !important;}}
[data-ogsc] .os-ink{{color:{INK} !important;}} [data-ogsc] .os-body{{color:{BODY} !important;}} [data-ogsc] .os-muted{{color:{MUTED} !important;}} [data-ogsc] .os-accent{{color:{ACCENT} !important;}} [data-ogsc] .os-gold{{color:{GOLD} !important;}} [data-ogsc] .os-goldink{{color:{GOLD_INK} !important;}} [data-ogsc] .os-brick{{color:{BRICK_INK} !important;}} [data-ogsc] .os-sand{{color:{SAND} !important;}} [data-ogsc] .os-white{{color:{WHITE} !important;}}
@media (prefers-color-scheme: dark){{
  .os-bg{{background-color:{CREAM} !important;}} .os-card{{background-color:{NOTE} !important;}} .os-navy,.os-btn-navy{{background-color:{INK} !important;}} .os-btn-gold,.os-stepbg{{background-color:{GOLD} !important;}}
  .os-ink{{color:{INK} !important;}} .os-body{{color:{BODY} !important;}} .os-muted{{color:{MUTED} !important;}} .os-accent{{color:{ACCENT} !important;}} .os-gold{{color:{GOLD} !important;}} .os-goldink{{color:{GOLD_INK} !important;}} .os-brick{{color:{BRICK_INK} !important;}} .os-sand{{color:{SAND} !important;}} .os-white{{color:{WHITE} !important;}}
}}
"""
    return f'''<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light only"><meta name="supported-color-schemes" content="light">
<title>{SUBJECT}</title>
<!-- MailerLite: Subject "{SUBJECT}". Merge tags {{$url}} and {{$unsubscribe}}. Plain text: newsletter-october-2026.txt. -->
<!-- Built by tools/build-october-2026.py. Edit that file, not this one. Site pictures: tools/render-decor.mjs. -->
<link href="https://fonts.googleapis.com/css2?family=Mulish:wght@400;700;800&amp;family=Outfit:wght@500;600&amp;family=Patrick+Hand&amp;display=swap" rel="stylesheet">
<style type="text/css">
{css}
{dark}
</style>
<!--[if mso]>
<style type="text/css">body,table,td,p,a,span{{font-family:Arial,Helvetica,sans-serif !important;}} p,td,a,span{{mso-line-height-rule:exactly;}}</style>
<![endif]-->
</head>'''


HOPE = dict(
    eyebrow="Family win",
    title="His love needs no words.",
    photo="hope-print.jpg",
    alt=("Nicole smiling with her arms around Connor and his brother, both in red shirts, at a birthday "
         "celebration with a gold number 8 balloon and star balloons behind them."),
    paras=[
        ("My name is Nicole. I am a single mom of two amazing boys. I am also a person in recovery who has "
         "experienced many challenging, traumatic events. Being a special needs mom has been the hardest "
         "experience of my life."),
        ("The most remarkable thing about this journey has been realizing that verbal communication is not "
         "necessary to express love. Connor expresses his love in the unexpected eye contact, the couple of "
         "tickles, the laughs, the rare interactive play."),
        ("When he grabbed my face and put his nose to mine and gave me Eskimo kisses while he giggled. That "
         "only happened twice but it was the most special moment."),
        ("When you have a child with special needs life can be lonely, dark, scary and filled with anxiety "
         "but! It is filled with moments of pure innocence, joy, love and light. Connor makes leaps and "
         "bounds of improvement and then will regress and it ebbs and flows. Every success no matter how "
         "&ldquo;small&rdquo; is celebrated loudly by the village. I&rsquo;m so grateful for the people that "
         "have been walking alongside us. It truly does take a village."),
        ("Let me leave you with a hopeshot, I know this isn&rsquo;t the life you thought you would have. I "
         "know you don&rsquo;t hear &ldquo;I love you&rdquo; or go to baseball games. I know you sit outside "
         "the party room while everyone else celebrates. The hopeshot is that you gain so many beautiful life "
         "lessons, moments, experiences and perspective that others do not get the pleasure to experience. "
         "If nobody has told you today I love you, you are doing a great job, we are the village."),
    ],
    byline="&#9998; Nicole, Murfreesboro",
)


_TAG = re.compile(r"<(td|table|th|div|p|span|a|img|b)\b[^>]*>")


def compact(html):
    """Trim inline CSS that the HTML attributes already say, to stay under Gmail's 102KB clip.

    cellspacing="0" makes border-collapse moot, valign covers vertical-align, and
    cellpadding="0" already zeroes cell padding.
    """
    def fix(m):
        tag = m.group(0)
        if 'style="' not in tag:
            return tag
        tag = tag.replace("border-collapse:collapse;", "").replace("border-collapse:separate;", "")
        va = re.search(r'valign="(top|middle|bottom)"', tag)
        if va:
            tag = tag.replace(f"vertical-align:{va.group(1)};", "")
        if m.group(1) == "td":
            tag = re.sub(r'(style=")padding:0;', r"\1", tag)
        if m.group(1) == "table" and 'width="100%"' in tag:
            tag = tag.replace('style="width:100%;', 'style="')
        if "background-image" not in tag and "background-size" not in tag:
            tag = re.sub(r"background-color:(#[0-9a-fA-F]{3,6});", r"background:\1;", tag)
        return tag.replace(' style=""', "")
    return _TAG.sub(fix, html)


def build_html(base, browser=False):
    art = lambda f: f"{base}art/{f}"
    o = [head()]
    o.append(f'<body id="os-body" class="os-bg" bgcolor="{CREAM}" style="margin:0;padding:0;background-color:{CREAM};width:100%;overflow-x:hidden;">')
    o.append(f'<span style="display:none;font-size:1px;color:{CREAM};line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{PREHEADER}</span>')
    o.append(f'<table {T} class="os-bg" width="100%" bgcolor="{CREAM}" style="width:100%;border-collapse:collapse;background-color:{CREAM};">'
             f'<tr><td align="center" style="padding:14px 10px 40px 10px;font-family:{FONT};color:{BODY};">'
             f'<table {T} class="os-wrap" width="600" style="width:100%;max-width:600px;border-collapse:collapse;">')

    view_href = BROWSER_VIEW_URL if browser else "{$url}"
    unsub_href = BROWSER_UNSUB_URL if browser else "{$unsubscribe}"
    # --- Opening: top bar, header, the village in its landscape, Taylor's letter ---
    o.append(f'<tr><td style="padding:0 0 12px 0;">{top_bar("October 2026", view_href)}</td></tr>')
    o.append(padrow(site_header(art, SITE), pad="0 16px 14px 16px"))
    o.append(hero(art, 'October in Our <span class="os-hl">Special Village</span>', "fall"))
    alone_hi = f'<span style="background-color:{GOLD_SOFT};color:{INK};padding:1px 4px;border-radius:4px;">{ALONE_PHRASE}</span>'
    paras = "".join(p(para.replace(ALONE_PHRASE, alone_hi), 16, 25, BODY, 400, margin=("0" if i == 0 else "10px 0 0 0"))
                    for i, para in enumerate(NOTE_PARAS))
    o.append(padrow(letter(art, None, paras)))
    o.append(sp(26))
    o.append(padrow(stops_block(art, [("#deadlines", "Fall break"), ("#ongoing", "Parent support"),
                                      ("#events", "Sensory-friendly events"), ("#library", "New resources")]), pad="0 22px"))

    # --- Three things: the deadline tag ---
    o.append(major_sp())
    o.append(section_head("deadlines", "Three things to know this month", eyebrow="Deadline watch"))
    o.append(sp(14))
    o.append(padrow(tag_card(art, rows_table(TOP_DEADLINE_ROWS))))
    o.append(sp(16))
    o.append(padrow(button(DEADLINES_URL, "See all deadlines", INK, CREAM)
                    + p("Dates confirmed Sept 14. If something changed, reply and we will fix it.", 13, 20, MUTED, 400, margin="8px 0 0 0", cls="os-confirm")))

    # --- Village Hall: bunting, the hall, fact pills, the notice board, the ticket ---
    o.append(major_sp())
    o.append(fullrow(img(art(DECOR + "bunting.png"), 600, "", style="max-width:none;")))
    o.append(padrow(anchor("village-hall") + hand("The next deep dive", 22, GOLD_INK, "8px 0 0 0")
                    + h2("Village Hall", "2px 0 0 0", 40, 44)
                    + p("One topic. One guest expert. Your questions.", 19, 25, INK, 500, margin="6px 0 0 0",
                        extra=f"font-family:{DISPLAY};")))
    o.append(fullrow(img(art("vh-land.jpg"), 600, "Parents gathered around a table with a laptop for an online IEP workshop - autumn village setting",
                         style="max-width:none;")))
    o.append(padrow(fact_pills("Saturday, October 10, 2026", ["9:30 to 11:00 AM Central", "Online", "Free"])))
    o.append(sp(12))
    mercedes = dict(
        name="Mercedes Lawson, M.S. Ed.",
        role="Founder of A.C.C.E.S.S. &middot; Greater Nashville",
        photo_alt="Mercedes Lawson, M.S. Ed., with her family.",
        bio=("She grew up with a sibling with disabilities, taught special education for nine years "
             "helping 250+ students, and has two neurodivergent children. Through A.C.C.E.S.S. "
             "(Advocacy &amp; Consultation Center for Educational Student Supports), she helps families "
             "with IEP consultation, educational advocacy, and tutoring."),
        links=[(ACCESS_URL, "accessyouredu.com"), (f"mailto:{ACCESS_EMAIL}", "access.your.education@<wbr>gmail.com")],
    )
    o.append(padrow(board(art, poster(
        art, "Topic and guest", "The IEP process and navigating the school system",
        guest_block(mercedes, art, photo_src=art("guest-1-print.jpg")),
        "A 45-minute lesson on how the IEP process works and how to navigate the school system, then live parent "
        "questions. The lesson is recorded and sent to registrants; the Q&amp;A is not."))))
    o.append(sp(18))
    o.append(padrow(ticket(art, button(f"{SITE}/village-hall", "Register for Village Hall", GOLD, INK, align="center"), free_note())))

    # --- The month ahead: featured night, then the calendar page ---
    o.append(major_sp())
    o.append(section_head("events", "The month ahead", "Picked for sensory-sensitive kids and their families. Drive times are from Murfreesboro.",
                          eyebrow="Happening soon"))
    o.append(sp(14))
    featured_art = story_img(art("featured-monsters-museum-compact.jpg"), 600,
                             "Family exploring a friendly museum dinosaur exhibit at a calm after-hours sensory night; one child wears headphones",
                             link=MONSTERS_URL, extra_style="margin:0 auto;")
    featured_copy = (hand("Featured", 21, GOLD_INK, "12px 0 0 0")
                     + p("All Access Night: Monsters in the Museum &middot; Discovery Center", 19, 25, INK, 700, margin="4px 0 0 0")
                     + p("Thu Oct 15 &middot; 6:00&ndash;8:00 PM &middot; Murfreesboro &middot; Free, registration required", 16, 24, BODY, 400, margin="6px 0 0 0")
                     + pill_row([(MONSTERS_URL, "Reserve your spot")], kind="gold", margin="6px 0 0 0"))
    o.append(padrow(card(featured_art + featured_copy, pad="12px 12px 18px 12px")))
    o.append(sp(20))
    ev_rows = []
    for i, e in enumerate(SECONDARY_EVENTS):
        lines = [e["meta"]] + ([e["note"]] if e.get("note") else []) + disclose(e.get("disclose") or [])
        content = item(e["title"], lines)
        if e.get("link"):
            content += pill_row([e["link"]])
        ev_rows.append(row(e["chip"], content, last=(i == len(SECONDARY_EVENTS) - 1), tight=True))
    o.append(padrow(calendar_page(art, rows_table(ev_rows))))
    o.append(sp(20))
    o.append(padrow(button(EVENTS_CAL_URL, "View the full October events calendar", INK, CREAM, align="center")))

    # --- New in the library: two books ---
    o.append(major_sp())
    o.append(section_head("library", "New in the library", eyebrow="Resource Library"))
    o.append(sp(14))
    guide = lambda f, alt, title, blurb, href, cta, n: book(
        art, "New guide",
        img(art(f), 490, alt, 228, style="border-radius:10px;margin:0 0 12px 0;", cls="os-card-art"),
        p(title, 18, 24, INK, 700) + p(blurb, 15, 22, BODY, 400, margin="8px 0 0 0")
        + f'<div class="os-card-cta">{pill_row([(href, cta)], margin="4px 0 0 0")}</div>', n)
    o.append(padrow(browser_cols(
        guide("guide-therapy-styles-landscape-compact.jpg", "Adult and child sharing a calm sensory play tray in a warm playroom",
              "Therapy styles: play, structure, and compliance",
              "Two therapists can have the same license and run completely different rooms. Learn what the common labels actually look like.",
              f"{SITE}/resources/therapy-styles", "Read the guide", 0),
        guide("guide-grief-landscape-compact.jpg", "Parent on a porch in autumn while a child plays nearby in leaves - quiet and hopeful",
              "Grief and disability: the loss nobody sends a card for",
              "This kind of grief rarely has an occasion attached. It shows up at a birthday, a missed milestone, or in the parking lot after an evaluation.",
              f"{SITE}/resources/grieving-the-life-you-imagined", "Read the grief guide", 1),
        gap=18)))

    # --- Wall of Hope: Nicole's story pinned to the board, and a note to add yours ---
    o.append(major_sp())
    o.append(section_head("hope", "Wall of Hope", eyebrow="One hopeful story"))
    o.append(sp(8))
    o.append(padrow(img(art(DECOR + "garland.png"), 532, "")))
    hope_photo = img(art(HOPE["photo"]), 250, HOPE["alt"], style="margin:0 auto;", cls="os-hope-photo")
    hope_paras = "".join(p(t, 16, 26, BODY, 400, margin=("0" if i == 0 else "12px 0 0 0")) for i, t in enumerate(HOPE["paras"]))
    story = story_note(art, HOPE["eyebrow"], HOPE["title"], hope_photo, hope_paras, HOPE["byline"])
    invite = share_note("Borrow a little hope, or lend some",
                        "Have a win of your own? Tell it like you would tell another parent.",
                        pill(f"{SITE}/hope", "Share your win", "gold", "4px 0 0 0"))
    o.append(padrow(board(art, f'<div class="os-hope">{story}</div><div style="height:22px;font-size:0;line-height:0;">&nbsp;</div>{invite}')))

    # --- One question, answered: the index card ---
    o.append(major_sp())
    o.append(section_head("question", "One question, answered", "One real question from a local parent, answered plainly.",
                          eyebrow="Parent to parent"))
    o.append(sp(14))
    steps = rows_table([
        step(1, f'{b("Put it in writing.")} Email the case manager and copy the principal: name what is missing, quote the IEP, ask for a fix by a date, and request service logs.'),
        step(2, f'{b("Ask for an IEP team meeting.")} Request one in writing any time. If things stall, copy the district special education director. Bring notes and a friend.'),
        step(3, f'{b("Use free state help.")} File a Tennessee Department of Education administrative complaint (no lawyer, decision in 60 days), or call STEP TN at {tel("800-280-7837", "+18002807837")}', last=True),
    ])
    q_head = (f'<table {T} width="100%" style="width:100%;border-collapse:collapse;"><tr><td valign="top">'
              + hand("October&rsquo;s question") + '</td>' + question_mark() + '</tr></table>'
              + p("&ldquo;What do I do if my child&rsquo;s IEP isn&rsquo;t being followed?&rdquo;", 20, 27, INK, 700, margin="4px 0 0 0")
              + p("An IEP is legally binding. The school has to deliver what is written in it.", 16, 24, BODY, 400, margin="8px 0 0 0"))
    q_foot = (pill_row([(f"{SITE}/resources/iep-504", "IEP &amp; 504 guide"),
                        ("https://www.tn.gov/education/legal-services/special-education-legal-services/legal-dispute-resolution-processes.html",
                         "Tennessee Department of Education dispute options"),
                        (f"{SITE}/contact", "Send us yours")], margin="0")
              + p("Parent-to-parent guidance, not legal advice.", 13, 20, MUTED, 400, margin="10px 0 0 0", cls="os-tiny"))
    o.append(padrow(index_card(art, q_head, steps, q_foot)))

    # --- Connect with other local parents: two taped notes ---
    o.append(sp(34))
    online_card = group_card(
        [], "Our Special Village Online Parent Group",
        [("calendar", "Thursdays"), ("clock", "7:00&ndash;8:00 PM Central"), ("video", "Online")],
        "Connect with parents and caregivers of neurodivergent and disabled children in a welcoming, judgment-free space.",
        ["No formal diagnosis required", "Drop in any Thursday beginning October 1", "Cameras are optional", "Meetings are never recorded"],
        f"{SITE}/group", "Join the Online Group", secondary=["ONLINE", "WEEKLY", "FREE"], art=art, tilt="os-tl")
    werock_card = group_card(
        [], "We Rock the Spectrum Parent Group",
        [("calendar", "Wednesdays at 5:00 PM"), ("pin", "We Rock the Spectrum Murfreesboro")],
        "Connect with other parents of kids with special needs while children enjoy the gym. "
        "Gym staff watch the kids during group; childcare is available but not appropriate for all children.",
        ["Led by Cari Parr", "$15 per child for kids to play",
         "Gym staff watch children during group; not appropriate for all children", "Discounted gym admission is available separately."],
        WRTS_URL, "Plan Your Visit", secondary=["IN PERSON", "WEEKLY", "FREE"], art=art, tilt="os-tr")
    o.append(dusk_band(art, "ongoing", "The heart of the village", "Connect with other local parents",
                       '<div class="os-browser-cols os-equal-pair" style="display:block;width:100%;">'
                       f'<div class="os-browser-col" style="display:block;width:100%;margin:0 0 20px 0;box-sizing:border-box;">{online_card}</div>'
                       f'<div class="os-browser-col" style="display:block;width:100%;margin:0;box-sizing:border-box;">{werock_card}</div></div>'))

    # --- About, numbers, forward, footer ---
    o.append(major_sp())
    o.append(padrow(about_card(art, ABOUT, [(f"{SITE}/about", "About the Village"), (f"{SITE}/editorial-policy", "How we check information")])))
    o.append(sp(20))
    o.append(padrow(numbers_card(art, NUMBERS)))
    o.append(sp(22))
    o.append(padrow(forward_line(SITE)))
    o.append(sp(30))
    o.append(footer_rows(art, SITE, unsub_href))
    o.append('</table></td></tr></table></body></html>')
    return compact("\n".join(o) + "\n")


def _plain(s):
    import html as _h
    return _h.unescape(re.sub(r"<[^>]+>", "", s)).replace("\u2013", "-")


def build_text():
    L = []
    w = L.append
    w("OUR SPECIAL VILLAGE · October 2026")
    w("View this email in your browser: {$url}")
    w("")
    w("OCTOBER IN OUR SPECIAL VILLAGE")
    w("")
    for para in NOTE_PARAS:
        # strip entities for plain text
        plain = (para.replace("&rsquo;", "'").replace("&middot;", "·")
                     .replace("&ndash;", "-").replace("&amp;", "&")
                     .replace("&ldquo;", '"').replace("&rdquo;", '"'))
        w(plain)
        w("")
    w("With love,")
    w("Taylor")
    w("")
    w("In this issue: Fall break · Parent support · Sensory-friendly events · New resources")
    w("")
    w("----------------------------------------")
    w("THREE THINGS TO KNOW THIS MONTH")
    w("")
    w("Mon Oct 5 · Fall break, Oct 5 to 9: Rutherford County and Murfreesboro City Schools")
    w("  Both districts are closed all week. Rutherford County Schools conferences Tue Oct 20; Murfreesboro City Schools conferences Tue Nov 3 (no school). Ask for IEP progress data then.")
    w(f"  Rutherford County Schools calendar: {RCS_CAL}")
    w(f"  Murfreesboro City Schools calendar: {MCS_CAL}")
    w("")
    w("Mon Oct 5 · Voter registration deadline: Mon Oct 5")
    w("  For the Nov 3 election. Register or update at GoVoteTN.gov by Mon Oct 5. Early voting Oct 14 to 29. Disability mail-ballot requests by Sat Oct 24.")
    w("  GoVoteTN: https://govotetn.gov/")
    w("")
    w("Sun Nov 1 · Clocks fall back one hour")
    w("  If sleep is fragile, shift bedtime 10 to 15 minutes a night the week before.")
    w(f"  How daylight saving time works: {DST_URL}")
    w("")
    w(f"See all deadlines: {DEADLINES_URL}")
    w("Dates confirmed Sept 14. If something changed, reply and we will fix it.")
    w("")
    w("----------------------------------------")
    w("THE NEXT DEEP DIVE · VILLAGE HALL")
    w("")
    w("Village Hall: Saturday, October 10, 2026")
    w("9:30 to 11:00 AM Central")
    w("Online · Free")
    w("Topic and guest: The IEP process and navigating the school system")
    w("Mercedes Lawson, M.S. Ed. - Founder of A.C.C.E.S.S. (Advocacy & Consultation Center for Educational Student Supports) in Greater Nashville. She grew up with a sibling with disabilities, taught special education for nine years helping 250+ students, and has two neurodivergent children. She helps families with IEP consultation, educational advocacy, and tutoring.")
    w(f"Website: {ACCESS_URL}")
    w(f"Email: {ACCESS_EMAIL}")
    w("A 45-minute lesson, then live parent questions. Lesson recorded; Q&A is not.")
    w(f"Register for Village Hall: {SITE}/village-hall")
    w("Free for every family. Our first Village Hall is free. Register to save your seat.")
    w("The meeting link is emailed to registrants.")
    w("")
    w("----------------------------------------")
    w("THE MONTH AHEAD")
    w("Picked for sensory-sensitive kids and their families. Drive times are from Murfreesboro.")
    w("")
    w("All Access Night: Monsters in the Museum · Discovery Center  [Featured]")
    w("  Thu Oct 15 · 6:00-8:00 PM · Murfreesboro · Free, registration required")
    w(f"  Reserve your spot: {MONSTERS_URL}")
    w("")
    import html as _html
    strip = lambda s: _html.unescape(re.sub(r"<[^>]+>", "", s))
    for e in SECONDARY_EVENTS:
        w(strip(e["title"]))
        w(f"  {strip(e['meta'])}")
        for extra in e.get("disclose") or []:
            w(f"  {strip(extra)}")
        if e.get("note"):
            w(f"  {strip(e['note'])}")
        if e.get("link"):
            w(f"  {e['link'][1]}: {e['link'][0]}")
        w("")
    w(f"View the full October events calendar: {EVENTS_CAL_URL}")
    w("")
    w("----------------------------------------")
    w("NEW IN THE LIBRARY")
    w("")
    w("New guide · Therapy styles: play, structure, and compliance")
    w("  Two therapists can have the same license and run completely different rooms. Learn what the common labels actually look like.")
    w(f"  Read the guide: {SITE}/resources/therapy-styles")
    w("")
    w("New guide · Grief and disability: the loss nobody sends a card for")
    w("  This kind of grief rarely has an occasion attached. It shows up at a birthday, a missed milestone, or in the parking lot after an evaluation.")
    w(f"  Read the grief guide: {SITE}/resources/grieving-the-life-you-imagined")
    w("")
    w("----------------------------------------")
    w("WALL OF HOPE")
    w("")
    w(f"{HOPE['eyebrow']}: {_plain(HOPE['title'])}")
    for para in HOPE["paras"]:
        w("  " + _plain(para))
    w("  " + _plain(HOPE["byline"]))
    w("")
    w("Borrow a little hope, or lend some")
    w("  Have a win of your own? Tell it like you would tell another parent.")
    w(f"  Share your win: {SITE}/hope")
    w("")
    w("----------------------------------------")
    w("ONE QUESTION, ANSWERED")
    w(f"Send us yours: {SITE}/contact")
    w("")
    w('October\'s question: "What do I do if my child\'s IEP isn\'t being followed?"')
    w("An IEP is legally binding. The school has to deliver what is written in it.")
    w("")
    w("1. Put it in writing. Email the case manager and copy the principal: name what is missing, quote the IEP, ask for a fix by a date, and request service logs.")
    w("2. Ask for an IEP team meeting in writing. If things stall, copy the district special education director. Bring notes and a friend.")
    w("3. Use free state help. File a Tennessee Department of Education administrative complaint, or call STEP TN at 800-280-7837.")
    w("")
    w(f"IEP & 504 guide: {SITE}/resources/iep-504")
    w("Tennessee Department of Education dispute options: https://www.tn.gov/education/legal-services/special-education-legal-services/legal-dispute-resolution-processes.html")
    w("Parent-to-parent guidance, not legal advice.")
    w("")
    w("----------------------------------------")
    w("CONNECT WITH OTHER LOCAL PARENTS")
    w("")
    w("Our Special Village Online Parent Group")
    w("  ONLINE · WEEKLY · FREE")
    w("  Thursdays · 7:00-8:00 PM Central · Online")
    w("  Connect with parents and caregivers of neurodivergent and disabled children in a welcoming, judgment-free space.")
    w("  Good to know: No formal diagnosis required; Drop in any Thursday beginning October 1; Cameras are optional; Meetings are never recorded.")
    w(f"  Join the Online Group: {SITE}/group")
    w("")
    w("We Rock the Spectrum Parent Group")
    w("  IN PERSON · WEEKLY · FREE")
    w("  Wednesdays at 5:00 PM · We Rock the Spectrum Murfreesboro")
    w("  Connect with other parents of kids with special needs while children enjoy the gym. Gym staff watch the kids during group; childcare is available but not appropriate for all children.")
    w("  Good to know: Led by Cari Parr; $15 per child for kids to play; Gym staff watch children during group; not appropriate for all children; Discounted gym admission is available separately.")
    w(f"  Plan Your Visit: {WRTS_URL}")
    w("")
    w("----------------------------------------")
    w("ABOUT OUR SPECIAL VILLAGE")
    w("")
    w(ABOUT)
    w("")
    w(f"About the Village: {SITE}/about")
    w(f"How we check information: {SITE}/editorial-policy")
    w("")
    w("NUMBERS WORTH KEEPING")
    w("988 Suicide & Crisis Lifeline · Call or text any hour.")
    w("STEP TN (IEP help): 800-280-7837 / Español 800-975-2919")
    w("Disability Rights TN: 800-342-1660")
    w("")
    w(f"Know a family who could use this? Forward it along. Anyone can join at {SITE}/newsletter")
    w("")
    w("----------------------------------------")
    w("Our Special Village · Murfreesboro and surrounding areas, Tennessee")
    w(f"Sponsorship options: {SITE}/sponsors")
    w("")
    w("You are receiving this because you joined the newsletter list at ourspecialvillagetn.com.")
    w("Unsubscribe in one click: {$unsubscribe}")
    w(f"Privacy: {SITE}/privacy · Contact: {SITE}/contact")
    w("")
    w("Our Special Village is owned and operated by Little Luminaries Therapy Services, PLLC")
    w("1810 Ward Dr, Suite 101, Murfreesboro, TN 37129")
    return "\n".join(L) + "\n"


def deadline_chip(dow, day, moy):
    """Newsletter-style date square (left chip). Range bottoms stay one line."""
    moy = format_chip_range_end(moy)
    return (
        f'<div class="chip" aria-hidden="true">'
        f'<div class="dow">{dow}</div>'
        f'<div class="dom">{day}</div>'
        f'<div class="moy">{moy}</div>'
        f'</div>'
    )


def deadline_item(dow, day, moy, title, body):
    return (
        f'<div class="item">{deadline_chip(dow, day, moy)}'
        f'<div class="body"><strong>{title}</strong>{body}</div></div>'
    )


def build_deadlines_page():
    items_school = "".join([
        deadline_item(
            "Mon", "5", "Oct",
            "Fall break, Oct&nbsp;5&ndash;9: RCS and MCS",
            'Both districts closed. RCS conferences Tue Oct 20; MCS conferences Tue Nov 3 (no school). '
            '<a href="https://www.rcschools.net/o/rcs/page/rcs-academic-calendars">RCS</a>, '
            '<a href="https://www.cityschools.net/calendar">MCS</a>'),
        deadline_item(
            "Mon", "5", "Oct",
            "Voter registration deadline: Mon&nbsp;Oct&nbsp;5",
            'For the Nov 3 election. Early voting Oct 14&ndash;29; disability mail-ballot requests by Sat Oct 24. '
            '<a href="https://govotetn.gov/">GoVoteTN</a>'),
        deadline_item(
            "Sun", "1", "Nov",
            "Clocks fall back: Sun&nbsp;Nov&nbsp;1",
            'DST ends 2:00 AM. Shift bedtime gradually if sleep is fragile. '
            '<a href="https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst">NIST</a>'),
    ])
    items_health = "".join([
        deadline_item(
            "Oct", "15", "Dec 7",
            "Medicare open enrollment: Oct&nbsp;15&ndash;Dec&nbsp;7",
            'Compare or switch drug and Advantage plans for 2027. TN SHIP: 1-877-801-0044. '
            '<a href="https://www.medicare.gov/health-drug-plans/open-enrollment">Medicare.gov</a>'),
        deadline_item(
            "Nov", "1", "Jan 15",
            "HealthCare.gov: Nov&nbsp;1&ndash;Jan&nbsp;15",
            'Enroll by Dec 15 for Jan 1 coverage. Kids may qualify for TennCare or CoverKids any time. '
            '<a href="https://www.healthcare.gov/quick-guide/dates-and-deadlines/">Dates</a>'),
        deadline_item(
            "Any", "-", "time",
            "Katie Beckett (TennCare)",
            f'Apply any time; Part B has a waiting list. <a href="{SITE}/resources/katie-beckett">Katie Beckett guide</a>'),
    ])
    items_money = "".join([
        deadline_item(
            "Wed", "14", "Oct",
            "SSI / Social Security COLA announced: Wed&nbsp;Oct&nbsp;14",
            'Expected with the September inflation report; new amounts start in January. '
            '<a href="https://www.ssa.gov/cola/">SSA COLA</a>'),
    ])
    items_teens = "".join([
        deadline_item(
            "Thu", "1", "Oct",
            "FAFSA for 2027&ndash;28 opens: Thu&nbsp;Oct&nbsp;1",
            'Free. TN Promise students must file by April 1, 2027. '
            '<a href="https://studentaid.gov/h/apply-for-aid/fafsa">StudentAid.gov</a>'),
        deadline_item(
            "Thu", "1", "Oct",
            "Education Freedom Scholarship office hours: Thu&nbsp;Oct&nbsp;1, 1&ndash;2&nbsp;PM&nbsp;CT",
            '2027&ndash;28 application dates not posted yet. '
            '<a href="https://www.tn.gov/education/efs.html">EFS</a>'),
        deadline_item(
            "Mon", "2", "Nov",
            "Tennessee Promise deadline: Mon&nbsp;Nov&nbsp;2",
            'Class of 2027. <a href="https://www.collegefortn.org/tnpromise/">CollegeforTN</a>'),
        deadline_item(
            "Fri", "6", "Nov",
            "ACT accommodations for Dec&nbsp;12: Fri&nbsp;Nov&nbsp;6",
            'Through your school testing coordinator. '
            '<a href="https://www.act.org/content/act/en/products-and-services/the-act/registration/accommodations.html">ACT accommodations</a>'),
        deadline_item(
            "Mon", "16", "Feb",
            "Individualized Education Account: projected Feb&nbsp;16,&nbsp;2027",
            'Needs an active IEP and a prior year in a Tennessee public school. '
            '<a href="https://www.tn.gov/education/iea.html">IEA</a>'),
    ])
    items_undated = "".join([
        deadline_item(
            "Open", "-", "now",
            "Salvation Army Angel Tree (Rutherford &amp; Cannon)",
            'Family registration is full; spots may reopen. Adoptions open Nov 6. '
            '<a href="https://www.salvationarmymurfreesboro.org/angeltree">Angel Tree</a>'),
    ])

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>October 2026 deadlines · Our Special Village</title>
<link href="https://fonts.googleapis.com/css2?family=Mulish:wght@400;700;800&amp;family=Outfit:wght@500;600&amp;family=Patrick+Hand&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0;padding:24px 16px 48px;background:{CREAM};color:{BODY};font-family:{FONT};line-height:1.5;}}
main{{max-width:640px;margin:0 auto;}}
h1{{color:{INK};font-family:{DISPLAY};font-weight:600;letter-spacing:-.02em;font-size:32px;line-height:1.15;margin:0 0 8px;}}
h2{{color:{INK};font-family:{DISPLAY};font-weight:600;font-size:21px;margin:30px 0 12px;}}
.meta{{color:{MUTED};font-size:14px;margin:0 0 24px;}}
.item{{display:flex;gap:14px;align-items:flex-start;background:{WHITE};border:1px solid {HAIR};border-radius:16px;padding:14px 16px;margin:0 0 12px;box-shadow:{SHADOW};}}
.chip{{flex:0 0 62px;width:62px;background:#fff;border:2px solid {INK};border-radius:12px;overflow:hidden;text-align:center;padding:0 0 5px;box-sizing:border-box;font-family:{DISPLAY};font-weight:600;}}
.chip .dow,.chip .dom,.chip .moy{{white-space:nowrap;overflow-wrap:normal;word-break:normal;}}
.chip .dow{{background:{INK};color:{GOLD};font-size:11px;line-height:14px;padding:3px 0 2px;letter-spacing:1px;text-transform:uppercase;}}
.chip .dom{{color:{INK};font-size:24px;line-height:27px;margin:3px 0 0;}}
.chip .moy{{color:#7a5b13;font-size:11px;line-height:14px;letter-spacing:.8px;text-transform:uppercase;}}
.body{{flex:1;min-width:0;}}
.body strong{{color:{INK};font-family:{DISPLAY};font-weight:600;display:block;margin-bottom:4px;font-size:17px;overflow-wrap:normal;word-break:normal;}}
a{{color:{ACCENT};font-weight:700;text-decoration:none;}}
.body a{{display:inline-block;margin:8px 8px 0 0;padding:5px 14px;background:{WHITE};border:2px solid {INK};border-bottom-width:4px;border-radius:999px;color:{INK};font:600 14px/18px {DISPLAY};white-space:nowrap;}}
.back{{margin:0 0 20px;font-size:14px;}}
.back a{{font-family:{DISPLAY};font-weight:600;}}
</style></head><body><main>
<p class="back"><a href="{PAGES}">&larr; October newsletter preview</a></p>
<h1>All October deadlines</h1>
<p class="meta">Dates confirmed Sept 14, 2026. Teen, college, Medicare, benefits, and undated items live here so the email can stay short.</p>
<h2>School and community</h2>
{items_school}
<h2>Insurance and health</h2>
{items_health}
<h2>Money and benefits</h2>
{items_money}
<h2>Teens and college</h2>
{items_teens}
<h2>Undated</h2>
{items_undated}
<p class="meta" style="margin-top:28px;">If something changed, reply to the newsletter. A person reads it.</p>
</main></body></html>
"""



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=PAGES, help="URL prefix for art/ (default: GitHub Pages)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    args = ap.parse_args()
    html_email = build_html(args.base, browser=False)
    html_browser = build_html(args.base, browser=True)
    txt = build_text()
    deadlines = build_deadlines_page()
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "newsletter-october-subscriber-preview.html"), "w", encoding="utf-8") as f:
        f.write(html_email)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_browser)
    with open(os.path.join(out, "newsletter-october-2026.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    with open(os.path.join(out, "deadlines-october-2026.html"), "w", encoding="utf-8") as f:
        f.write(deadlines)
    html = html_email  # assertions target MailerLite/email HTML
    for s in (html_email, txt):
        assert "{$url}" in s and "{$unsubscribe}" in s
    # Merge tags may remain in HTML comments; live hrefs must be real destinations.
    assert f'href="{BROWSER_VIEW_URL}"' in html_browser
    assert f'href="{BROWSER_UNSUB_URL}"' in html_browser
    assert 'href="{$url}"' not in html_browser and 'href="{$unsubscribe}"' not in html_browser
    for s in (html_email, html_browser, txt, deadlines):
        assert "—" not in s and "&mdash;" not in s, "em dash found"
        assert "Village Picks" not in s and "Microsoft Teams" not in s
        assert "reviewed Sept" not in s and "reviewed Aug" not in s  # Taylor: no reviewed stamps
    for doc in (html_email, html_browser):
        # Taylor: no word links. Every <a> is a button, a picture, a stop on the path, or an anchor target.
        for m in re.finditer(r"<a (?![^>]*\bid=)[^>]*>", doc):
            tag = m.group(0)
            assert ("os-pill" in tag or "display:block" in tag or "display:inline-block" in tag), tag
        assert "text-decoration:underline" not in doc
        assert re.search(r"\bRCS\b|\bMCS\b|\bTDOE\b", re.sub(r"<[^>]+>", " ", doc)) is None, "spell out abbreviations"
        # the site pictures
        for f in ("decor/bunting.png", "decor/stamp.png", "decor/airmail-top.png", "decor/calendar-top.png",
                  "decor/tag-eyelet.png", "decor/ribbon-gold.png", "decor/ribbon-blue.png", "decor/garland.png", "decor/dusk-top.png", "decor/stars.png", "decor/dusk-wave.png", "hero-sky.jpg", "decor/swoosh.png", "decor/cork.png", "decor/ruled.png", "decor/foot-hills.png",
                  "decor/pin-brick.png", "decor/notch-l.png", "hero-land.jpg", "vh-land.jpg", "stop-1.png", "stop-4.png",
                  "guest-1-print.jpg", "hope-print.jpg", "decor/about-print.jpg", "signature-taylor.png",
                  "featured-monsters-museum-compact.jpg", "guide-therapy-styles-landscape-compact.jpg", "guide-grief-landscape-compact.jpg"):
            assert f"art/{f}" in doc, f
        # section order, and In this issue links to real sections
        order = ['id="deadlines"', 'id="village-hall"', 'id="events"', 'id="library"', 'id="hope"', 'id="question"', 'id="ongoing"']
        idx = [doc.find(x) for x in order]
        assert all(k > 0 for k in idx) and idx == sorted(idx), idx
        for href in ("#deadlines", "#ongoing", "#events", "#library"):
            assert f'href="{href}"' in doc
        # Wall of Hope is Nicole's story (Taylor, Sept 30), then the invitation
        hope_slice = doc.split('id="hope"', 1)[1].split('id="question"', 1)[0]
        for para in HOPE["paras"]:
            assert para in hope_slice
        assert "His love needs no words." in hope_slice and "&#9998; Nicole, Murfreesboro" in hope_slice
        assert "Ellie" not in doc and "&#9998; Taylor, Murfreesboro" not in doc
        assert hope_slice.find("we are the village.") < hope_slice.find("&#9998; Nicole, Murfreesboro") < hope_slice.find("Borrow a little hope, or lend some")
        assert f'href="{SITE}/hope"' in hope_slice and "Share your win" in hope_slice
    assert "WALL OF HOPE" in txt and "His love needs no words." in txt and "✎ Nicole, Murfreesboro" in txt and "Ellie" not in txt
    assert txt.find("NEW IN THE LIBRARY") < txt.find("WALL OF HOPE") < txt.find("ONE QUESTION, ANSWERED")
    # words that must survive the restyle
    for phrase in ("October in Our Special Village", "Welcome to Our Special Village!", "you do not have to figure everything out alone",
                   "Three things to know this month", "Voter registration deadline: Mon&nbsp;Oct&nbsp;5", "Clocks fall back one hour on Sun Nov 1",
                   "See all deadlines", "Dates confirmed Sept 14", "The next deep dive", "One topic. One guest expert. Your questions.",
                   "Saturday, October 10, 2026", "9:30 to 11:00 AM Central", "Topic and guest", "The IEP process and navigating the school system",
                   "Mercedes Lawson, M.S. Ed.", "two neurodivergent children", "Advocacy &amp; Consultation Center for Educational Student Supports",
                   "45-minute lesson", "Register for Village Hall", "Free for every family", "Our first Village Hall is free.",
                   "The meeting link is emailed to registrants.", "The month ahead", "View the full October events calendar",
                   "Sensory Spooktacular", "sensory-sensitive hour 1:00&ndash;2:00 PM", "Little Luminaries and Cultivate Play", "tickets limited",
                   "New in the library", "Therapy styles: play, structure, and compliance", "Grief and disability: the loss nobody sends a card for",
                   "One question, answered", "An IEP is legally binding.", "Parent-to-parent guidance, not legal advice.",
                   "Connect with other local parents", "Our Special Village Online Parent Group", "Drop in any Thursday beginning October 1",
                   "We Rock the Spectrum Parent Group", "Led by Cari Parr", "$15 per child for kids to play", "Discounted gym admission is available separately.",
                   "Join the Online Group", "Plan Your Visit", "About Our Special Village", "Numbers worth keeping", "Suicide &amp; Crisis Lifeline",
                   "Know a family who could use this?", "Unsubscribe in one click", "Little Luminaries Therapy Services, PLLC",
                   "6050 Dana Way, Antioch, TN", EVERGREEN_BLURB, "Touch-A-Truck after treats.", "700 Dan P. Herron Drive, Gallatin",
                   "1257 Broad Street, Murfreesboro", "5019 WalkUp Road, Pegram, TN", "About 4 hours 15 min", "(931) 265-5376",
                   SPOOK_ON_SITE, SPOOK_THANKS):
        assert phrase in html.replace('<span class="os-hl">', "").replace("Special Village</span>", "Special Village"), phrase
    for href in (ACCESS_URL, f"mailto:{ACCESS_EMAIL}", SPOOK_REG_URL, GALLATIN_FLYER, CALEB_FLYER, PEGRAM_FLYER, DOLLYWOOD_URL,
                 RECESS_MAIL, EVERGREEN_URL, MONSTERS_URL, RCS_CAL, MCS_CAL, DST_URL, "tel:988", "tel:+18002807837",
                 f"{SITE}/village-hall", f"{SITE}/group", WRTS_URL, f"{SITE}/sponsors", f"{SITE}/privacy", f"{SITE}/contact"):
        assert f'href="{href}"' in html, href
    assert html.count("Register for Village Hall") == 1
    assert "Amanda Rains" not in html and "Amanda Rains" not in txt
    # Spooktacular shows its details openly (no expander) and sits before Evergreen
    month = html.split('id="events"', 1)[1].split('id="library"', 1)[0]
    assert month.find("Sensory Spooktacular") < month.find("Evergreen Trunk or Treat")
    assert month.find(">25</td>") < month.find(">31</td>")
    spook_row = month[month.find("Sensory Spooktacular"):month.find("Caleb&rsquo;s Friends")]
    assert "<details" not in html and SPOOK_ON_SITE in spook_row and SPOOK_THANKS in spook_row
    assert spook_row.find(SPOOK_THANKS) < spook_row.find(SPOOK_REG_URL)
    assert txt.find("Sensory Spooktacular") < txt.find("Evergreen Trunk or Treat")
    for month_abbr in _NON_OCT_MONTHS:
        assert not re.search(rf'white-space:nowrap;">(?:&ndash;|&mdash;|–|—|-){month_abbr}', html)
        assert f'class="moy">&ndash;{month_abbr}' not in deadlines
    assert ">Nov&nbsp;1<" in html
    assert 'class="moy">Dec&nbsp;7<' in deadlines and 'class="moy">Jan&nbsp;15<' in deadlines
    text = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&\w+;", " ", text)
    words = len(text.split())
    # Nicole's full story (Sept 30) adds about 230 words over Ellie's.
    assert 850 <= words <= 1800, f"word count {words} outside 850-1800"
    print(f"wrote {out}: email {len(html_email.encode('utf-8'))}B, browser {len(html_browser.encode('utf-8'))}B, txt {len(txt.encode('utf-8'))}B, words≈{words}")


if __name__ == "__main__":
    main()
