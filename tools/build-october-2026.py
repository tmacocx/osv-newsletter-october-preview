#!/usr/bin/env python3
"""Build the October 2026 Our Special Village newsletter (T355 Hickok intro/support).

Writes newsletter-october-subscriber-preview.html, an identical index.html,
newsletter-october-2026.txt, and deadlines-october-2026.html (full deadline list).

T355: replace intro with "October in Our Special Village" copy (body font, not
full italic); keep signature PNG; tighter spacing; optional circular Taylor photo;
compact "In this issue"; highlight alone-callout; section heading Connect with
Other Local Parents; two equal badge cards; remove T353 inclusive lines; parent
supervision note on We Rock; Cari Parr retained (live OSV support-groups/events).

Edit this file and run it. Do not hand-edit the generated HTML.

    python3 tools/build-october-2026.py
"""
import argparse
import os
import re

PAGES = "https://tmacocx.github.io/osv-newsletter-october-preview/"
SITE = "https://ourspecialvillagetn.com"

CREAM = "#f7f1e2"
WHITE = "#ffffff"
BLUSH = "#f6e4d6"
INK = "#1b2340"
BODY = "#4a5169"
MUTED = "#6b6250"
ACCENT = "#964720"
HAIR = "#e6dcc6"
RULE = "#ece3cf"
GOLD = "#d4ac4d"
SAND = "#ded7c4"

FONT = "Figtree, 'Segoe UI', Helvetica, Arial, sans-serif"

CLASS_FOR = {INK: "os-ink", BODY: "os-body", MUTED: "os-muted", ACCENT: "os-accent",
             GOLD: "os-gold", SAND: "os-sand", CREAM: "os-cream", WHITE: "os-white"}

SUBJECT = "October: sensory-friendly events + deadlines"
PREHEADER = ("Fall break starts Oct 5. Three things to know this month, a featured Discovery Center night, "
             "two new guides, and one IEP question answered.")


def p(text, size=16, lh=24, color=BODY, weight=400, margin="0", extra="", cls=""):
    classes = " ".join(c for c in [CLASS_FOR.get(color, ""), cls] if c)
    w = f"font-weight:{weight};" if weight != 400 else ""
    return (f'<p class="{classes}" style="margin:{margin};font-family:{FONT};font-size:{size}px;'
            f'line-height:{lh}px;mso-line-height-rule:exactly;color:{color};{w}{extra}">{text}</p>')


def b(text, color=INK):
    return f'<b class="{CLASS_FOR.get(color, "")}" style="color:{color};font-weight:700;">{text}</b>'


def a(href, label, nowrap=True):
    nowrap_css = "white-space:nowrap;" if nowrap else ""
    return (f'<a class="os-link" href="{href}" style="color:{ACCENT};font-weight:700;'
            f'text-decoration:underline;{nowrap_css}">'
            f'<span class="os-link" style="color:{ACCENT};">{label}</span></a>')


def tel(number_display, number_tel):
    return a(f"tel:{number_tel}", number_display)


def sp(h):
    return f'<tr><td style="font-size:0;line-height:0;height:{h}px;mso-line-height-rule:exactly;">&nbsp;</td></tr>'


def padrow(inner, pad="0 34px"):
    return f'<tr><td class="os-pad" align="left" style="padding:{pad};">{inner}</td></tr>'


def anchor(id_):
    return f'<a id="{id_}" name="{id_}" style="display:block;height:0;line-height:0;font-size:0;">&nbsp;</a>'


def rule():
    return ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="40" '
            'style="width:40px;border-collapse:collapse;"><tr>'
            f'<td height="3" bgcolor="{ACCENT}" class="os-rulebar" style="height:3px;font-size:1px;line-height:3px;'
            f'mso-line-height-rule:exactly;background-color:{ACCENT};">&nbsp;</td></tr></table>')


def section_head(id_, title, intro=None):
    out = anchor(id_) + rule()
    out += (f'<h2 class="os-h2 os-ink" style="margin:14px 0 0 0;font-family:{FONT};font-size:21px;'
            f'line-height:27px;mso-line-height-rule:exactly;color:{INK};font-weight:700;">{title}</h2>')
    if intro:
        out += p(intro, 16, 24, BODY, 400, margin="8px 0 0 0")
    return padrow(out)


def card(inner, pad="8px 20px 8px 20px"):
    return (f'<table role="presentation" class="os-card" cellpadding="0" cellspacing="0" border="0" width="100%" '
            f'bgcolor="{WHITE}" style="width:100%;border-collapse:separate;background-color:{WHITE};'
            f'border:1px solid {HAIR};border-radius:16px;box-shadow:0 1px 3px rgba(27,35,64,0.06);">'
            f'<tr><td class="os-cardpad" align="left" style="padding:{pad};">{inner}</td></tr></table>')


def rows_table(rows_html):
    return ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" '
            'style="width:100%;border-collapse:collapse;">' + "".join(rows_html) + '</table>')


def row(chip_html, content_html, last=False, featured=False):
    pad = "16px 0 18px 0" if featured else "11px 0 12px 0"
    border = "" if last else f"border-bottom:1px solid {RULE};"
    return (f'<tr><td class="os-rule" style="padding:{pad};{border}">'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;">'
            f'<tr><td width="62" style="width:62px;vertical-align:top;padding:2px 14px 0 0;">{chip_html}</td>'
            f'<td style="vertical-align:top;">{content_html}</td></tr></table></td></tr>')


def chip(top, big=None, bottom=None, year=False):
    """Date square. Bottom range labels stay on one line (nowrap; shorten 'to …')."""
    nowrap = "text-align:center;white-space:nowrap;word-break:normal;overflow-wrap:normal;"
    shell_open = (f'<table role="presentation" class="os-chip" cellpadding="0" cellspacing="0" border="0" width="62" '
                  f'bgcolor="{BLUSH}" style="width:62px;border-collapse:separate;background-color:{BLUSH};border-radius:10px;">'
                  '<tr><td align="center" style="padding:{pad};">')
    shell_close = '</td></tr></table>'
    if big is None:
        inner = (p(top, 13, 17, INK, 700, extra=nowrap) +
                 p(bottom, 13, 17, INK, 700, extra=nowrap))
        return shell_open.format(pad="17px 3px 17px 3px") + inner + shell_close
    # "to Dec 7" / "to Jan 15" wrapped in 62px chips — keep one line via en dash + nbsp
    if isinstance(bottom, str) and bottom.startswith("to "):
        bottom = "&ndash;" + bottom[3:].replace(" ", "&nbsp;")
    bottom_size = 11 if "&ndash;" in (bottom or "") or "&nbsp;" in (bottom or "") else 12
    inner = (p(top, 12, 14, ACCENT, 700, extra=nowrap) +
             p(big, 22, 26, INK, 700, margin="1px 0 0 0", extra=nowrap) +
             p(bottom, bottom_size, 14, BODY, 700, extra=nowrap))
    return shell_open.format(pad="7px 3px 7px 3px") + inner + shell_close


def item(title, lines, featured=False, label=None, first=True):
    out = ""
    if label:
        out += p(label, 13, 18, ACCENT, 700, margin=("0 0 4px 0" if first else "14px 0 4px 0"))
        tmargin = "0"
    else:
        tmargin = "0" if first else "14px 0 0 0"
    tsize, tlh = (18, 25) if featured else (16, 23)
    # Keep date headers readable: no mid-number breaks from mobile word-break CSS
    title_extra = "overflow-wrap:normal;word-break:normal;"
    out += p(title, tsize, tlh, INK, 700, margin=tmargin, extra=title_extra)
    bsize, blh = (16, 24) if featured else (15, 22)
    for ln in lines:
        out += p(ln, bsize, blh, BODY, 400, margin="4px 0 0 0")
    return out


def button(href, label, fill, text_color, align="left"):
    align_attr = f' align="{align}"' if align != "left" else ""
    margin = "margin:0 auto;" if align == "center" else ""
    return (f'<table role="presentation" class="os-btn" cellpadding="0" cellspacing="0" border="0"{align_attr} '
            f'bgcolor="{fill}" style="border-collapse:separate;background-color:{fill};border-radius:999px;{margin}">'
            f'<tr><td align="center" style="padding:13px 26px;">'
            f'<a href="{href}" style="display:block;font-family:{FONT};font-size:16px;line-height:20px;'
            f'color:{text_color};font-weight:700;text-decoration:none;">'
            f'<span style="color:{text_color};">{label}</span></a></td></tr></table>')


def badge(label):
    """Compact ONLINE / IN PERSON / FREE / WEEKLY pill."""
    return (
        f'<td style="padding:0 6px 8px 0;vertical-align:middle;">'
        f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" bgcolor="{BLUSH}" '
        f'style="border-collapse:separate;background-color:{BLUSH};border-radius:999px;">'
        f'<tr><td align="center" style="padding:4px 10px;">'
        f'<span style="font-family:{FONT};font-size:11px;line-height:14px;color:{INK};'
        f'font-weight:700;letter-spacing:0.6px;text-transform:uppercase;white-space:nowrap;">{label}</span>'
        f'</td></tr></table></td>'
    )


def badges_row(labels):
    cells = "".join(badge(lab) for lab in labels)
    return (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        f'style="border-collapse:collapse;margin:0 0 10px 0;"><tr>{cells}</tr></table>'
    )


def group_card(badges, name, when, where, cost, body_paras, btn_href, btn_label):
    """Equal support-group card: badges, name, day/time, location, cost, blurb, one button."""
    body = "".join(p(t, 15, 22, BODY, 400, margin="8px 0 0 0") for t in body_paras)
    inner = (
        badges_row(badges)
        + p(name, 17, 23, INK, 700, margin="0")
        + p(when, 15, 22, BODY, 400, margin="6px 0 0 0")
        + p(where, 15, 22, BODY, 400, margin="2px 0 0 0")
        + p(cost, 15, 22, BODY, 400, margin="2px 0 0 0")
        + body
        + '<div style="margin:14px 0 0 0;">'
        + button(btn_href, btn_label, INK, CREAM).replace('class="os-btn"', 'class="os-btn os-btn-navy"')
        + '</div>'
    )
    return card(inner, pad="16px 18px 16px 18px")


def story_img(src, width, alt, radius=12, link=None, extra_style=""):
    img = (f'<img src="{src}" width="{width}" alt="{alt}" '
           f'style="display:block;width:100%;max-width:{width}px;height:auto;border:0;outline:none;'
           f'text-decoration:none;border-radius:{radius}px;{extra_style}">')
    if link:
        return (f'<a href="{link}" style="display:block;text-decoration:none;border:0;outline:none;">'
                f'{img}</a>')
    return img


def step(n, text):
    return ('<tr><td style="padding:0 0 12px 0;">'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;"><tr>'
            '<td width="30" style="width:30px;vertical-align:top;padding:2px 10px 0 0;">'
            f'<table role="presentation" class="os-stepbg" cellpadding="0" cellspacing="0" border="0" width="26" bgcolor="{INK}" '
            f'style="width:26px;border-collapse:separate;background-color:{INK};border-radius:13px;"><tr>'
            f'<td align="center" style="padding:0;height:26px;">{p(str(n), 13, 26, WHITE, 700, extra="text-align:center;", cls="os-step")}</td></tr></table></td>'
            f'<td style="vertical-align:top;">{p(text, 16, 24, BODY, 400)}</td></tr></table></td></tr>')



def price_boxes():
    """Equal-size VH pay-what-you-can boxes ($0/$10/$20/$35)."""
    boxes = [
        ("$0", "Always<br>welcome"),
        ("$10", "Helps"),
        ("$20", "Suggested"),
        ("$35", "Sponsors<br>another seat"),
    ]
    cells = []
    n = len(boxes)
    for i, (amt, label) in enumerate(boxes):
        if i == 0:
            pad = "0 4px 0 0"
        elif i == n - 1:
            pad = "0 0 0 4px"
        else:
            pad = "0 4px 0 4px"
        # Two-line label slot so short captions still match tall ones
        if "<br>" not in label:
            label_html = f"{label}<br>&nbsp;"
        else:
            label_html = label
        inner = (
            f'<table role="presentation" class="os-paybox" cellpadding="0" cellspacing="0" border="0" width="100%" '
            f'bgcolor="#e4e9f2" height="78" style="width:100%;height:78px;border-collapse:separate;background-color:#e4e9f2;border-radius:12px;">'
            f'<tr><td class="os-paybox" align="center" valign="middle" height="78" style="padding:10px 4px;height:78px;vertical-align:middle;">'
            + p(amt, 20, 24, INK, 700, extra="text-align:center;")
            + p(label_html, 11, 14, BODY, 400, margin="4px 0 0 0", extra="text-align:center;")
            + '</td></tr></table>'
        )
        cells.append(
            f'<td class="os-stack" width="25%" valign="top" height="78" '
            f'style="width:25%;padding:{pad};vertical-align:top;height:78px;">{inner}</td>'
        )
    return (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" '
        'style="width:100%;border-collapse:separate;margin:16px 0 0 0;"><tr>'
        + "".join(cells)
        + '</tr></table>'
        + p("The meeting link is emailed to registrants.", 13, 20, SAND, 400, margin="4px 0 0 0")
    )


def sensory(text, link_html):
    """Legacy helper — T299 feedback: do not emit Sensory: lines; link only."""
    return link_html


SECONDARY_EVENTS = [
    dict(chip=chip("Sat", "3", "Oct"),
         title="Game Day &middot; Autism Tennessee",
         meta="12:00&ndash;3:00 PM &middot; Nashville &middot; Free, food provided &middot; About 45 min",
         sensory="indoor, small-group games for autistic kids, teens, and adults; families welcome.",
         link=("https://autismtn.org/events/EventDetails.aspx?id=2003814", "Register")),
    dict(chip=chip("Sun", "11", "Oct"),
         title="Sensory Sunday Hour &middot; Frist Art Museum",
         meta="12:00&ndash;1:00 PM &middot; Frist Art Museum, Nashville &middot; Free for members and ages 18 and under &middot; About 45 min",
         sensory="gallery sound lowered for the hour, multisensory carts with volunteers.",
         link=("https://fristartmuseum.org/event/sensory-sunday-hour-5/", "Details")),
    dict(chip=chip("Oct", "16", "to Nov 1"),
         title="Boo at the Zoo &middot; Nashville Zoo",
         meta="Nightly 5:00&ndash;9:00 PM &middot; $19&ndash;$23 ages 2+, parking $10 &middot; About 35 min",
         sensory="free Zooper Packs and a social story; Mon&ndash;Wed quietest.",
         link=("https://www.nashvillezoo.org/boo", "Tickets and social story")),
    dict(chip=chip("Sat", "31", "Oct"),
         title="Evergreen Trunk or Treat &middot; Evergreen Life Services",
         meta="1:00&ndash;3:00 PM &middot; Antioch &middot; Free &middot; About 30 min",
         sensory="outdoors; trunks, games, and booths built for IDD families.",
         link=("https://evergreenls.org/trunkortreat/", "Details")),
]

MONSTERS_URL = "https://www.explorethedc.org/event/monsters-in-the-museum/"
DEADLINES_URL = f"{PAGES}deadlines-october-2026.html"
EVENTS_CAL_URL = f"{SITE}/events"

FALL_BREAK = item(
    "Fall break, Oct 5 to 9: Rutherford County and Murfreesboro City Schools",
    ["Both districts are closed all week. RCS conferences Tue Oct 20; MCS conferences Tue Nov 3 (no school). Ask for IEP progress data then. &nbsp;"
     + a("https://www.rcschools.net/o/rcs/page/rcs-academic-calendars", "RCS") + " &nbsp;&middot;&nbsp; "
     + a("https://www.cityschools.net/calendar", "MCS")], featured=True)
VOTER = item(
    "Voter registration deadline: Mon&nbsp;Oct&nbsp;5",
    ["For the Nov 3 election. Register or update your address at GoVoteTN.gov by Mon Oct 5. Early voting Oct 14 to 29. Voters with a disability can request a mail ballot by Sat Oct 24. &nbsp;"
     + a("https://govotetn.gov/", "GoVoteTN")], featured=True, first=False)
CLOCKS = item(
    "Clocks fall back one hour on Sun Nov 1",
    ["Daylight saving time ends at 2:00 AM. If sleep is fragile at your house, shift bedtime 10 to 15 minutes a night the week before. &nbsp;"
     + a("https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst", "How DST works")])

TOP_DEADLINE_ROWS = [
    row(chip("Mon", "5", "Oct"), FALL_BREAK + VOTER, featured=True),
    row(chip("Sun", "1", "Nov"), CLOCKS, last=True),
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
NOTE = " ".join(NOTE_PARAS)  # plain-text export
ALONE_PHRASE = "you do not have to figure everything out alone"
IN_THIS_ISSUE = "Fall break &middot; Parent support &middot; Sensory-friendly events &middot; New resources"

ABOUT = ("A village for families like ours in Murfreesboro and surrounding areas: free guides, a local "
         "Resource Directory, sensory-friendly events, and a parent community. Built around autism and open "
         "to every kind of difference and disability.")

NUMBERS = [
    (b("988") + " &middot; Call or text any hour."),
    (b("STEP TN") + " (IEP help): " + tel("800-280-7837", "+18002807837")
     + " / Espa&ntilde;ol " + tel("800-975-2919", "+18009752919") + "."),
    (b("Disability Rights TN:") + " " + tel("800-342-1660", "+18003421660") + "."),
]


def head():
    css = """
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;700&display=swap');
:root{color-scheme:light only;supported-color-schemes:light;}
a[x-apple-data-detectors]{color:inherit !important;text-decoration:none !important;}
u + #os-body a{color:ACCENT;text-decoration:underline;}
@media only screen and (max-width:620px){
  html,body{width:100% !important;max-width:100% !important;overflow-x:hidden !important;-webkit-text-size-adjust:100% !important;}
  .os-wrap,.os-wrap table{width:100% !important;max-width:100% !important;}
  table[width="600"]{width:100% !important;max-width:100% !important;}
  .os-pad{padding-left:20px !important;padding-right:20px !important;}
  .os-cardpad{padding-left:16px !important;padding-right:16px !important;}
  .os-h1{font-size:27px !important;line-height:33px !important;}
  .os-h2{font-size:20px !important;line-height:26px !important;}
  .os-col{display:block !important;width:100% !important;max-width:100% !important;}
  .os-col-photo{padding:0 0 16px 0 !important;}
  .os-photo{width:100% !important;max-width:160px !important;height:auto !important;}
  .os-intro-photo{width:72px !important;max-width:72px !important;height:72px !important;border-radius:50% !important;}
  .os-intro-col{display:block !important;width:100% !important;max-width:100% !important;}
  .os-intro-photocell{padding:0 0 12px 0 !important;text-align:left !important;}
  body,table,td,p,a,span{overflow-wrap:anywhere !important;word-break:break-word !important;}
  .os-chip,.os-chip p,table[width="62"] p,td[width="62"] p{white-space:nowrap !important;overflow-wrap:normal !important;word-break:normal !important;}
  .os-paybox,.os-paybox p{overflow-wrap:normal !important;word-break:normal !important;}
  img{max-width:100% !important;height:auto !important;}
  table[width="62"],td[width="62"]{width:62px !important;max-width:62px !important;}
  table[width="26"],td[width="30"]{width:26px !important;max-width:30px !important;}
  table[width="40"]{width:40px !important;max-width:40px !important;}
  table[width="160"]{width:160px !important;max-width:160px !important;}
}
""".replace("ACCENT", ACCENT)
    dark = f"""
[data-ogsb] .os-bg{{background-color:{CREAM} !important;}} [data-ogsb] .os-card{{background-color:{WHITE} !important;}} [data-ogsb] .os-chip{{background-color:{BLUSH} !important;}} [data-ogsb] .os-navy{{background-color:{INK} !important;}} [data-ogsb] .os-btn-navy{{background-color:{INK} !important;}} [data-ogsb] .os-btn-gold{{background-color:{GOLD} !important;}} [data-ogsb] .os-stepbg{{background-color:{INK} !important;}} [data-ogsb] .os-rulebar{{background-color:{ACCENT} !important;}} [data-ogsb] .os-photocell{{background-color:{BLUSH} !important;}}
[data-ogsc] .os-ink{{color:{INK} !important;}} [data-ogsc] .os-body{{color:{BODY} !important;}} [data-ogsc] .os-muted{{color:{MUTED} !important;}} [data-ogsc] .os-accent,[data-ogsc] .os-link{{color:{ACCENT} !important;}} [data-ogsc] .os-gold{{color:{GOLD} !important;}} [data-ogsc] .os-sand{{color:{SAND} !important;}} [data-ogsc] .os-cream{{color:{CREAM} !important;}} [data-ogsc] .os-white,[data-ogsc] .os-step{{color:{WHITE} !important;}}
@media (prefers-color-scheme: dark){{
  .os-bg{{background-color:{CREAM} !important;}} .os-card{{background-color:{WHITE} !important;}} .os-chip{{background-color:{BLUSH} !important;}} .os-navy{{background-color:{INK} !important;}} .os-btn-navy{{background-color:{INK} !important;}} .os-btn-gold{{background-color:{GOLD} !important;}} .os-stepbg{{background-color:{INK} !important;}} .os-rulebar{{background-color:{ACCENT} !important;}} .os-photocell{{background-color:{BLUSH} !important;}}
  .os-ink{{color:{INK} !important;}} .os-body{{color:{BODY} !important;}} .os-muted{{color:{MUTED} !important;}} .os-accent,.os-link{{color:{ACCENT} !important;}} .os-gold{{color:{GOLD} !important;}} .os-sand{{color:{SAND} !important;}} .os-cream{{color:{CREAM} !important;}} .os-white,.os-step{{color:{WHITE} !important;}}
}}
"""
    return f'''<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light only"><meta name="supported-color-schemes" content="light">
<title>{SUBJECT}</title>
<!-- MailerLite: Subject "{SUBJECT}". Merge tags {{$url}} and {{$unsubscribe}}. Plain text: newsletter-october-2026.txt. -->
<!-- Built by tools/build-october-2026.py. Edit that file, not this one. T299 Hickok feedback pass. -->
<!-- T355: Hickok intro + Connect with Other Local Parents support cards. Audience = parents/caregivers of neurodivergent children. -->
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;700&amp;display=swap" rel="stylesheet">
<style type="text/css">
{css}
{dark}
</style>
<!--[if mso]>
<style type="text/css">body,table,td,p,a,span{{font-family:Arial,Helvetica,sans-serif !important;}} p,td,a,span{{mso-line-height-rule:exactly;}}</style>
<![endif]-->
</head>'''


def build_html(base):
    art = lambda f: f"{base}art/{f}"
    o = []
    o.append(head())
    o.append(f'<body id="os-body" class="os-bg" bgcolor="{CREAM}" style="margin:0;padding:0;background-color:{CREAM};width:100%;max-width:100%;overflow-x:hidden;">')
    o.append(f'<span style="display:none;font-size:1px;color:{CREAM};line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{PREHEADER}</span>')
    o.append(f'<table role="presentation" class="os-bg" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="{CREAM}" style="width:100%;border-collapse:collapse;background-color:{CREAM};">'
             '<tr><td align="center" style="padding:20px 12px 40px 12px;">'
             '<table role="presentation" class="os-wrap" cellpadding="0" cellspacing="0" border="0" width="600" style="width:100%;max-width:600px;border-collapse:collapse;">')

    vib = ('<a class="os-muted" href="{$url}" style="color:' + MUTED + ';text-decoration:underline;">View in browser</a>')
    o.append(padrow(p(vib, 12, 17, MUTED, 400, extra="text-align:center;"), pad="0 34px 12px 34px"))

    o.append(padrow(
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;"><tr>'
        f'<td align="left" style="vertical-align:middle;">{p("Our Special Village", 12, 16, ACCENT, 700, extra="letter-spacing:1.6px;text-transform:uppercase;")}</td>'
        f'<td align="right" style="vertical-align:middle;">{p("October 2026", 13, 16, MUTED, 700, extra="text-align:right;")}</td>'
        '</tr></table>', pad="0 34px 14px 34px"))

    o.append('<tr><td align="left" style="padding:0;">'
             f'<img src="{art("newsletter-fall.jpg")}" width="600" alt="Illustration of the village in autumn: homes, a gazebo, shops, and neighbors walking the path." '
             'style="display:block;width:100%;max-width:600px;height:auto;border:0;outline:none;text-decoration:none;border-radius:16px;"></td></tr>')
    o.append(sp(18))
    o.append(padrow(
        f'<h1 class="os-h1 os-ink" style="margin:0;font-family:{FONT};font-size:30px;line-height:36px;'
        f'mso-line-height-rule:exactly;color:{INK};font-weight:700;letter-spacing:-0.3px;">October in Our Special Village</h1>'))

    o.append(sp(14))
    # T355 intro: regular body font (not italic), tighter spacing, circular photo, alone highlight, issue line
    alone_hi = (
        f'<span style="background-color:{BLUSH};color:{INK};padding:1px 4px;border-radius:4px;">'
        f'{ALONE_PHRASE}</span>'
    )
    note_paras_html = []
    for i, para in enumerate(NOTE_PARAS):
        html_para = para.replace(ALONE_PHRASE, alone_hi) if ALONE_PHRASE in para else para
        note_paras_html.append(p(html_para, 16, 24, BODY, 400, margin=("0" if i == 0 else "8px 0 0 0")))
    note_copy = "".join(note_paras_html)
    note_copy += p("With love,", 16, 24, BODY, 400, margin="12px 0 2px 0")
    note_copy += (
        f'<img src="{art("signature-taylor.png")}" width="96" height="55" alt="Taylor" '
        f'style="display:block;width:96px;max-width:96px;height:auto;margin:0;padding:0;border:0;outline:none;'
        f'text-decoration:none;font-family:Georgia, Times New Roman, serif;font-size:22px;font-style:italic;color:{ACCENT};">'
    )
    photo = (
        f'<img class="os-intro-photo" src="{art("taylor-hickok-160.jpg")}" width="72" height="72" '
        f'alt="Dr. Taylor Hickok, founder of Our Special Village." '
        f'style="display:block;width:72px;max-width:72px;height:72px;margin:0;padding:0;border:0;outline:none;'
        f'text-decoration:none;border-radius:50%;object-fit:cover;">'
    )
    intro = (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" '
        'style="width:100%;border-collapse:collapse;"><tr>'
        f'<td class="os-intro-col" align="left" valign="top" style="vertical-align:top;padding:0 14px 0 0;">{note_copy}</td>'
        f'<td class="os-intro-col os-intro-photocell" width="72" align="right" valign="top" '
        f'style="width:72px;vertical-align:top;padding:4px 0 0 0;">{photo}</td>'
        '</tr></table>'
        + p(f'<b style="color:{ACCENT};font-weight:700;">In this issue</b> &nbsp;{IN_THIS_ISSUE}',
            13, 20, MUTED, 400, margin="14px 0 0 0")
    )
    o.append(padrow(intro))

    o.append(sp(28))
    o.append(section_head("deadlines", "Three things to know this month"))
    o.append(sp(16))
    o.append(padrow(card(rows_table(TOP_DEADLINE_ROWS))))
    o.append(sp(14))
    o.append(padrow(
        button(DEADLINES_URL, "See all deadlines", INK, CREAM).replace('class="os-btn"', 'class="os-btn os-btn-navy"')
        + p("Dates confirmed Sept 14. If something changed, reply and we will fix it.", 13, 20, MUTED, 400, margin="12px 0 0 0")))

    o.append(sp(40))
    o.append(section_head("events", "The month ahead", "Picked for sensory-sensitive kids and their families. Drive times are from Murfreesboro."))
    o.append(sp(16))

    featured_art = story_img(
        art("featured-monsters-museum.jpg"), 560,
        "Family exploring a friendly museum dinosaur exhibit at a calm after-hours sensory night; one child wears headphones",
        radius=12, link=MONSTERS_URL)
    featured_copy = (p("Featured", 13, 18, ACCENT, 700, margin="14px 0 4px 0")
                     + p("All Access Night: Monsters in the Museum &middot; Discovery Center", 18, 25, INK, 700)
                     + p("Thu Oct 15 &middot; 6:00&ndash;8:00 PM &middot; Murfreesboro &middot; Free, registration required", 16, 24, BODY, 400, margin="4px 0 0 0")
                     + p(a(MONSTERS_URL, "Reserve your spot"), 16, 24, BODY, 400, margin="4px 0 0 0"))
    o.append(padrow(card(featured_art + featured_copy, pad="12px 20px 18px 20px")))

    o.append(sp(20))
    ev_rows = []
    for i, e in enumerate(SECONDARY_EVENTS):
        content = item(e["title"], [e["meta"] + " &nbsp;" + a(*e["link"])])
        ev_rows.append(row(e["chip"], content, last=(i == len(SECONDARY_EVENTS) - 1)))
    o.append(padrow(card(rows_table(ev_rows))))
    o.append(sp(16))
    o.append(padrow(button(EVENTS_CAL_URL, "View the full October events calendar", INK, CREAM, align="center").replace('class="os-btn"', 'class="os-btn os-btn-navy"')))

    o.append(sp(40))
    o.append(section_head("library", "New in the library"))
    o.append(sp(16))
    therapy_img = (
        f'<img src="{art("guide-therapy-styles-landscape.jpg")}" '
        f'srcset="{art("guide-therapy-styles-landscape-280.jpg")} 280w, {art("guide-therapy-styles-landscape.jpg")} 490w" '
        f'sizes="(max-width:620px) 280px, 490px" width="490" height="260" '
        f'alt="Adult and child sharing a calm sensory play tray in a warm playroom" '
        f'style="display:block;width:100%;max-width:490px;height:auto;border:0;outline:none;text-decoration:none;border-radius:12px;margin:0 0 12px 0;">'
    )
    therapy = (therapy_img
               + p("New guide, reviewed Sept 2026", 13, 18, ACCENT, 700, margin="0 0 4px 0")
               + p("Therapy styles: play, structure, and compliance", 17, 24, INK, 700)
               + p("Two therapists can have the same license and run completely different rooms. Learn what the common labels actually look like.", 15, 22, BODY, 400, margin="6px 0 0 0")
               + p(a(f"{SITE}/resources/therapy-styles", "Read the guide"), 15, 22, BODY, 400, margin="10px 0 0 0"))
    o.append(padrow(card(therapy, pad="12px 20px 16px 20px")))
    o.append(sp(16))
    grief_img = (
        f'<img src="{art("guide-grief-landscape.jpg")}" '
        f'srcset="{art("guide-grief-landscape-280.jpg")} 280w, {art("guide-grief-landscape.jpg")} 490w" '
        f'sizes="(max-width:620px) 280px, 490px" width="490" height="260" '
        f'alt="Parent on a porch in autumn while a child plays nearby in leaves - quiet and hopeful" '
        f'style="display:block;width:100%;max-width:490px;height:auto;border:0;outline:none;text-decoration:none;border-radius:12px;margin:0 0 12px 0;">'
    )
    grief = (grief_img
             + p("New guide, reviewed Sept 2026", 13, 18, ACCENT, 700, margin="0 0 4px 0")
             + p("Grief and disability: the loss nobody sends a card for", 17, 24, INK, 700)
             + p("This kind of grief rarely has an occasion attached. It shows up at a birthday, a missed milestone, or in the parking lot after an evaluation.", 15, 22, BODY, 400, margin="6px 0 0 0")
             + p(a(f"{SITE}/resources/grieving-the-life-you-imagined", "Read the grief guide"), 15, 22, BODY, 400, margin="10px 0 0 0"))
    o.append(padrow(card(grief, pad="12px 20px 16px 20px")))

    o.append(sp(40))
    o.append(section_head("question", "One question, answered",
                          "One real question from a local parent, answered plainly. " + a(f"{SITE}/contact", "Send us yours")))
    o.append(sp(16))
    steps = rows_table([
        step(1, f'{b("Put it in writing.")} Email the case manager and copy the principal: name what is missing, quote the IEP, ask for a fix by a date, and request service logs.'),
        step(2, f'{b("Ask for an IEP team meeting.")} Request one in writing any time. If things stall, copy the district special education director. Bring notes and a friend.'),
        step(3, f'{b("Use free state help.")} File a TDOE administrative complaint (no lawyer, decision in 60 days), or call STEP TN at {tel("800-280-7837", "+18002807837")}.'),
    ])
    qa = (p("October&rsquo;s question", 13, 18, ACCENT, 700, margin="0 0 6px 0")
          + p("&ldquo;What do I do if my child&rsquo;s IEP isn&rsquo;t being followed?&rdquo;", 18, 25, INK, 700)
          + p("An IEP is legally binding. The school has to deliver what is written in it.", 16, 24, BODY, 400, margin="12px 0 12px 0")
          + steps
          + p(a(f"{SITE}/resources/iep-504", "IEP &amp; 504 guide") + " &nbsp;&middot;&nbsp; " + a("https://www.tn.gov/education/legal-services/special-education-legal-services/legal-dispute-resolution-processes.html", "TDOE dispute options"), 15, 22, BODY, 400, margin="4px 0 0 0")
          + p("Parent-to-parent guidance, not legal advice.", 13, 20, MUTED, 400, margin="10px 0 0 0"))
    o.append(padrow(card(qa, pad="16px 20px 16px 20px")))

    o.append(sp(16))
    vh_art = story_img(
        art("village-hall-iep.jpg"), 600,
        "Parents gathered around a table with a laptop for an online IEP workshop - autumn village setting",
        radius=12)
    o.append(padrow(vh_art, pad="0 0 0 0"))
    o.append(sp(12))
    # Extended Village Hall from prior iteration (Topic and guest + pricing), still under IEP art
    mercedes = (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" '
        'style="width:100%;border-collapse:collapse;margin:0 0 16px 0;"><tr>'
        f'<td class="os-stack" width="96" valign="top" style="width:96px;padding:0 14px 0 0;vertical-align:top;">'
        f'<img src="{art("mercedes-lawson-160.jpg")}" width="96" height="138" '
        f'alt="Mercedes Lawson, M.S. Ed., founder of A.C.C.E.S.S." '
        f'style="display:block;width:96px;max-width:96px;height:auto;border:0;outline:none;text-decoration:none;border-radius:10px;">'
        f'</td><td class="os-stack" valign="top" style="padding:0;vertical-align:top;">'
        + p("Mercedes Lawson, M.S. Ed.", 13, 18, GOLD, 700, margin="0 0 4px 0")
        + p("Founder of A.C.C.E.S.S. in Greater Nashville. She grew up with a sibling with disabilities, "
           "taught special education for nine years helping 250+ students, and has a child with Autism.",
           14, 21, SAND, 400)
        + '</td></tr></table>'
    )
    vh = (f'<table role="presentation" class="os-navy" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="{INK}" style="width:100%;border-collapse:separate;background-color:{INK};border-radius:16px;">'
          '<tr><td align="left" style="padding:26px 26px 26px 26px;">'
          + p("Saturday, October 10, 2026", 13, 18, GOLD, 700, margin="0 0 6px 0")
          + p("9:30 to 11:00 AM Central, Online<br>Pay what you can, including nothing", 16, 24, SAND, 400, margin="0 0 18px 0")
          + p("Topic and guest", 13, 18, GOLD, 700, margin="0 0 6px 0")
          + p("The IEP process and navigating the school system, with Mercedes Lawson of A.C.C.E.S.S.", 20, 27, CREAM, 700, margin="0 0 12px 0")
          + mercedes
          + p("A 45-minute lesson on how the IEP process works and how to navigate the school system, then live parent questions. The lesson is recorded and sent to registrants; the Q&amp;A is not.", 16, 24, SAND, 400, margin="0 0 20px 0")
          + button(f"{SITE}/village-hall", "Register for Village Hall", GOLD, INK).replace('class="os-btn"', 'class="os-btn os-btn-gold"')
          + price_boxes()
          + '</td></tr></table>')
    o.append(padrow(vh))

    o.append(sp(40))
    o.append(section_head("ongoing", "Connect with Other Local Parents"))
    o.append(sp(16))
    online_card = group_card(
        ["ONLINE", "FREE", "WEEKLY"],
        "Our Special Village Online Parent Group",
        "Thursdays &middot; 7:00&ndash;8:00 PM Central",
        "Online",
        "Free",
        [
            "Connect with other parents and caregivers of neurodivergent and disabled children "
            "in a welcoming, judgment-free space. A formal diagnosis is not required.",
            "Join us beginning Thursday, October 1 &ndash; or drop in on any Thursday that works for your family.",
            "Cameras are optional, and meetings are never recorded.",
        ],
        f"{SITE}/group",
        "Join the Online Group",
    )
    werock_card = group_card(
        ["IN PERSON", "FREE", "WEEKLY"],
        "We Rock the Spectrum Parent Group",
        "Wednesdays &middot; 5:00 PM",
        "We Rock the Spectrum Murfreesboro &middot; 820 N. Thompson Lane, Murfreesboro",
        "Parent group: Free",
        [
            "Led by Cari Parr. This in-person group gives parents and caregivers an opportunity "
            "to connect while children play in the gym.",
            "Parents stay with and supervise their children during gym play (this is not included childcare). "
            "Discounted gym admission is available for children.",
            f"Questions? Call {tel('(615) 962-8627', '+16159628627')} or email "
            f"{a('mailto:info@werockthespectrummurfreesboro.com', 'info@werockthespectrummurfreesboro.com', nowrap=False)}.",
        ],
        "mailto:info@werockthespectrummurfreesboro.com",
        "Contact We Rock the Spectrum",
    )
    o.append(padrow(online_card))
    o.append(sp(16))
    o.append(padrow(werock_card))

    o.append(sp(40))
    about_copy = ((f'<h2 class="os-ink" style="margin:0;font-family:{FONT};font-size:17px;line-height:23px;'
                   f'mso-line-height-rule:exactly;color:{INK};font-weight:700;">About Our Special Village</h2>')
                  + p(ABOUT, 14, 21, BODY, 400, margin="8px 0 0 0")
                  + p(a(f"{SITE}/about", "About the Village") + " &nbsp;&middot;&nbsp; " + a(f"{SITE}/editorial-policy", "How we check information"), 14, 21, BODY, 400, margin="10px 0 0 0"))
    photo = (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="160" class="os-photocell" bgcolor="{BLUSH}" '
             f'style="width:160px;border-collapse:separate;background-color:{BLUSH};border-radius:12px;margin:0 auto;">'
             f'<tr><td class="os-photocell" align="center" style="width:160px;vertical-align:middle;border-radius:12px;">'
             f'<img class="os-photo" src="{art("about-family-bowling-small.jpg")}" width="160" height="160" alt="Taylor, her husband, and their daughter at a bowling alley." '
             f'style="display:block;width:160px;max-width:100%;height:auto;margin:0 auto;border:0;outline:none;text-decoration:none;border-radius:12px;font-family:{FONT};font-size:13px;line-height:18px;color:{BODY};"></td></tr></table>')
    # Stacked + centered photo (T299 feedback), then About copy
    about = (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;">'
        f'<tr><td align="center" style="padding:0 0 14px 0;">{photo}</td></tr>'
        f'<tr><td align="left" style="padding:0;">{about_copy}</td></tr>'
        '</table>'
    )
    o.append(padrow(card(about, pad="16px 18px 16px 18px")))

    o.append(sp(16))
    nums = p("Numbers worth keeping", 14, 20, ACCENT, 700, margin="0 0 4px 0") + "".join(
        p(t, 14, 20, BODY, 400, margin="4px 0 0 0") for t in NUMBERS)
    o.append(padrow(card(nums, pad="12px 18px 14px 18px")))

    o.append(sp(22))
    o.append(padrow(p("Know a family who could use this? Forward it along. Anyone can join at "
                      + a(f"{SITE}/newsletter", "ourspecialvillagetn.com/newsletter", nowrap=False) + ".", 14, 21, BODY, 400, extra="text-align:center;")))

    o.append(sp(28))
    o.append(f'<tr><td class="os-pad" style="padding:0 34px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;"><tr><td class="os-rule" style="border-top:1px solid {HAIR};font-size:0;line-height:0;height:1px;">&nbsp;</td></tr></table></td></tr>')
    o.append(sp(18))
    footer = (p("Our Special Village &middot; Murfreesboro and surrounding areas, Tennessee", 14, 21, INK, 700, margin="0 0 6px 0")
              + p("Local businesses and practices help keep the Village free and ad-free. " + a(f"{SITE}/sponsors", "Sponsorship options", nowrap=False) + ".", 13, 20, BODY, 400, margin="0 0 12px 0")
              + p("You are receiving this because you joined the newsletter list at ourspecialvillagetn.com.<br>"
                  + a("{$unsubscribe}", "Unsubscribe in one click", nowrap=False) + " &nbsp;&middot;&nbsp; " + a(f"{SITE}/privacy", "Privacy") + " &nbsp;&middot;&nbsp; " + a(f"{SITE}/contact", "Contact"), 12, 20, BODY, 400, margin="0 0 10px 0")
              + p("Our Special Village is owned and operated by Little Luminaries Therapy Services, PLLC<br>1810 Ward Dr, Suite 101, Murfreesboro, TN 37129", 12, 18, BODY, 400))
    o.append(padrow(footer))

    o.append('</table></td></tr></table></body></html>')
    return "\n".join(o) + "\n"


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
    w("  Both districts are closed all week. RCS conferences Tue Oct 20; MCS conferences Tue Nov 3 (no school). Ask for IEP progress data then.")
    w("  RCS: https://www.rcschools.net/o/rcs/page/rcs-academic-calendars")
    w("  MCS: https://www.cityschools.net/calendar")
    w("")
    w("Mon Oct 5 · Voter registration deadline: Mon Oct 5")
    w("  For the Nov 3 election. Register or update at GoVoteTN.gov by Mon Oct 5. Early voting Oct 14 to 29. Disability mail-ballot requests by Sat Oct 24.")
    w("  https://govotetn.gov/")
    w("")
    w("Sun Nov 1 · Clocks fall back one hour")
    w("  If sleep is fragile, shift bedtime 10 to 15 minutes a night the week before.")
    w("  https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst")
    w("")
    w(f"See all deadlines: {DEADLINES_URL}")
    w("Dates confirmed Sept 14. If something changed, reply and we will fix it.")
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
        w(f"  {e['link'][1]}: {e['link'][0]}")
        w("")
    w(f"View the full October events calendar: {EVENTS_CAL_URL}")
    w("")
    w("----------------------------------------")
    w("NEW IN THE LIBRARY")
    w("")
    w("New guide, reviewed Sept 2026 · Therapy styles: play, structure, and compliance")
    w("  Two therapists can have the same license and run completely different rooms. Learn what the common labels actually look like.")
    w(f"  Read the guide: {SITE}/resources/therapy-styles")
    w("")
    w("New guide, reviewed Sept 2026 · Grief and disability: the loss nobody sends a card for")
    w("  This kind of grief rarely has an occasion attached. It shows up at a birthday, a missed milestone, or in the parking lot after an evaluation.")
    w(f"  Read the grief guide: {SITE}/resources/grieving-the-life-you-imagined")
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
    w("3. Use free state help. File a TDOE administrative complaint, or call STEP TN at 800-280-7837.")
    w("")
    w(f"IEP & 504 guide: {SITE}/resources/iep-504")
    w("TDOE dispute options: https://www.tn.gov/education/legal-services/special-education-legal-services/legal-dispute-resolution-processes.html")
    w("Parent-to-parent guidance, not legal advice.")
    w("")
    w("Village Hall: Saturday, October 10, 2026")
    w("9:30 to 11:00 AM Central, Online")
    w("Pay what you can, including nothing")
    w("Topic and guest: The IEP process and navigating the school system, with Mercedes Lawson of A.C.C.E.S.S.")
    w("Mercedes Lawson, M.S. Ed. - Founder of A.C.C.E.S.S. in Greater Nashville. She grew up with a sibling with disabilities, taught special education for nine years helping 250+ students, and has a child with Autism.")
    w("A 45-minute lesson, then live parent questions. Lesson recorded; Q&A is not.")
    w("Pay what you can (equal boxes): $0 Always welcome / $10 Helps / $20 Suggested / $35 Sponsors another seat")
    w("The meeting link is emailed to registrants.")
    w(f"Register for Village Hall: {SITE}/village-hall")
    w("")
    w("----------------------------------------")
    w("CONNECT WITH OTHER LOCAL PARENTS")
    w("")
    w("Our Special Village Online Parent Group · ONLINE · FREE · WEEKLY")
    w("  Thursdays · 7:00-8:00 PM Central · Online · Free")
    w("  Connect with other parents and caregivers of neurodivergent and disabled children in a welcoming, judgment-free space. A formal diagnosis is not required.")
    w("  Join us beginning Thursday, October 1 - or drop in on any Thursday that works for your family.")
    w("  Cameras are optional, and meetings are never recorded.")
    w(f"  Join the Online Group: {SITE}/group")
    w("")
    w("We Rock the Spectrum Parent Group · IN PERSON · FREE · WEEKLY")
    w("  Wednesdays · 5:00 PM · We Rock the Spectrum Murfreesboro · 820 N. Thompson Lane, Murfreesboro")
    w("  Parent group: Free · Led by Cari Parr")
    w("  This in-person group gives parents and caregivers an opportunity to connect while children play in the gym.")
    w("  Parents stay with and supervise their children during gym play (this is not included childcare). Discounted gym admission is available for children.")
    w("  Questions? Call (615) 962-8627 or email info@werockthespectrummurfreesboro.com.")
    w("  Contact We Rock the Spectrum: mailto:info@werockthespectrummurfreesboro.com")
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
    w("988 · Call or text any hour.")
    w("STEP TN (IEP help): 800-280-7837 / Español 800-975-2919.")
    w("Disability Rights TN: 800-342-1660.")
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
    if isinstance(moy, str) and moy.startswith("to "):
        moy = "&ndash;" + moy[3:].replace(" ", "&nbsp;")
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
            "Oct", "15", "to Dec 7",
            "Medicare open enrollment: Oct&nbsp;15&ndash;Dec&nbsp;7",
            'Compare or switch drug and Advantage plans for 2027. TN SHIP: 1-877-801-0044. '
            '<a href="https://www.medicare.gov/health-drug-plans/open-enrollment">Medicare.gov</a>'),
        deadline_item(
            "Nov", "1", "to Jan 15",
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
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;700&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0;padding:24px 16px 48px;background:{CREAM};color:{BODY};font-family:{FONT};line-height:1.5;}}
main{{max-width:640px;margin:0 auto;}}
h1{{color:{INK};font-size:28px;margin:0 0 8px;}}
h2{{color:{INK};font-size:18px;margin:28px 0 10px;}}
.meta{{color:{MUTED};font-size:14px;margin:0 0 24px;}}
.item{{display:flex;gap:14px;align-items:flex-start;background:{WHITE};border:1px solid {HAIR};border-radius:12px;padding:14px 16px;margin:0 0 10px;}}
.chip{{flex:0 0 62px;width:62px;background:{BLUSH};border-radius:10px;text-align:center;padding:7px 3px;box-sizing:border-box;}}
.chip .dow,.chip .dom,.chip .moy{{white-space:nowrap;overflow-wrap:normal;word-break:normal;}}
.chip .dow{{color:{ACCENT};font-size:12px;line-height:14px;font-weight:700;}}
.chip .dom{{color:{INK};font-size:22px;line-height:26px;font-weight:700;margin:1px 0 0;}}
.chip .moy{{color:{BODY};font-size:11px;line-height:14px;font-weight:700;}}
.body{{flex:1;min-width:0;}}
.body strong{{color:{INK};display:block;margin-bottom:4px;font-size:16px;overflow-wrap:normal;word-break:normal;}}
a{{color:{ACCENT};font-weight:700;}}
.back{{margin:0 0 20px;font-size:14px;}}
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
    html = build_html(args.base)
    txt = build_text()
    deadlines = build_deadlines_page()
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    for name in ("newsletter-october-subscriber-preview.html", "index.html"):
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(html)
    with open(os.path.join(out, "newsletter-october-2026.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    with open(os.path.join(out, "deadlines-october-2026.html"), "w", encoding="utf-8") as f:
        f.write(deadlines)
    for s in (html, txt):
        assert "—" not in s and "&mdash;" not in s, "em dash found"
        assert "{$url}" in s and "{$unsubscribe}" in s
        assert "Village Picks" not in s
        assert "Microsoft Teams" not in s
        assert "art/icons/" not in s
        assert "Wall of Hope" not in s
        assert "autumn-events-collage" not in s
    assert 'alt="Taylor"' in html
    assert "about-family-bowling-small.jpg" in html
    assert "featured-monsters-museum.jpg" in html
    assert "guide-therapy-styles-landscape.jpg" in html
    assert "guide-grief-landscape.jpg" in html
    assert "village-hall-iep.jpg" in html
    assert "Three things to know this month" in html
    assert "See all deadlines" in html
    assert "View the full October events calendar" in html
    assert "Connect with Other Local Parents" in html
    assert "Support groups in Murfreesboro" not in html
    assert "Every week" not in html
    assert "Ongoing this month" not in html
    assert html.count("Register for Village Hall") == 1
    assert "In this issue" in html
    assert "Fall break &middot; Parent support &middot; Sensory-friendly events &middot; New resources" in html
    assert "Welcome to Our Special Village!" in html
    assert "Welcome to the Our Special Village family!" not in html
    assert "October in Our Special Village" in html
    assert "October gets full fast" not in html
    assert "Sensory:" not in html
    assert "Voter registration deadline: Mon&nbsp;Oct&nbsp;5" in html
    assert "Topic and guest" in html
    assert "Sponsors<br>another seat" in html or "Sponsors another seat" in html
    # FEEDBACK-2: Village Hall navy card must never use interpunct dots
    assert "9:30 to 11:00 AM Central, Online" in html
    assert "9:30 to 11:00 AM Central &middot;" not in html
    assert "Always<br>welcome" in html and "Helps" in html and "Suggested" in html
    assert "os-paybox" in html
    assert "$0 always welcome &middot;" not in html
    assert "45-minute lesson" in html
    assert "mercedes-lawson-160.jpg" in html
    assert "taylor-hickok-160.jpg" in html
    assert "A formal diagnosis is not required" in html
    assert "Neurodivergent parents, you are welcome too" not in html
    assert "whether your child struggles a little or a lot" not in html
    assert "I&rsquo;m neurodivergent myself" not in html
    assert "Join the Online Group" in html
    assert "Contact We Rock the Spectrum" in html
    assert "Led by Cari Parr" in html
    assert "Parents stay with and supervise their children" in html
    assert "not included childcare" in html
    assert 'class="chip"' in deadlines
    assert "Sun" in deadlines and "Nov" in deadlines
    assert "Join us beginning Thursday, October 1" in html
    assert 'width="96"' in html and "signature-taylor.png" in html
    assert 'align="center"' in html and "about-family-bowling-small.jpg" in html
    # Intro body must not be wholesale italic (signature PNG may keep italic fallback font).
    intro_slice = html.split("October in Our Special Village", 1)[1].split("Three things to know this month", 1)[0]
    assert "font-style:italic" not in intro_slice.replace("signature-taylor.png", "").split("With love")[0]
    text = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&\w+;", " ", text)
    words = len(text.split())
    # T355 adds intro + equal support cards; keep readable length.
    assert 900 <= words <= 1550, f"word count {words} outside 900-1550"
    print(f"wrote {out}: html {len(html.encode('utf-8'))} bytes, txt {len(txt.encode('utf-8'))} bytes, words≈{words}")


if __name__ == "__main__":
    main()
