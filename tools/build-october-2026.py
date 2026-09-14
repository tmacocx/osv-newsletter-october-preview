#!/usr/bin/env python3
"""Build the October 2026 Our Special Village newsletter (T303 + T323 visual storytelling).

Writes newsletter-october-subscriber-preview.html, an identical index.html, and
newsletter-october-2026.txt (plain-text alternative for the MailerLite send).

Edit this file and run it. Do not hand-edit the generated HTML.

    python3 tools/build-october-2026.py                       # into the repo root
    python3 tools/build-october-2026.py --base art/ --out /tmp # relative art, elsewhere

No dependencies beyond the standard library.
"""
import argparse
import os

PAGES = "https://tmacocx.github.io/osv-newsletter-october-preview/"
SITE = "https://ourspecialvillagetn.com"

# Palette (all text/background pairs used are at or above 4.5:1, see research notes)
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
PREHEADER = ("Two deadlines land Monday, October 5. Plus sensory-friendly fall outings with drive times, "
             "two new guides, and one IEP question answered.")


# ---------------------------------------------------------------- helpers

def p(text, size=16, lh=24, color=BODY, weight=400, margin="0", extra="", cls=""):
    classes = " ".join(c for c in [CLASS_FOR.get(color, ""), cls] if c)
    w = f"font-weight:{weight};" if weight != 400 else ""
    return (f'<p class="{classes}" style="margin:{margin};font-family:{FONT};font-size:{size}px;'
            f'line-height:{lh}px;mso-line-height-rule:exactly;color:{color};{w}{extra}">{text}</p>')


def b(text, color=INK):
    return f'<b class="{CLASS_FOR.get(color, "")}" style="color:{color};font-weight:700;">{text}</b>'


def a(href, label, nowrap=True):
    """Every link, including tel: and mailto:, gets the same terracotta treatment."""
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


def subhead(text, first=True):
    return p(text, 14, 20, ACCENT, 700, margin=("10px 0 2px 0" if first else "0 0 2px 0"))


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
    """Date chip. Single date: weekday / day / month. Range: month / day / "to Dec 7".
    Undated: two short words. Normal case throughout (no letter-spaced caps)."""
    shell_open = (f'<table role="presentation" class="os-chip" cellpadding="0" cellspacing="0" border="0" width="62" '
                  f'bgcolor="{BLUSH}" style="width:62px;border-collapse:separate;background-color:{BLUSH};border-radius:10px;">'
                  '<tr><td align="center" style="padding:{pad};">')
    shell_close = '</td></tr></table>'
    if big is None:
        # two-word text chip, e.g. "Any" / "time"
        inner = (p(top, 13, 17, INK, 700, extra="text-align:center;") +
                 p(bottom, 13, 17, INK, 700, extra="text-align:center;"))
        return shell_open.format(pad="17px 3px 17px 3px") + inner + shell_close
    top_color = ACCENT
    bottom_size = 12 if not bottom.startswith("to ") else 11
    inner = (p(top, 12, 14, top_color, 700, extra="text-align:center;") +
             p(big, 22, 26, INK, 700, margin="1px 0 0 0", extra="text-align:center;") +
             p(bottom, bottom_size, 14, BODY, 700, extra="text-align:center;"))
    return shell_open.format(pad="7px 3px 7px 3px") + inner + shell_close


def item(title, lines, featured=False, label=None, first=True):
    """One list item: optional label, bold title, then plain lines (each already HTML)."""
    out = ""
    if label:
        out += p(label, 13, 18, ACCENT, 700, margin=("0 0 4px 0" if first else "14px 0 4px 0"))
        tmargin = "0"
    else:
        tmargin = "0" if first else "14px 0 0 0"
    tsize, tlh = (18, 25) if featured else (16, 23)
    out += p(title, tsize, tlh, INK, 700, margin=tmargin)
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



def story_img(src, width, alt, radius=12, link=None, extra_style=""):
    """Full-width section image; optional wrap link (featured CTAs)."""
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


# ---------------------------------------------------------------- content

def sensory(text, link_html):
    return f'{b("Sensory:")} {text} &nbsp;{link_html}'


EVENTS = [
    dict(chip=chip("Sat", "3", "Oct"),
         title="Game Day &middot; Autism Tennessee",
         meta="12:00&ndash;3:00 PM &middot; Nashville, address sent when you register &middot; Free, food provided &middot; About 45 min",
         sensory="indoor, small-group games for autistic kids, teens, and adults; families welcome.",
         link=("https://autismtn.org/events/EventDetails.aspx?id=2003814", "Register")),
    dict(chip=chip("Sat", "10", "Oct"),
         title="Village Hall: the IEP process, with Mercedes Lawson of A.C.C.E.S.S.",
         meta="9:30&ndash;11:00 AM Central &middot; Online &middot; Pay what you can, including nothing &middot; No drive",
         sensory="join from home and bring a question or simply listen; the lesson is recorded, the Q&amp;A is not.",
         link=(f"{SITE}/village-hall", "Register for Village Hall")),
    dict(chip=chip("Sun", "11", "Oct"),
         title="Sensory Sunday Hour &middot; Frist Art Museum",
         meta="12:00&ndash;1:00 PM &middot; Frist Art Museum, Nashville &middot; Free for members and ages 18 and under; other adults pay admission &middot; About 45 min",
         sensory="gallery sound lowered for the hour, multisensory carts with volunteers, Family Sunday activities afterward.",
         link=("https://fristartmuseum.org/event/sensory-sunday-hour-5/", "Details")),
    dict(chip=chip("Thu", "15", "Oct"), featured=True, label="Featured",
         title="All Access Night: Monsters in the Museum &middot; Discovery Center",
         meta="6:00&ndash;8:00 PM &middot; Discovery Center at Murfree Spring, Murfreesboro &middot; Free, registration required &middot; In Murfreesboro",
         sensory="after-hours museum with smaller crowds and reduced stimulation, at your own pace. A free night, close to home, built for exactly this.",
         link=("https://www.explorethedc.org/event/monsters-in-the-museum/", "Reserve your spot")),
    dict(chip=chip("Oct", "16", "to Nov 1"),
         title="Boo at the Zoo &middot; Nashville Zoo",
         meta="Nightly Oct 16 to Nov 1, 5:00&ndash;9:00 PM &middot; Nashville Zoo &middot; $19 Mon&ndash;Thu, $23 Fri&ndash;Sun (ages 2+), parking $10, advance tickets &middot; About 35 min",
         sensory="free Zooper Packs (fidgets, earplugs) at the ticket booth, a social story in English and Spanish, Mon&ndash;Wed quietest; some scenes are dark after sunset.",
         link=("https://www.nashvillezoo.org/boo", "Tickets and social story")),
    dict(chip=chip("Sat", "17", "Oct"),
         title="Super Sports Saturday &middot; ABLE Youth",
         meta="9:00 AM&ndash;12:00 PM &middot; Williamson County Rec Center, Franklin &middot; RSVP to info@ableyouth.org &middot; About 50 min",
         sensory="indoor rec-center gym with adaptive sports and games for kids of all ages.",
         link=("https://www.ableyouth.org/event/super-sports-saturday-34/", "Event page")),
    dict(chip=chip("Sat", "24", "Oct"),
         title="The EXTRA Mile &middot; Down Syndrome Association of Middle Tennessee",
         meta="Gates 9:00 AM, celebration 10:00 AM &middot; Ward Ag Center, Lebanon &middot; Rain or shine &middot; About 40 min",
         sensory="outdoors and lively; bounce houses open at 9:00 and live music starts at 10:00, so the first hour is the calmer one. No pets or balloons.",
         link=("https://somethingextra.org/ways-to-help/the-extra-mile/", "Details")),
    dict(chip=chip("Sun", "25", "Oct"),
         title="Sensory Spooktacular &middot; We Rock the Spectrum Murfreesboro",
         meta="820 N Thompson Ln, Murfreesboro &middot; Time and cost not posted yet &middot; In Murfreesboro",
         sensory=f"Halloween inside the sensory gym; watch their page or call {tel('(615) 962-8627', '+16159628627')} for details closer to the date.",
         link=("https://werockthespectrummurfreesboro.com/", "We Rock the Spectrum")),
    dict(chip=chip("Sat", "31", "Oct"),
         title="Evergreen Trunk or Treat &middot; Evergreen Life Services",
         meta="1:00&ndash;3:00 PM &middot; Evergreen Life Services, Antioch &middot; Free &middot; About 30 min",
         sensory="outdoors; decorated trunks, games, and booths built for people with intellectual and developmental disabilities and their families.",
         link=("https://evergreenls.org/trunkortreat/", "Details")),
]

# Deadline watch. Dated first, in date order; one chip per start date; undated last.
FALL_BREAK = item(
    "Fall break, Oct 5 to 9: Rutherford County and Murfreesboro City Schools",
    ["Both districts are closed all week. RCS report cards Fri Oct 16, conferences Tue Oct 20; MCS conferences Tue Nov 3 "
     "(no school). Conference day is a good time to ask for IEP progress data. &nbsp;"
     + a("https://www.rcschools.net/o/rcs/page/rcs-academic-calendars", "RCS calendar") + " &nbsp;&middot;&nbsp; "
     + a("https://www.cityschools.net/calendar", "MCS calendar")], featured=True)
VOTER = item(
    "Voter registration deadline for the Nov 3 election",
    ["Register or update your address at GoVoteTN.gov. Early voting Oct 14 to 29; Election Day Nov 3. Voters with a "
     "disability (or age 60+) can vote by mail if the county receives the request by Sat Oct 24. &nbsp;"
     + a("https://govotetn.gov/", "GoVoteTN")], featured=True, first=False)
COLA = item(
    "2027 Social Security and SSI raise (COLA) announced",
    ["Expected the morning the September inflation report comes out. New amounts start with January payments. &nbsp;"
     + a("https://www.ssa.gov/cola/", "SSA cost-of-living page")])
MEDICARE = item(
    "Medicare open enrollment, Oct 15 to Dec 7",
    ["For adult family members on Medicare: the one window to compare or switch drug and Advantage plans for 2027. "
     f"Free help from TN SHIP, {tel('1-877-801-0044', '+18778010044')}. &nbsp;"
     + a("https://www.medicare.gov/health-drug-plans/open-enrollment", "Medicare.gov")])
CLOCKS = item(
    "Clocks fall back one hour",
    ["Daylight saving time ends at 2:00 AM. If sleep is fragile at your house, shift bedtime 10 to 15 minutes a night the week before. &nbsp;"
     + a("https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst", "How DST works")])
HEALTHCARE = item(
    "HealthCare.gov open enrollment for 2027 plans, Nov 1 to Jan 15",
    ["Enroll or change plans by Dec 15 for Jan 1 coverage. Children may qualify for TennCare or CoverKids any time of year. &nbsp;"
     + a("https://www.healthcare.gov/quick-guide/dates-and-deadlines/", "Dates and deadlines")], first=False)
KATIE = item(
    "Katie Beckett, TennCare for children with disabilities",
    ["Not based on parent income. Apply any time; Part B has a waiting list, so sooner is better. &nbsp;"
     + a(f"{SITE}/resources/katie-beckett", "Katie Beckett guide")])
ANGEL = item(
    "Salvation Army Angel Tree, Rutherford and Cannon counties",
    ["Family registration is full but spots may reopen as applications are reviewed. Angel adoptions open Nov 6 for families who want to give. &nbsp;"
     + a("https://www.salvationarmymurfreesboro.org/angeltree", "Angel Tree page")])

FAFSA = item(
    "FAFSA for 2027&ndash;28 opens",
    ["For seniors and college students, including those with IEPs or 504 plans. Free; Tennessee Promise students must file by April 1, 2027. &nbsp;"
     + a("https://studentaid.gov/h/apply-for-aid/fafsa", "StudentAid.gov")])
EFS = item(
    "Education Freedom Scholarship family office hours, 1 to 2 PM Central",
    ["The state answers questions about the 2027&ndash;28 scholarship. Application dates are not posted yet; last year&rsquo;s window ran Dec 9 to Feb 6. &nbsp;"
     + a("https://www.tn.gov/education/efs.html", "EFS page")], first=False)
PROMISE = item(
    "Tennessee Promise application deadline, class of 2027",
    ["Tuition-free community college or TCAT for this year&rsquo;s seniors. School counselors and tnAchieves can help. &nbsp;"
     + a("https://www.collegefortn.org/tnpromise/", "Apply at CollegeforTN.org")])
ACT = item(
    "ACT: register and request accommodations for the Dec 12 test",
    ["Requests for extended time, breaks, or a separate room go through your school&rsquo;s testing coordinator by this date; late registration does not extend it. &nbsp;"
     + a("https://www.act.org/content/act/en/products-and-services/the-act/registration/accommodations.html", "ACT accommodations")])
IEA = item(
    "Individualized Education Account (IEA)",
    ["Projected to open Feb 16, 2027. It requires an active IEP and a full prior year in a Tennessee public school, so this fall counts. &nbsp;"
     + a("https://www.tn.gov/education/iea.html", "IEA page")])

EVERYONE_ROWS = [
    row(chip("Mon", "5", "Oct"), FALL_BREAK + VOTER, featured=True),
    row(chip("Wed", "14", "Oct"), COLA),
    row(chip("Oct", "15", "to Dec 7"), MEDICARE),
    row(chip("Sun", "1", "Nov"), CLOCKS + HEALTHCARE),
    row(chip("Any", None, "time"), KATIE),
    row(chip("No", None, "date"), ANGEL, last=True),
]
TEEN_ROWS = [
    row(chip("Thu", "1", "Oct"), FAFSA + EFS),
    row(chip("Mon", "2", "Nov"), PROMISE),
    row(chip("Fri", "6", "Nov"), ACT),
    row(chip("Feb", "16", "2027"), IEA, last=True),
]

NOTE_PARAS = [
    "Welcome to the Our Special Village family! I am a speech language pathologist running a private practice here in "
    "Murfreesboro. I&rsquo;m neurodivergent myself, married to my neurodivergent husband, and we have an AuDHD daughter together.",
    "I built this site because I saw one too many families feel lost, isolated, and confused by the system, and I noticed "
    "they were all asking the same questions.",
    "I hope this newsletter brings you information, but most of all a little slice of peace. October can be a busy month "
    "as we kick off the holiday season, so make sure you take care of yourself.",
]

ABOUT_PARAS = [
    "A village for families like ours. Free, parent-built guides, a local Resource Directory, sensory-friendly events, and a "
    "parent community for Murfreesboro and surrounding areas. Built around autism and open to every kind of difference and disability.",
    "Providers cannot pay for placement or recommendations. Sponsors and supporters never decide what gets listed or written.",
    "Owned and operated by Little Luminaries Therapy Services, PLLC.",
]

NUMBERS = [
    (b("988 Suicide and Crisis Lifeline.") + " Call or text " + tel("988", "988") + ", any hour."),
    (b("STEP TN,") + " free IEP and special education help for parents: " + tel("800-280-7837", "+18002807837")
     + " (Espa&ntilde;ol " + tel("800-975-2919", "+18009752919") + ")."),
    (b("Disability Rights Tennessee:") + " " + tel("800-342-1660", "+18003421660") + "."),
    (b("TN SHIP,") + " free Medicare counseling: " + tel("1-877-801-0044", "+18778010044") + "."),
]


# ---------------------------------------------------------------- page

def head():
    return f'''<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light only"><meta name="supported-color-schemes" content="light">
<title>{SUBJECT}</title>
<!-- MailerLite settings. Subject: "{SUBJECT}" ({len(SUBJECT)} chars). Preheader: "{PREHEADER}" Merge tags used in this file: {{$url}} (view in browser, the hosted archive copy) and {{$unsubscribe}} (one-click unsubscribe); they resolve only inside MailerLite and are dead on the GitHub Pages preview by design. Send with the plain-text alternative newsletter-october-2026.txt. -->
<!-- Built by tools/build-october-2026.py. Edit that file, not this one. -->
<!-- Note from Taylor: the first line ("Welcome to the Our Special Village family!") is written to a new subscriber. Once returning readers outnumber new ones, swap that first line and keep the rest. -->
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;700&amp;display=swap" rel="stylesheet">
<style type="text/css">
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;700&display=swap');
:root{{color-scheme:light only;supported-color-schemes:light;}}
a[x-apple-data-detectors]{{color:inherit !important;text-decoration:none !important;}}
u + #os-body a{{color:{ACCENT};text-decoration:underline;}}
@media only screen and (max-width:620px){{
  html,body{{width:100% !important;max-width:100% !important;overflow-x:hidden !important;-webkit-text-size-adjust:100% !important;}}
  .os-wrap,.os-wrap table{{width:100% !important;max-width:100% !important;}}
  table[width="600"]{{width:100% !important;max-width:100% !important;}}
  .os-pad{{padding-left:20px !important;padding-right:20px !important;}}
  .os-cardpad{{padding-left:16px !important;padding-right:16px !important;}}
  .os-h1{{font-size:27px !important;line-height:33px !important;}}
  .os-h2{{font-size:20px !important;line-height:26px !important;}}
  .os-col{{display:block !important;width:100% !important;max-width:100% !important;}}
  .os-col-photo{{padding:0 0 16px 0 !important;}}
  .os-col-photo td{{padding:0 0 16px 0 !important;}}
  .os-photo{{width:100% !important;max-width:100% !important;height:auto !important;}}
  .os-photocell,.os-photocell table{{width:100% !important;max-width:100% !important;height:auto !important;}}
  table[width="220"],table[width="256"]{{width:100% !important;max-width:100% !important;}}
  .os-col td{{padding-left:0 !important;}}
  body,table,td,p,a,span{{overflow-wrap:anywhere !important;word-break:break-word !important;}}
  img{{max-width:100% !important;height:auto !important;}}
  table[width="62"],td[width="62"]{{width:62px !important;max-width:62px !important;}}
  table[width="26"],td[width="30"]{{width:26px !important;max-width:30px !important;}}
  table[width="40"]{{width:40px !important;max-width:40px !important;}}
}}
/* Outlook.com and Windows Mail dark mode: hold the light palette. */
[data-ogsb] .os-bg{{background-color:{CREAM} !important;}} [data-ogsb] .os-card{{background-color:{WHITE} !important;}} [data-ogsb] .os-chip{{background-color:{BLUSH} !important;}} [data-ogsb] .os-navy{{background-color:{INK} !important;}} [data-ogsb] .os-btn-navy{{background-color:{INK} !important;}} [data-ogsb] .os-btn-gold{{background-color:{GOLD} !important;}} [data-ogsb] .os-stepbg{{background-color:{INK} !important;}} [data-ogsb] .os-rulebar{{background-color:{ACCENT} !important;}} [data-ogsb] .os-photocell{{background-color:{BLUSH} !important;}}
[data-ogsc] .os-ink{{color:{INK} !important;}} [data-ogsc] .os-body{{color:{BODY} !important;}} [data-ogsc] .os-muted{{color:{MUTED} !important;}} [data-ogsc] .os-accent,[data-ogsc] .os-link{{color:{ACCENT} !important;}} [data-ogsc] .os-gold{{color:{GOLD} !important;}} [data-ogsc] .os-sand{{color:{SAND} !important;}} [data-ogsc] .os-cream{{color:{CREAM} !important;}} [data-ogsc] .os-white,[data-ogsc] .os-step{{color:{WHITE} !important;}}
/* Apple Mail / iOS: force the light palette so cream and navy do not invert to navy-on-near-black. */
@media (prefers-color-scheme: dark){{
  .os-bg{{background-color:{CREAM} !important;}} .os-card{{background-color:{WHITE} !important;}} .os-chip{{background-color:{BLUSH} !important;}} .os-navy{{background-color:{INK} !important;}} .os-btn-navy{{background-color:{INK} !important;}} .os-btn-gold{{background-color:{GOLD} !important;}} .os-stepbg{{background-color:{INK} !important;}} .os-rulebar{{background-color:{ACCENT} !important;}} .os-photocell{{background-color:{BLUSH} !important;}}
  .os-ink{{color:{INK} !important;}} .os-body{{color:{BODY} !important;}} .os-muted{{color:{MUTED} !important;}} .os-accent,.os-link{{color:{ACCENT} !important;}} .os-gold{{color:{GOLD} !important;}} .os-sand{{color:{SAND} !important;}} .os-cream{{color:{CREAM} !important;}} .os-white,.os-step{{color:{WHITE} !important;}}
}}
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

    # View in browser (MailerLite archive merge tag)
    vib = ('<a class="os-muted" href="{$url}" style="color:' + MUTED + ';text-decoration:underline;">View in browser</a>')
    o.append(padrow(p(vib, 12, 17, MUTED, 400, extra="text-align:center;"), pad="0 34px 12px 34px"))

    # Masthead: the one place letter-spaced uppercase is used
    o.append(padrow(
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;"><tr>'
        f'<td align="left" style="vertical-align:middle;">{p("Our Special Village", 12, 16, ACCENT, 700, extra="letter-spacing:1.6px;text-transform:uppercase;")}</td>'
        f'<td align="right" style="vertical-align:middle;">{p("October 2026", 13, 16, MUTED, 700, extra="text-align:right;")}</td>'
        '</tr></table>', pad="0 34px 14px 34px"))

    # Hero illustration (the one illustration kept)
    o.append('<tr><td align="left" style="padding:0;">'
             f'<img src="{art("newsletter-fall.jpg")}" width="600" alt="Illustration of the village in autumn: homes, a gazebo, shops, and neighbors walking the path." '
             'style="display:block;width:100%;max-width:600px;height:auto;border:0;outline:none;text-decoration:none;border-radius:16px;"></td></tr>')
    o.append(sp(22))
    o.append(padrow(
        (f'<h1 class="os-h1 os-ink" style="margin:0 0 10px 0;font-family:{FONT};font-size:30px;line-height:36px;'
         f'mso-line-height-rule:exactly;color:{INK};font-weight:700;letter-spacing:-0.3px;">October in the Village</h1>') +
        p("The deadlines that actually matter, fall outings picked for sensory-sensitive kids, two new guides, and one hard school question answered plainly.", 17, 26, BODY, 400)))
    o.append(sp(14))
    toc = " &nbsp;&middot;&nbsp; ".join(a(f"#{i}", t, nowrap=False) for i, t in [
        ("deadlines", "Deadline watch"), ("events", "The month ahead"), ("library", "New in the library"),
        ("hope", "Wall of Hope"), ("question", "One question, answered"), ("village-hall", "Village Hall")])
    o.append(padrow(p(f'{b("In this issue:")} {toc}', 14, 24, BODY, 400)))

    # 1. Note from Taylor: plain, no card, no border, no icon
    o.append(sp(40))
    note = "".join(p(t, 16, 25, BODY, 400, margin=("0" if i == 0 else "12px 0 0 0")) for i, t in enumerate(NOTE_PARAS))
    note += p("With love,", 16, 25, BODY, 400, margin="16px 0 6px 0")
    note += (f'<img src="{art("signature-taylor.png")}" width="140" height="55" alt="Taylor" '
             f'style="display:block;width:140px;height:auto;border:0;outline:none;text-decoration:none;font-family:{FONT};font-size:18px;color:{ACCENT};">')
    o.append(padrow(note))

    # 2/5/6/7/8. Deadline watch first, dated rows with chips, teen/college under its own subhead
    o.append(sp(48))
    o.append(section_head("deadlines", "Deadline watch",
                          "Two land on Monday, October 5. Dated items first, then the ones that only matter if you have a high schooler."))
    o.append(sp(20))
    o.append(padrow(card(subhead("For every family") + rows_table(EVERYONE_ROWS))))
    o.append(sp(24))
    o.append(padrow(card(subhead("Teens and college") +
                         p("Five items for families with a high schooler or college student. Skip this card if that is not you yet.", 15, 22, BODY, 400, margin="0 0 4px 0") +
                         rows_table(TEEN_ROWS))))
    o.append(sp(14))
    o.append(padrow(p("Dates confirmed Sept 14. If something changed, reply and we will fix it.", 13, 20, MUTED, 400)))

    # Featured: All Access Night (Rem T323) — image linked to reserve URL, above event copy
    MONSTERS_URL = "https://www.explorethedc.org/event/monsters-in-the-museum/"
    o.append(sp(48))
    featured_art = story_img(
        art("featured-monsters-museum.jpg"), 560,
        "Family exploring a friendly museum dinosaur exhibit at a calm after-hours sensory night; one child wears headphones",
        radius=12, link=MONSTERS_URL)
    featured_copy = (p("Featured", 13, 18, ACCENT, 700, margin="14px 0 4px 0")
                     + p("All Access Night: Monsters in the Museum &middot; Discovery Center", 18, 25, INK, 700)
                     + p("6:00&ndash;8:00 PM &middot; Discovery Center at Murfree Spring, Murfreesboro &middot; Free, registration required &middot; In Murfreesboro", 16, 24, BODY, 400, margin="4px 0 0 0")
                     + p(sensory("after-hours museum with smaller crowds and reduced stimulation, at your own pace. A free night, close to home, built for exactly this.", a(MONSTERS_URL, "Reserve your spot")), 16, 24, BODY, 400, margin="4px 0 0 0"))
    o.append(padrow(card(featured_art + featured_copy, pad="12px 20px 18px 20px")))

    # The month ahead — autumn collage once above the event list (not per-event thumbs)
    o.append(sp(48))
    o.append(section_head("events", "The month ahead", "Picked for sensory-sensitive kids and their families. Drive times are from Murfreesboro."))
    o.append(sp(20))
    collage = story_img(
        art("autumn-events-collage.jpg"), 600,
        "Coordinated autumn sensory-friendly outings: museum, gazebo walk, lantern zoo night, indoor play, trunk-or-treat",
        radius=12)
    o.append(padrow(collage, pad="0 0 0 0"))
    o.append(sp(16))
    ev_rows = []
    for i, e in enumerate(EVENTS):
        feat = e.get("featured", False)
        content = item(e["title"], [e["meta"], sensory(e["sensory"], a(*e["link"]))], featured=feat, label=e.get("label"))
        ev_rows.append(row(e["chip"], content, last=(i == len(EVENTS) - 1), featured=feat))
    o.append(padrow(card(rows_table(ev_rows))))
    o.append(sp(24))
    weekly = subhead("Every week") + rows_table([
        f'<tr><td class="os-rule" style="padding:10px 0 16px 0;border-bottom:1px solid {RULE};">'
        + p("Thursdays &middot; 7:00&ndash;8:00 PM Central", 16, 23, INK, 700)
        + p("Our Special Village online parent group &middot; Free &middot; Online", 15, 22, BODY, 400, margin="4px 0 0 0")
        + p("Meeting weekly since September, so join any Thursday. Any diagnosis or none yet; cameras optional; not recorded.", 15, 22, BODY, 400, margin="4px 0 14px 0")
        + button(f"{SITE}/group", "Save my seat", INK, CREAM).replace('class="os-btn"', 'class="os-btn os-btn-navy"')
        + '</td></tr>',
        '<tr><td class="os-rule" style="padding:12px 0 10px 0;">'
        + p("Wednesdays &middot; 5:00 PM", 16, 23, INK, 700)
        + p("We Rock the Spectrum Murfreesboro group, led by Cari Parr &middot; 820 N Thompson Ln, Murfreesboro", 15, 22, BODY, 400, margin="4px 0 0 0")
        + p(f"Call {tel('(615) 962-8627', '+16159628627')} for current details.", 15, 22, BODY, 400, margin="4px 0 0 0")
        + '</td></tr>'])
    o.append(padrow(card(weekly)))

    # New in the library — matching Rem/Vincent card images (560; -280 optional srcset)
    o.append(sp(48))
    o.append(section_head("library", "New in the library"))
    o.append(sp(20))
    therapy_img = (
        f'<img src="{art("guide-therapy-styles.jpg")}" srcset="{art("guide-therapy-styles-280.jpg")} 280w, {art("guide-therapy-styles.jpg")} 560w" '
        f'sizes="(max-width:620px) 280px, 560px" width="560" '
        f'alt="Adult and child sharing a calm sensory play tray in a warm playroom" '
        f'style="display:block;width:100%;max-width:560px;height:auto;border:0;outline:none;text-decoration:none;border-radius:12px;margin:0 0 14px 0;">'
    )
    therapy = (therapy_img
               + p("New guide, reviewed Sept 2026", 13, 18, ACCENT, 700, margin="0 0 6px 0")
               + p("Therapy styles: play, structure, and compliance", 18, 25, INK, 700)
               + p("Two therapists can have the same license and run completely different rooms. Learn what the common labels actually look like.", 16, 24, BODY, 400, margin="8px 0 0 0")
               + p(a(f"{SITE}/resources/therapy-styles", "Read the guide"), 16, 24, BODY, 400, margin="12px 0 0 0"))
    o.append(padrow(card(therapy, pad="12px 20px 20px 20px")))
    o.append(sp(24))
    grief_img = (
        f'<img src="{art("guide-grief.jpg")}" srcset="{art("guide-grief-280.jpg")} 280w, {art("guide-grief.jpg")} 560w" '
        f'sizes="(max-width:620px) 280px, 560px" width="560" '
        f'alt="Parent on a porch in autumn while a child plays nearby in leaves - quiet and hopeful" '
        f'style="display:block;width:100%;max-width:560px;height:auto;border:0;outline:none;text-decoration:none;border-radius:12px;margin:0 0 14px 0;">'
    )
    grief = (grief_img
             + p("New guide, reviewed Sept 2026", 13, 18, ACCENT, 700, margin="0 0 6px 0")
             + p("Grief and disability: the loss nobody sends a card for", 22, 29, INK, 700)
             + p("This kind of grief rarely has an occasion attached to it. It shows up at a birthday party, at a milestone that did not arrive, in the parking lot after an evaluation. The guide covers what it actually looks like, why it circles back instead of ending, how it can land differently on each parent in the same house, what siblings end up carrying, and when it has turned into something worth taking to a counselor.", 16, 25, BODY, 400, margin="10px 0 0 0")
             + p(a(f"{SITE}/resources/grieving-the-life-you-imagined", "Read the grief guide"), 16, 24, BODY, 400, margin="14px 0 0 0"))
    o.append(padrow(card(grief, pad="12px 20px 22px 20px")))

    # Wall of Hope
    o.append(sp(48))
    o.append(section_head("hope", "Wall of Hope"))
    o.append(sp(20))
    hope = (p("An invitation", 13, 18, ACCENT, 700, margin="0 0 6px 0")
            + p("Borrow a little hope, or lend some", 20, 27, INK, 700)
            + p("Each month this space holds one real win from a family in Murfreesboro or the surrounding areas, shared with permission and the name you choose. The first stories are on their way. Have one? Something that got easier, a skill or friendship worth celebrating, or a wonderfully ordinary week. Tell it like you would tell another parent.", 16, 24, BODY, 400, margin="8px 0 0 0")
            + p(a(f"{SITE}/hope", "Share your win"), 16, 24, BODY, 400, margin="12px 0 0 0"))
    o.append(padrow(card(hope, pad="18px 20px 20px 20px")))

    # One question, answered
    o.append(sp(48))
    o.append(section_head("question", "One question, answered",
                          "Our recurring column: one real question from a local parent, answered plainly, every issue. " + a(f"{SITE}/contact", "Send us your question")))
    o.append(sp(20))
    steps = rows_table([
        step(1, f'{b("Put it in writing.")} Email the case manager and copy the principal: name the service or accommodation, quote what the IEP says, describe what is actually happening, and ask for a fix by a specific date. Ask for service logs and progress data too; you are entitled to them. Keep the sent copy.'),
        step(2, f'{b("Ask for an IEP team meeting.")} You can request one in writing at any time, not just at the annual review, and the school has to respond. If things stall, copy the district&rsquo;s special education director. Bring your notes and a friend to take notes for you.'),
        step(3, f'{b("Use the state&rsquo;s free complaint process.")} If it still is not fixed, file an administrative complaint with the Tennessee Department of Education. No lawyer, no cost. &ldquo;Failing to implement IEP accommodations or services&rdquo; is one of the state&rsquo;s own listed examples. TDOE must issue a written decision within 60 calendar days, and you have one year from the problem to file. Mediation is also available.'),
        step(4, f'{b("Get free backup.")} STEP TN, Tennessee&rsquo;s parent training center, will review the IEP with you and help you prepare: {tel("800-280-7837", "+18002807837")} (Espa&ntilde;ol {tel("800-975-2919", "+18009752919")}). For a district that will not follow its own plan, Disability Rights Tennessee: {tel("800-342-1660", "+18003421660")}.'),
    ])
    qa = (p("October&rsquo;s question", 13, 18, ACCENT, 700, margin="0 0 6px 0")
          + p("&ldquo;What do I do if my child&rsquo;s IEP isn&rsquo;t being followed?&rdquo;", 20, 27, INK, 700)
          + p("Answer", 13, 18, ACCENT, 700, margin="16px 0 6px 0")
          + p("An IEP is a legally binding plan: the school has to deliver every service and accommodation written in it, not just the convenient ones. When that is not happening, you have more options than most parents are told.", 16, 24, BODY, 400, margin="0 0 14px 0")
          + steps
          + p("Bring your own version of this question to Village Hall on Sat Oct 10. Mercedes Lawson of A.C.C.E.S.S. is covering the IEP process and taking parent questions live; pay what you can, including nothing. &nbsp;" + a(f"{SITE}/village-hall", "Register for Village Hall"), 15, 23, BODY, 400, margin="2px 0 0 0")
          + p(a(f"{SITE}/resources/iep-504", "Read the IEP &amp; 504 guide") + " &nbsp;&middot;&nbsp; " + a("https://www.tn.gov/education/legal-services/special-education-legal-services/legal-dispute-resolution-processes.html", "TDOE dispute options"), 16, 24, BODY, 400, margin="14px 0 0 0")
          + p("Parent-to-parent guidance, not legal advice.", 13, 20, MUTED, 400, margin="12px 0 0 0"))
    o.append(padrow(card(qa, pad="18px 20px 20px 20px")))

    # Village Hall — Rem/Vincent IEP workshop art above Oct 10 block
    o.append(sp(48))
    o.append(section_head("village-hall", "Village Hall", "One topic, one guest expert, your questions. Second Saturday of every month, online. Pay what you can, including nothing."))
    o.append(sp(20))
    vh_art = story_img(
        art("village-hall-iep.jpg"), 600,
        "Parents gathered around a table with a laptop for an online IEP workshop - autumn village setting",
        radius=12)
    o.append(padrow(vh_art, pad="0 0 0 0"))
    o.append(sp(16))
    vh = (f'<table role="presentation" class="os-navy" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="{INK}" style="width:100%;border-collapse:separate;background-color:{INK};border-radius:16px;">'
          '<tr><td align="left" style="padding:26px 26px 26px 26px;">'
          + p("Saturday, October 10, 2026", 13, 18, GOLD, 700, margin="0 0 6px 0")
          + p("9:30 to 11:00 AM Central &middot; Online &middot; Pay what you can, including nothing", 16, 24, SAND, 400, margin="0 0 18px 0")
          + p("Topic and guest", 13, 18, GOLD, 700, margin="0 0 6px 0")
          + p("The IEP process and navigating the school system, with Mercedes Lawson of A.C.C.E.S.S.", 20, 27, CREAM, 700, margin="0 0 12px 0")
          + p("A 40-minute lesson on how the IEP process works and how to navigate the school system, then live parent questions. The lesson is recorded and sent to registrants; the Q&amp;A is not.", 16, 24, SAND, 400, margin="0 0 20px 0")
          + button(f"{SITE}/village-hall", "Register for Village Hall", GOLD, INK).replace('class="os-btn"', 'class="os-btn os-btn-gold"')
          + p("$0 always welcome &middot; $10 helps &middot; $20 suggested &middot; $35 sponsors another seat. The meeting link is emailed to registrants.", 14, 22, SAND, 400, margin="16px 0 0 0")
          + '</td></tr></table>')
    o.append(padrow(vh))

    # 3. About Our Special Village: fixed block, photo left, copy right, stacks photo-on-top on mobile
    o.append(sp(48))
    about_copy = ((f'<h2 class="os-ink" style="margin:0;font-family:{FONT};font-size:18px;line-height:25px;'
                   f'mso-line-height-rule:exactly;color:{INK};font-weight:700;">About Our Special Village</h2>')
                  + "".join(p(t, 15, 22, BODY, 400, margin="8px 0 0 0") for t in ABOUT_PARAS)
                  + p(a(f"{SITE}/about", "About the Village &rarr;") + " &nbsp;&middot;&nbsp; " + a(f"{SITE}/editorial-policy", "How we check information &rarr;"), 15, 22, BODY, 400, margin="12px 0 0 0"))
    # About photo ~280–320 wide (T323 shrink/resize from full bleed)
    photo = (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="280" class="os-photocell" bgcolor="{BLUSH}" '
             f'style="width:280px;border-collapse:separate;background-color:{BLUSH};border-radius:14px;">'
             f'<tr><td class="os-photocell" align="center" style="width:280px;vertical-align:middle;border-radius:14px;">'
             f'<img class="os-photo" src="{art("about-family-bowling.jpg")}" width="280" height="280" alt="Taylor, her husband, and their daughter at a bowling alley." '
             f'style="display:block;width:280px;max-width:100%;height:auto;border:0;outline:none;text-decoration:none;border-radius:14px;font-family:{FONT};font-size:13px;line-height:18px;color:{BODY};"></td></tr></table>')
    # Hybrid columns: side-by-side on desktop (align=left tables), photo-on-top on mobile.
    about = (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;"><tr><td align="left" style="padding:0;">'
        '<!--[if mso]><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="560"><tr><td width="280" valign="top"><![endif]-->'
        f'<table role="presentation" class="os-col os-col-photo" align="left" cellpadding="0" cellspacing="0" border="0" width="280" style="width:280px;max-width:280px;border-collapse:collapse;">'
        f'<tr><td style="padding:0;">{photo}</td></tr></table>'
        '<!--[if mso]></td><td width="16"></td><td width="264" valign="top"><![endif]-->'
        f'<table role="presentation" class="os-col" align="left" cellpadding="0" cellspacing="0" border="0" width="264" style="width:264px;max-width:264px;border-collapse:collapse;">'
        f'<tr><td style="padding:0 0 0 16px;">{about_copy}</td></tr></table>'
        '<!--[if mso]></td></tr></table><![endif]-->'
        '</td></tr></table>'
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;clear:both;"><tr><td style="font-size:0;line-height:0;height:0;">&nbsp;</td></tr></table>'
    )
    o.append(padrow(card(about, pad="20px 20px 20px 20px")))

    # 12. Numbers worth keeping
    o.append(sp(24))
    nums = subhead("Numbers worth keeping", first=False) + "".join(p(t, 15, 22, BODY, 400, margin=("6px 0 0 0" if i == 0 else "6px 0 0 0")) for i, t in enumerate(NUMBERS))
    o.append(padrow(card(nums, pad="16px 20px 18px 20px")))

    # 9. Forward it, subscribe link
    o.append(sp(28))
    o.append(padrow(p("Know a family who could use this? Forward it along. Anyone can join the list at "
                      + a(f"{SITE}/newsletter", "ourspecialvillagetn.com/newsletter", nowrap=False) + ".", 15, 23, BODY, 400, extra="text-align:center;")))

    # Footer (13. sponsors reduced to one line)
    o.append(sp(36))
    o.append(f'<tr><td class="os-pad" style="padding:0 34px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;"><tr><td class="os-rule" style="border-top:1px solid {HAIR};font-size:0;line-height:0;height:1px;">&nbsp;</td></tr></table></td></tr>')
    o.append(sp(22))
    footer = (p("Our Special Village &middot; Murfreesboro and surrounding areas, Tennessee", 15, 23, INK, 700, margin="0 0 8px 0")
              + p("Local businesses and practices help keep the Village free and ad-free. " + a(f"{SITE}/sponsors", "Sponsorship options", nowrap=False) + ".", 14, 22, BODY, 400, margin="0 0 14px 0")
              + p("You are receiving this because you joined the newsletter list at ourspecialvillagetn.com.<br>"
                  + a("{$unsubscribe}", "Unsubscribe in one click", nowrap=False) + " &nbsp;&middot;&nbsp; " + a(f"{SITE}/privacy", "Privacy") + " &nbsp;&middot;&nbsp; " + a(f"{SITE}/contact", "Contact"), 13, 22, BODY, 400, margin="0 0 12px 0")
              + p("Our Special Village is owned and operated by Little Luminaries Therapy Services, PLLC<br>1810 Ward Dr, Suite 101, Murfreesboro, TN 37129", 12, 20, BODY, 400))
    o.append(padrow(footer))

    o.append('</table></td></tr></table></body></html>')
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------- plain text

def build_text():
    L = []
    w = L.append
    w("OUR SPECIAL VILLAGE · October 2026")
    w("View this email in your browser: {$url}")
    w("")
    w("OCTOBER IN THE VILLAGE")
    w("The deadlines that actually matter, fall outings picked for sensory-sensitive kids, two new guides, and one hard school question answered plainly.")
    w("")
    w("In this issue: Deadline watch · The month ahead · New in the library · Wall of Hope · One question, answered · Village Hall")
    w("")
    w("Welcome to the Our Special Village family! I am a speech language pathologist running a private practice here in Murfreesboro. I'm neurodivergent myself, married to my neurodivergent husband, and we have an AuDHD daughter together.")
    w("")
    w("I built this site because I saw one too many families feel lost, isolated, and confused by the system, and I noticed they were all asking the same questions.")
    w("")
    w("I hope this newsletter brings you information, but most of all a little slice of peace. October can be a busy month as we kick off the holiday season, so make sure you take care of yourself.")
    w("")
    w("With love,")
    w("Taylor")
    w("")
    w("----------------------------------------")
    w("DEADLINE WATCH")
    w("Two land on Monday, October 5. Dated items first, then the ones that only matter if you have a high schooler.")
    w("")
    w("For every family")
    w("")
    w("Mon Oct 5 · Fall break, Oct 5 to 9: Rutherford County and Murfreesboro City Schools")
    w("  Both districts are closed all week. RCS report cards Fri Oct 16, conferences Tue Oct 20; MCS conferences Tue Nov 3 (no school). Conference day is a good time to ask for IEP progress data.")
    w("  RCS calendar: https://www.rcschools.net/o/rcs/page/rcs-academic-calendars")
    w("  MCS calendar: https://www.cityschools.net/calendar")
    w("")
    w("Mon Oct 5 · Voter registration deadline for the Nov 3 election")
    w("  Register or update your address at GoVoteTN.gov. Early voting Oct 14 to 29; Election Day Nov 3. Voters with a disability (or age 60+) can vote by mail if the county receives the request by Sat Oct 24.")
    w("  https://govotetn.gov/")
    w("")
    w("Wed Oct 14 · 2027 Social Security and SSI raise (COLA) announced")
    w("  Expected the morning the September inflation report comes out. New amounts start with January payments.")
    w("  https://www.ssa.gov/cola/")
    w("")
    w("Oct 15 to Dec 7 · Medicare open enrollment")
    w("  For adult family members on Medicare: the one window to compare or switch drug and Advantage plans for 2027. Free help from TN SHIP, 1-877-801-0044.")
    w("  https://www.medicare.gov/health-drug-plans/open-enrollment")
    w("")
    w("Sun Nov 1 · Clocks fall back one hour")
    w("  Daylight saving time ends at 2:00 AM. If sleep is fragile at your house, shift bedtime 10 to 15 minutes a night the week before.")
    w("  https://www.nist.gov/pml/time-and-frequency-division/popular-links/daylight-saving-time-dst")
    w("")
    w("Nov 1 to Jan 15 · HealthCare.gov open enrollment for 2027 plans")
    w("  Enroll or change plans by Dec 15 for Jan 1 coverage. Children may qualify for TennCare or CoverKids any time of year.")
    w("  https://www.healthcare.gov/quick-guide/dates-and-deadlines/")
    w("")
    w("Any time · Katie Beckett, TennCare for children with disabilities")
    w("  Not based on parent income. Apply any time; Part B has a waiting list, so sooner is better.")
    w(f"  {SITE}/resources/katie-beckett")
    w("")
    w("No date · Salvation Army Angel Tree, Rutherford and Cannon counties")
    w("  Family registration is full but spots may reopen as applications are reviewed. Angel adoptions open Nov 6 for families who want to give.")
    w("  https://www.salvationarmymurfreesboro.org/angeltree")
    w("")
    w("Teens and college")
    w("Five items for families with a high schooler or college student. Skip this block if that is not you yet.")
    w("")
    w("Thu Oct 1 · FAFSA for 2027-28 opens")
    w("  For seniors and college students, including those with IEPs or 504 plans. Free; Tennessee Promise students must file by April 1, 2027.")
    w("  https://studentaid.gov/h/apply-for-aid/fafsa")
    w("")
    w("Thu Oct 1 · Education Freedom Scholarship family office hours, 1 to 2 PM Central")
    w("  The state answers questions about the 2027-28 scholarship. Application dates are not posted yet; last year's window ran Dec 9 to Feb 6.")
    w("  https://www.tn.gov/education/efs.html")
    w("")
    w("Mon Nov 2 · Tennessee Promise application deadline, class of 2027")
    w("  Tuition-free community college or TCAT for this year's seniors. School counselors and tnAchieves can help.")
    w("  https://www.collegefortn.org/tnpromise/")
    w("")
    w("Fri Nov 6 · ACT: register and request accommodations for the Dec 12 test")
    w("  Requests for extended time, breaks, or a separate room go through your school's testing coordinator by this date; late registration does not extend it.")
    w("  https://www.act.org/content/act/en/products-and-services/the-act/registration/accommodations.html")
    w("")
    w("Feb 16, 2027 · Individualized Education Account (IEA)")
    w("  Projected to open Feb 16, 2027. It requires an active IEP and a full prior year in a Tennessee public school, so this fall counts.")
    w("  https://www.tn.gov/education/iea.html")
    w("")
    w("Dates confirmed Sept 14. If something changed, reply and we will fix it.")
    w("")
    w("----------------------------------------")
    w("THE MONTH AHEAD")
    w("Picked for sensory-sensitive kids and their families. Drive times are from Murfreesboro.")
    w("")
    import html as _html
    import re as _re
    for e in EVENTS:
        strip = lambda s: _html.unescape(_re.sub(r"<[^>]+>", "", s))
        w(f"{strip(e['title'])}" + ("  [Featured]" if e.get("featured") else ""))
        w(f"  {strip(e['meta'])}")
        w(f"  Sensory: {strip(e['sensory'])}")
        w(f"  {e['link'][1]}: {e['link'][0]}")
        w("")
    w("Every week")
    w("")
    w("Thursdays · 7:00-8:00 PM Central · Our Special Village online parent group · Free · Online")
    w("  Meeting weekly since September, so join any Thursday. Any diagnosis or none yet; cameras optional; not recorded.")
    w(f"  Save my seat: {SITE}/group")
    w("")
    w("Wednesdays · 5:00 PM · We Rock the Spectrum Murfreesboro group, led by Cari Parr · 820 N Thompson Ln, Murfreesboro")
    w("  Call (615) 962-8627 for current details.")
    w("")
    w("----------------------------------------")
    w("NEW IN THE LIBRARY")
    w("")
    w("New guide, reviewed Sept 2026 · Therapy styles: play, structure, and compliance")
    w("  Two therapists can have the same license and run completely different rooms. Learn what the common labels actually look like.")
    w(f"  Read the guide: {SITE}/resources/therapy-styles")
    w("")
    w("New guide, reviewed Sept 2026 · Grief and disability: the loss nobody sends a card for")
    w("  This kind of grief rarely has an occasion attached to it. It shows up at a birthday party, at a milestone that did not arrive, in the parking lot after an evaluation. The guide covers what it actually looks like, why it circles back instead of ending, how it can land differently on each parent in the same house, what siblings end up carrying, and when it has turned into something worth taking to a counselor.")
    w(f"  Read the grief guide: {SITE}/resources/grieving-the-life-you-imagined")
    w("")
    w("----------------------------------------")
    w("WALL OF HOPE")
    w("")
    w("An invitation · Borrow a little hope, or lend some")
    w("  Each month this space holds one real win from a family in Murfreesboro or the surrounding areas, shared with permission and the name you choose. The first stories are on their way. Have one? Something that got easier, a skill or friendship worth celebrating, or a wonderfully ordinary week. Tell it like you would tell another parent.")
    w(f"  Share your win: {SITE}/hope")
    w("")
    w("----------------------------------------")
    w("ONE QUESTION, ANSWERED")
    w(f"Our recurring column: one real question from a local parent, answered plainly, every issue. Send us your question: {SITE}/contact")
    w("")
    w("October's question: \"What do I do if my child's IEP isn't being followed?\"")
    w("")
    w("Answer")
    w("An IEP is a legally binding plan: the school has to deliver every service and accommodation written in it, not just the convenient ones. When that is not happening, you have more options than most parents are told.")
    w("")
    w("1. Put it in writing. Email the case manager and copy the principal: name the service or accommodation, quote what the IEP says, describe what is actually happening, and ask for a fix by a specific date. Ask for service logs and progress data too; you are entitled to them. Keep the sent copy.")
    w("")
    w("2. Ask for an IEP team meeting. You can request one in writing at any time, not just at the annual review, and the school has to respond. If things stall, copy the district's special education director. Bring your notes and a friend to take notes for you.")
    w("")
    w("3. Use the state's free complaint process. If it still is not fixed, file an administrative complaint with the Tennessee Department of Education. No lawyer, no cost. \"Failing to implement IEP accommodations or services\" is one of the state's own listed examples. TDOE must issue a written decision within 60 calendar days, and you have one year from the problem to file. Mediation is also available.")
    w("")
    w("4. Get free backup. STEP TN, Tennessee's parent training center, will review the IEP with you and help you prepare: 800-280-7837 (Español 800-975-2919). For a district that will not follow its own plan, Disability Rights Tennessee: 800-342-1660.")
    w("")
    w(f"Bring your own version of this question to Village Hall on Sat Oct 10. Mercedes Lawson of A.C.C.E.S.S. is covering the IEP process and taking parent questions live; pay what you can, including nothing. Register for Village Hall: {SITE}/village-hall")
    w(f"Read the IEP & 504 guide: {SITE}/resources/iep-504")
    w("TDOE dispute options: https://www.tn.gov/education/legal-services/special-education-legal-services/legal-dispute-resolution-processes.html")
    w("Parent-to-parent guidance, not legal advice.")
    w("")
    w("----------------------------------------")
    w("VILLAGE HALL")
    w("One topic, one guest expert, your questions. Second Saturday of every month, online. Pay what you can, including nothing.")
    w("")
    w("Saturday, October 10, 2026 · 9:30 to 11:00 AM Central · Online · Pay what you can, including nothing")
    w("Topic and guest: The IEP process and navigating the school system, with Mercedes Lawson of A.C.C.E.S.S.")
    w("A 40-minute lesson on how the IEP process works and how to navigate the school system, then live parent questions. The lesson is recorded and sent to registrants; the Q&A is not.")
    w(f"Register for Village Hall: {SITE}/village-hall")
    w("$0 always welcome · $10 helps · $20 suggested · $35 sponsors another seat. The meeting link is emailed to registrants.")
    w("")
    w("----------------------------------------")
    w("ABOUT OUR SPECIAL VILLAGE")
    w("")
    for t in ABOUT_PARAS:
        w(_html.unescape(t))
        w("")
    w(f"About the Village: {SITE}/about")
    w(f"How we check information: {SITE}/editorial-policy")
    w("")
    w("NUMBERS WORTH KEEPING")
    w("988 Suicide and Crisis Lifeline. Call or text 988, any hour.")
    w("STEP TN, free IEP and special education help for parents: 800-280-7837 (Español 800-975-2919).")
    w("Disability Rights Tennessee: 800-342-1660.")
    w("TN SHIP, free Medicare counseling: 1-877-801-0044.")
    w("")
    w(f"Know a family who could use this? Forward it along. Anyone can join the list at {SITE}/newsletter")
    w("")
    w("----------------------------------------")
    w("Our Special Village · Murfreesboro and surrounding areas, Tennessee")
    w(f"Local businesses and practices help keep the Village free and ad-free. Sponsorship options: {SITE}/sponsors")
    w("")
    w("You are receiving this because you joined the newsletter list at ourspecialvillagetn.com.")
    w("Unsubscribe in one click: {$unsubscribe}")
    w(f"Privacy: {SITE}/privacy · Contact: {SITE}/contact")
    w("")
    w("Our Special Village is owned and operated by Little Luminaries Therapy Services, PLLC")
    w("1810 Ward Dr, Suite 101, Murfreesboro, TN 37129")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=PAGES, help="URL prefix for art/ (default: GitHub Pages)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    args = ap.parse_args()
    html = build_html(args.base)
    txt = build_text()
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    for name in ("newsletter-october-subscriber-preview.html", "index.html"):
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(html)
    with open(os.path.join(out, "newsletter-october-2026.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    for s in (html, txt):
        assert "—" not in s and "&mdash;" not in s, "em dash found"
        assert "{$url}" in s and "{$unsubscribe}" in s
        assert "Village Picks" not in s
        assert "Microsoft Teams" not in s
        assert "art/icons/" not in s
    assert 'alt="Taylor"' in html
    assert 'alt="Taylor, her husband, and their daughter at a bowling alley."' in html
    assert "featured-monsters-museum.jpg" in html
    assert "autumn-events-collage.jpg" in html
    assert "guide-therapy-styles.jpg" in html
    assert "guide-grief.jpg" in html
    assert "village-hall-iep.jpg" in html
    assert "explorethedc.org/event/monsters-in-the-museum/" in html
    assert "Register for Village Hall" in html
    assert "Save my seat" in html
    assert "Numbers worth keeping" in html
    assert "ourspecialvillagetn.com/newsletter" in html
    assert html.count("&rarr;") == 2, html.count("&rarr;")
    print(f"wrote {out}: html {len(html.encode('utf-8'))} bytes, txt {len(txt.encode('utf-8'))} bytes")


if __name__ == "__main__":
    main()
