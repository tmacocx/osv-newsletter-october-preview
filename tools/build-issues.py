#!/usr/bin/env python3
"""Build the Nov 2026 - Feb 2027 Our Special Village newsletters from the October template.

Every block, size, color and spacing comes from tools/build-october-2026.py
(imported as O below), so the four new issues stay the exact same template.
Only the words, dates and pictures change; those live in tools/issue_data.py.

Writes, for each issue in issues/<id>/:
  index.html     browser preview (wide layout, real view/unsubscribe links)
  email.html     email HTML ({$url} / {$unsubscribe} merge tags)
  email.txt      plain-text alternative
  deadlines.html the "See all deadlines" companion page
and issues/index.html, a month picker for the preview.

Text inside ph(...) is a placeholder Taylor still has to fill in (Wall of Hope
stories, Village Hall guests not booked yet). It renders as a dashed yellow
box so it cannot go out by accident: --strict fails while any remain.

    python3 tools/build-issues.py
    python3 tools/build-issues.py --site-export ../OurSpecialVillage   # newsletters/<id>/ + assets
"""
import argparse
import html as _html
import importlib.util
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

_spec = importlib.util.spec_from_file_location("october", os.path.join(HERE, "build-october-2026.py"))
O = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(O)

import issue_data as D  # noqa: E402  (tools/ is on sys.path when run as a script)

p, b, a, navy_a, tel = O.p, O.b, O.a, O.navy_a, O.tel
sp, major_sp, padrow, anchor, rule = O.sp, O.major_sp, O.padrow, O.anchor, O.rule
section_head, card, rows_table, row, chip, item = (O.section_head, O.card, O.rows_table,
                                                    O.row, O.chip, O.item)
button, group_card, step, vh_meta_icon, price_boxes, disclose = (
    O.button, O.group_card, O.step, O.vh_meta_icon, O.price_boxes, O.disclose)
CREAM, WHITE, BLUSH, INK, BODY, MUTED, ACCENT, HAIR, RULE, GOLD, SAND, FONT = (
    O.CREAM, O.WHITE, O.BLUSH, O.INK, O.BODY, O.MUTED, O.ACCENT, O.HAIR, O.RULE, O.GOLD,
    O.SAND, O.FONT)
SITE = O.SITE
PAGES = "https://tmacocx.github.io/osv-newsletter-october-preview/"

PH_OPEN = "⟦"   # markers survive entity handling; replaced at render time
PH_CLOSE = "⟧"


def ph(text):
    """Placeholder Taylor must replace before the issue sends."""
    return f"{PH_OPEN}{text}{PH_CLOSE}"


def render_ph(s, dark=False):
    color = INK
    style = ("background-color:#fff1b8;border:1px dashed #b8912f;border-radius:4px;"
             f"padding:1px 5px;color:{color};font-weight:700;")
    return re.sub(f"{PH_OPEN}(.*?){PH_CLOSE}",
                  lambda m: f'<span class="os-ph" style="{style}">&#9998; {m.group(1)}</span>', s,
                  flags=re.S)


def plain(s):
    s = re.sub(f"{PH_OPEN}(.*?){PH_CLOSE}", r"[PLACEHOLDER: \1]", s, flags=re.S)
    s = s.replace("<br>", " ").replace("<wbr>", "")
    return _html.unescape(re.sub(r"<[^>]+>", "", s)).replace("–", "-").replace("\xa0", " ")


def has_ph(s):
    return PH_OPEN in s or "&#9998;" in s or "[PLACEHOLDER" in s


# --------------------------------------------------------------------------- email / browser


def head(issue):
    h = O.head()
    h = h.replace(f"<title>{O.SUBJECT}</title>", f"<title>{issue['subject']}</title>")
    h = re.sub(r"<!-- MailerLite:.*?-->\n<!-- Built by.*?-->\n<!-- T404:.*?-->\n",
               f"<!-- Subject \"{issue['subject']}\". Merge tags {{$url}} and {{$unsubscribe}}. "
               f"Built by tools/build-issues.py (same template as the Oct 2026 issue); edit tools/issue_data.py. -->\n",
               h, flags=re.S)
    return h


def img(src, alt, width=600, extra=""):
    return (f'<img class="os-card-art" src="{src}" width="{width}" alt="{alt}" '
            f'style="display:block;width:100%;max-width:100%;height:auto;border:0;outline:none;'
            f'text-decoration:none;border-radius:12px;{extra}">')


def btn(href, label, on_navy=False):
    """Small outlined pill button. Taylor's rule: buttons, never underlined text links."""
    color = GOLD if on_navy else ACCENT
    cls = "os-gold" if on_navy else "os-link"
    return (f'<a class="{cls}" href="{href}" style="display:inline-block;margin:8px 8px 0 0;'
            f'padding:7px 16px;border:1.5px solid {color};border-radius:99px;font:700 14px/18px {FONT};'
            f'color:{color};text-decoration:none;">{label}</a>')


def btn_row(links, margin="4px 0 0 0", on_navy=False):
    return (f'<div class="os-btn-row" style="margin:{margin};">'
            + "".join(btn(h, lab, on_navy) for h, lab in links) + '</div>')


def link_line(links, size=15, lh=22, margin="8px 0 0 0", cls=""):
    return btn_row(links, margin=margin)


def issue_chips(chips):
    cells = []
    for i, (href, label) in enumerate(chips):
        if i < 2:
            pad = "0 6px 8px 0" if i % 2 == 0 else "0 0 8px 6px"
        else:
            pad = "0 6px 0 0" if i % 2 == 0 else "0 0 0 6px"
        cells.append(f'<td class="os-issue-cell" width="50%" valign="top" style="width:50%;padding:{pad};">'
                     f'{O.issue_chip(href, label)}</td>')
    return (p(f'<b style="color:{ACCENT};font-weight:700;">In this issue</b>', 13, 18, MUTED, 400,
              margin="0 0 8px 0", cls="os-tiny")
            + '<table role="presentation" class="os-issue-grid" cellpadding="0" cellspacing="0" border="0" '
              'width="100%" style="width:100%;border-collapse:collapse;">'
            f'<tr>{cells[0]}{cells[1]}</tr><tr>{cells[2]}{cells[3]}</tr></table>')


def three_things(issue):
    rows = []
    groups = issue["three_things"]
    for gi, g in enumerate(groups):
        body = ""
        for ii, it in enumerate(g["items"]):
            if ii:
                body += (f'<div style="margin:14px 0 14px 0;border-top:1px solid {RULE};font-size:0;'
                         f'line-height:0;height:1px;">&nbsp;</div>')
            body += item(it["title"], [it["body"]], featured=True)
            if it.get("links"):
                body += btn_row(it["links"])
        rows.append(row(chip(*g["chip"]), body, last=(gi == len(groups) - 1), featured=True))
    return rows_table(rows)


def photo_cell(g, art):
    if g.get("photo"):
        return (f'<img class="os-vh-portrait" src="{art(g["photo"])}" width="88" height="115" alt="{g["photo_alt"]}" '
                'style="display:block;width:88px;max-width:88px;height:auto;border:0;outline:none;text-decoration:none;border-radius:10px;">')
    return ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="88" '
            'style="width:88px;border-collapse:separate;border:1px dashed #b8912f;border-radius:10px;background-color:#fff1b8;">'
            f'<tr><td align="center" style="height:113px;padding:4px;">{p(PH_OPEN + "Photo" + PH_CLOSE, 12, 16, INK, 700, extra="text-align:center;")}</td></tr></table>')


def guest_block(g, art):
    return (
        '<table role="presentation" class="os-vh-guest" cellpadding="0" cellspacing="0" border="0" width="100%" '
        'style="width:100%;border-collapse:collapse;margin:0 0 16px 0;">'
        '<tr><td colspan="2" class="os-vh-guestname" align="center" '
        'style="padding:0 0 10px 0;vertical-align:top;text-align:center;">'
        + p(g["name"], 15, 20, GOLD, 700, margin="0 0 2px 0", extra="text-align:center;")
        + p(g["role"], 13, 18, SAND, 700, margin="0", extra="text-align:center;white-space:nowrap;",
            cls="os-vh-guestrole")
        + '</td></tr><tr>'
        f'<td class="os-vh-guestphoto" width="88" valign="middle" style="width:88px;padding:0 12px 0 0;vertical-align:middle;">'
        + photo_cell(g, art)
        + '</td><td class="os-vh-guestblurb" valign="middle" align="left" style="padding:0;vertical-align:middle;text-align:left;">'
        + p(g["bio"], 13, 19, SAND, 400, extra="text-align:left;")
        + "".join(p(navy_a(h, lab, nowrap=False), 13, 18, SAND, 400, margin="8px 0 0 0" if i == 0 else "2px 0 0 0",
                    extra="text-align:left;", cls="os-vh-contact") for i, (h, lab) in enumerate(g.get("links", [])))
        + '</td></tr></table>'
    )


def village_hall(issue, art):
    vh = issue["village_hall"]
    guests = vh.get("guests") or ([vh["guest"]] if vh.get("guest") else [])
    guest = "".join(guest_block(g, art) for g in guests) if guests else (
        p(vh["guest_placeholder"], 14, 21, SAND, 400, margin="0 0 16px 0"))
    panel = (
        f'<table role="presentation" class="os-navy" cellpadding="0" cellspacing="0" border="0" width="100%" '
        f'bgcolor="{INK}" style="width:100%;border-collapse:separate;background-color:{INK};border-radius:16px;">'
        '<tr><td align="left" style="padding:16px 18px 20px 18px;">'
        + p(vh["date"], 13, 18, GOLD, 700, margin="0 0 4px 0")
        + vh_meta_icon("clock-gold", vh["time"], bottom="4px")
        + vh_meta_icon("video-gold", "Online", bottom="18px")
        + p("Topic and guests" if len(guests) > 1 else "Topic and guest", 13, 18, GOLD, 700, margin="0 0 6px 0")
        + p(vh["topic"], 17, 24, CREAM, 700, margin="0 0 14px 0")
        + guest
        + p(vh["about"], 14, 21, SAND, 400, margin="0 0 16px 0")
        + button(f"{SITE}/village-hall", vh.get("button", "Register for Village Hall"), GOLD, INK)
          .replace('class="os-btn"', 'class="os-btn os-btn-gold"')
        + price_boxes()
        + '</td></tr></table>')
    stack = (f'<div class="os-vh-stack" style="display:block;width:100%;">'
             f'<div class="os-browser-col" style="display:block;width:100%;margin:0 0 10px 0;vertical-align:top;box-sizing:border-box;">'
             f'{img(art("village-hall.jpg"), vh["art_alt"])}</div>'
             f'<div class="os-browser-col" style="display:block;width:100%;margin:0;vertical-align:top;box-sizing:border-box;">{panel}</div>'
             '</div>')
    return (padrow(anchor("village-hall") + rule()
                   + p("The next deep dive", 13, 18, ACCENT, 700, margin="12px 0 0 0")
                   + (f'<h2 class="os-h2 os-ink" style="margin:6px 0 0 0;font-family:{FONT};font-size:21px;'
                      f'line-height:27px;mso-line-height-rule:exactly;color:{INK};font-weight:700;">Village Hall</h2>')
                   + p("One topic. One guest expert. Your questions.", 16, 24, BODY, 400, margin="6px 0 0 0"))
            + sp(12) + padrow(stack, pad="0 34px"))


def month_ahead(issue, art):
    ev = issue["events"]
    f = ev["featured"]
    link = f.get("link")
    art_html = img(f.get("photo_url") or art(f.get("photo", "featured.jpg")), f["art_alt"], extra="")
    if link:
        art_html = f'<a href="{link[0]}" style="display:block;text-decoration:none;border:0;outline:none;">{art_html}</a>'
    copy = (p("Featured", 13, 18, ACCENT, 700, margin="12px 0 0 0")
            + p(f["title"], 18, 25, INK, 700, margin="6px 0 0 0")
            + p(f["meta"], 16, 24, BODY, 400, margin="6px 0 0 0")
            + (p(f["blurb"], 15, 22, BODY, 400, margin="6px 0 0 0") if f.get("blurb") else "")
            + (btn_row([link]) if link else ""))
    out = [section_head("events", "The month ahead", ev.get(
        "intro", "Picked for sensory-sensitive kids and their families. Drive times are from Murfreesboro.")),
           sp(12), padrow(card(art_html + copy, pad="12px 20px 16px 20px"))]
    if ev["list"]:
        rows = []
        for i, e in enumerate(ev["list"]):
            content = item(e["title"], [e["meta"]])
            if e.get("link"):
                content += btn_row([e["link"]])
            if e.get("disclose"):
                content += disclose(e["disclose"])
            rows.append(row(chip(*e["chip"]), content, last=(i == len(ev["list"]) - 1), tight=True))
        out += [sp(16), padrow(card(rows_table(rows), pad="6px 20px 6px 20px"))]
    if ev.get("note"):
        out += [sp(12), padrow(p(ev["note"], 14, 21, MUTED, 400, extra="text-align:center;"))]
    out += [sp(20), padrow(button(f"{SITE}/events", ev["calendar_label"], INK, CREAM, align="center")
                           .replace('class="os-btn"', 'class="os-btn os-btn-navy"'))]
    return "\n".join(out)


def wall_of_hope(issue, art):
    h = issue["hope"]
    quote = (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" '
             f'style="width:100%;border-collapse:collapse;margin:12px 0 0 0;"><tr>'
             f'<td width="3" bgcolor="{GOLD}" style="width:3px;background-color:{GOLD};border-radius:2px;font-size:0;">&nbsp;</td>'
             f'<td style="padding:2px 0 2px 14px;">'
             + p(h["quote"], 17, 25, INK, 700)
             + p(h["who"], 14, 20, MUTED, 400, margin="8px 0 0 0")
             + '</td></tr></table>')
    inner = (img(art("wall-of-hope.jpg"), h["art_alt"])
             + p("From the Wall of Hope", 13, 18, ACCENT, 700, margin="12px 0 0 0")
             + quote
             + link_line([(f"{SITE}/hope", "Read more stories"), (f"{SITE}/hope", "Share yours")],
                         margin="14px 0 0 0"))
    return (section_head("hope", "A little hope", "Real words from local parents, shared with permission.")
            + sp(12) + padrow(card(inner, pad="12px 20px 16px 20px")))


def library(issue, art):
    cards = []
    for i, g in enumerate(issue["guides"], start=1):
        inner = (img(art(f"guide-{i}.jpg"), g["art_alt"], width=490, extra="margin:0 0 12px 0;")
                 .replace('width="490"', 'width="490" height="228"')
                 + p(g["label"], 13, 18, ACCENT, 700, cls="os-tiny")
                 + p(g["title"], 17, 24, INK, 700, margin="6px 0 0 0")
                 + p(g["blurb"], 15, 22, BODY, 400, margin="8px 0 0 0")
                 + '<div class="os-card-cta">'
                 + btn_row([(SITE + g["path"], g.get("cta", "Read the guide"))]) + '</div>')
        cards.append(card(inner, pad="16px 16px 16px 16px"))
    return (section_head("library", issue.get("library_title", "From the library")) + sp(12)
            + padrow(O.browser_cols(*cards, gap=16)))


def question(issue):
    q = issue["question"]
    steps = rows_table([step(i + 1, f'{b(t)} {body.replace("{STEP}", tel("800-280-7837", "+18002807837"))}',
                             last=(i == len(q["steps"]) - 1))
                        for i, (t, body) in enumerate(q["steps"])])
    qa = (p(f"{issue['month']}&rsquo;s question", 13, 18, ACCENT, 700, margin="0 0 6px 0")
          + p(f"&ldquo;{q['q']}&rdquo;", 18, 25, INK, 700)
          + p(q["short"], 16, 24, BODY, 400, margin="10px 0 12px 0")
          + steps
          + f'<div style="margin:16px 0 0 0;border-top:1px solid {RULE};font-size:0;line-height:0;height:1px;">&nbsp;</div>'
          + link_line(q["links"] + [(f"{SITE}/contact", "Send us your question")], margin="6px 0 0 0")
          + p(q.get("disclaimer", "Parent-to-parent guidance, not medical or legal advice."), 13, 20, MUTED, 400,
              margin="10px 0 0 0", cls="os-tiny"))
    return (section_head("question", "One question, answered",
                         "One real question from a local parent, answered plainly.")
            + sp(12) + padrow(card(qa, pad="16px 20px 14px 20px")))


def connect(issue):
    online = group_card(
        [], "Our Special Village Online Parent Group",
        [("calendar", "Thursdays"), ("clock", "7:00&ndash;8:00 PM Central"), ("video", "Online")],
        "Connect with parents and caregivers of neurodivergent and disabled children "
        "in a welcoming, judgment-free space.",
        ["No formal diagnosis required", issue.get("group_line", "Drop in any Thursday"),
         "Cameras are optional", "Meetings are never recorded"],
        f"{SITE}/group", "Join the Online Group", secondary=["ONLINE", "WEEKLY", "FREE"])
    werock = group_card(
        [], "We Rock the Spectrum Parent Group",
        [("calendar", "Wednesdays at 5:00 PM"), ("pin", "We Rock the Spectrum Murfreesboro")],
        "Connect with other parents of kids with special needs while children enjoy the gym. "
        "Gym staff watch the kids during group; childcare is available but not appropriate for all children.",
        ["Led by Cari Parr", "$15 per child for kids to play",
         "Gym staff watch children during group; not appropriate for all children",
         "Discounted gym admission is available separately."],
        O.WRTS_URL, "Plan Your Visit", secondary=["IN PERSON", "WEEKLY", "FREE"])
    return (section_head("ongoing", "Connect with other local parents") + sp(12)
            + padrow('<div class="os-browser-cols os-equal-pair" style="display:block;width:100%;">'
                     f'<div class="os-browser-col" style="display:block;width:100%;margin:0 0 16px 0;vertical-align:top;box-sizing:border-box;">{online}</div>'
                     f'<div class="os-browser-col" style="display:block;width:100%;margin:0;vertical-align:top;box-sizing:border-box;">{werock}</div>'
                     '</div>'))


def build_html(issue, base, browser, deadlines_url, view_url):
    """Mirror of O.build_html with this issue's content. Section order matches October,
    with the Wall of Hope added between the library and the question."""
    art = lambda f: f"{base}{f}"
    o = [head(issue)]
    o.append(f'<body id="os-body" class="os-bg" bgcolor="{CREAM}" style="margin:0;padding:0;background-color:{CREAM};width:100%;max-width:100%;overflow-x:hidden;">')
    o.append(f'<span style="display:none;font-size:1px;color:{CREAM};line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{plain(issue["preheader"])}</span>')
    o.append(f'<table role="presentation" class="os-bg" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="{CREAM}" style="width:100%;border-collapse:collapse;background-color:{CREAM};">'
             '<tr><td align="center" style="padding:20px 12px 40px 12px;">'
             '<table role="presentation" class="os-wrap" cellpadding="0" cellspacing="0" border="0" width="600" style="width:100%;max-width:600px;border-collapse:collapse;">')
    view_href = view_url if browser else "{$url}"
    unsub_href = O.BROWSER_UNSUB_URL if browser else "{$unsubscribe}"
    o.append(padrow(p(f'<a class="os-muted os-tiny" href="{view_href}" style="color:{MUTED};text-decoration:underline;">View in browser</a>',
                      13, 18, MUTED, 400, extra="text-align:center;", cls="os-tiny"), pad="0 34px 12px 34px"))
    o.append(padrow(
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;"><tr>'
        f'<td align="left" style="vertical-align:middle;">{p("Our Special Village", 12, 16, ACCENT, 700, extra="letter-spacing:1.6px;text-transform:uppercase;")}</td>'
        f'<td align="right" style="vertical-align:middle;">{p(issue["month_year"], 13, 16, MUTED, 700, extra="text-align:right;")}</td>'
        '</tr></table>', pad="0 34px 14px 34px"))
    o.append('<tr><td align="left" style="padding:0;">'
             f'<img class="os-hero" src="{art("hero.jpg")}" width="600" alt="{issue["hero_alt"]}" '
             'style="display:block;width:100%;max-width:600px;height:auto;border:0;outline:none;text-decoration:none;border-radius:16px;"></td></tr>')
    o.append(sp(16))

    paras = []
    for i, para in enumerate(issue["note"]):
        hi = issue.get("note_highlight")
        if hi and hi in para:
            para = para.replace(hi, f'<span style="background-color:{BLUSH};color:{INK};padding:1px 4px;border-radius:4px;">{hi}</span>')
        paras.append(p(para, 16, 24, BODY, 400, margin=("0" if i == 0 else "8px 0 0 0")))
    note_copy = (f'<h1 class="os-h1 os-ink" style="margin:0 0 10px 0;font-family:{FONT};font-size:30px;line-height:36px;'
                 f'mso-line-height-rule:exactly;color:{INK};font-weight:700;letter-spacing:-0.3px;">{issue["month"]} in Our Special Village</h1>'
                 + "".join(paras)
                 + p("With love,", 16, 24, BODY, 400, margin="10px 0 2px 0")
                 + f'<img class="os-sig" src="{art("signature-taylor.png")}" width="96" height="55" alt="Taylor" '
                   f'style="display:block;width:96px;max-width:96px;height:auto;margin:0 0 0 8px;padding:0;border:0;outline:none;'
                   f'text-decoration:none;font-family:Georgia, Times New Roman, serif;font-size:22px;font-style:italic;color:{ACCENT};">')
    photo = (f'<img class="os-intro-photo" src="{art("taylor-hickok-160.jpg")}" width="96" height="96" '
             'alt="Dr. Taylor Hickok, founder of Our Special Village." '
             'style="display:block;width:96px;max-width:96px;height:96px;margin:0 auto;padding:0;border:0;outline:none;'
             'text-decoration:none;border-radius:50%;object-fit:cover;">')
    photo_block = ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;">'
                   f'<tr><td class="os-intro-photocell" align="center" style="padding:0 0 8px 0;">{photo}</td></tr>'
                   '<tr><td class="os-intro-byline" align="center" style="padding:0;">'
                   + p("Dr. Taylor Hickok", 15, 20, INK, 700, extra="text-align:center;")
                   + p("Founder &middot; SLP &middot; AuDHD parent", 13, 18, MUTED, 400, margin="2px 0 0 0",
                       extra="text-align:center;white-space:nowrap;", cls="os-tiny os-cred")
                   + '</td></tr></table>')
    o.append(padrow(
        '<div class="os-browser-cols os-intro-cols" style="display:block;width:100%;">'
        f'<div class="os-browser-col os-intro-photo-col" style="display:block;width:100%;margin:0 0 12px 0;vertical-align:top;box-sizing:border-box;">{photo_block}</div>'
        f'<div class="os-browser-col os-intro-text-col" style="display:block;width:100%;margin:0;vertical-align:top;box-sizing:border-box;">{note_copy}</div>'
        '</div>'))
    o.append(sp(6))
    o.append(padrow('<div style="margin:0;">' + issue_chips(issue["chips"]) + '</div>'))

    o.append(major_sp())
    o.append(section_head("deadlines", "Three things to know this month"))
    o.append(sp(12))
    o.append(padrow(card(three_things(issue), pad="8px 20px 8px 20px")))
    o.append(sp(14))
    o.append(padrow(button(deadlines_url, "See all deadlines", INK, CREAM).replace('class="os-btn"', 'class="os-btn os-btn-navy"')
                    + p(issue["confirmed"], 13, 20, MUTED, 400, margin="8px 0 0 0", cls="os-confirm")))

    o.append(major_sp())
    o.append(village_hall(issue, art))
    o.append(major_sp())
    o.append(month_ahead(issue, art))
    o.append(major_sp())
    o.append(library(issue, art))
    o.append(major_sp())
    o.append(wall_of_hope(issue, art))
    o.append(major_sp())
    o.append(question(issue))
    o.append(major_sp())
    o.append(connect(issue))

    # About, numbers, forward, footer: identical to October.
    o.append(major_sp())
    about_copy = ((f'<h2 class="os-ink" style="margin:0;font-family:{FONT};font-size:17px;line-height:23px;'
                   f'mso-line-height-rule:exactly;color:{INK};font-weight:700;">About Our Special Village</h2>')
                  + p(O.ABOUT, 14, 21, BODY, 400, margin="6px 0 0 0")
                  + btn_row([(f"{SITE}/about", "About the Village"), (f"{SITE}/editorial-policy", "How we check information")]))
    about_photo = (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="160" class="os-photocell" bgcolor="{BLUSH}" '
                   f'style="width:160px;border-collapse:separate;background-color:{BLUSH};border-radius:12px;">'
                   f'<tr><td class="os-photocell" align="center" style="width:160px;vertical-align:middle;border-radius:12px;">'
                   f'<img class="os-photo" src="{art("about-family-bowling-small.jpg")}" width="160" height="160" alt="Taylor, her husband, and their daughter at a bowling alley." '
                   f'style="display:block;width:160px;max-width:100%;height:auto;margin:0;border:0;outline:none;text-decoration:none;border-radius:12px;font-family:{FONT};font-size:13px;line-height:18px;color:{BODY};"></td></tr></table>')
    o.append(padrow(card(f'<div class="os-about-row" style="display:block;width:100%;">'
                         f'<div class="os-about-photo" style="display:block;width:160px;max-width:160px;margin:0 0 16px 0;">{about_photo}</div>'
                         f'<div class="os-about-text" style="display:block;width:100%;">{about_copy}</div></div>',
                         pad="14px 16px 14px 16px")))
    o.append(sp(12))
    nums = p("Numbers worth keeping", 14, 20, ACCENT, 700, margin="0 0 4px 0") + "".join(
        p(t, 14, 20, BODY, 400, margin="4px 0 0 0") for t in O.NUMBERS)
    o.append(padrow(card(nums, pad="12px 16px 12px 16px")))
    o.append(sp(16))
    o.append(padrow(p("Know a family who could use this? Forward it along. Anyone can join at "
                      + a(f"{SITE}/newsletter", "ourspecialvillagetn.com/newsletter", nowrap=False) + ".", 14, 21, BODY, 400, extra="text-align:center;")))
    o.append(sp(20))
    o.append(f'<tr><td class="os-pad" style="padding:0 34px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;"><tr><td class="os-rule" style="border-top:1px solid {HAIR};font-size:0;line-height:0;height:1px;">&nbsp;</td></tr></table></td></tr>')
    o.append(sp(14))
    footer = (p("Our Special Village &middot; Murfreesboro and surrounding areas, Tennessee", 14, 21, INK, 700, margin="0 0 6px 0")
              + p("Local businesses and practices help keep the Village free and ad-free. " + a(f"{SITE}/sponsors", "Sponsorship options", nowrap=False) + ".", 13, 20, BODY, 400, margin="0 0 12px 0")
              + p("You are receiving this because you joined the newsletter list at ourspecialvillagetn.com.<br>"
                  + a(unsub_href, "Unsubscribe in one click", nowrap=False) + " &nbsp;&middot;&nbsp; " + a(f"{SITE}/privacy", "Privacy") + " &nbsp;&middot;&nbsp; " + a(f"{SITE}/contact", "Contact"), 13, 20, BODY, 400, margin="0 0 10px 0", cls="os-tiny")
              + p("Our Special Village is owned and operated by Little Luminaries Therapy Services, PLLC<br>1810 Ward Dr, Suite 101, Murfreesboro, TN 37129", 13, 19, BODY, 400, cls="os-tiny"))
    o.append(padrow('<div class="os-footer">' + footer + '</div>'))
    o.append('</table></td></tr></table></body></html>')
    out = "\n".join(o) + "\n"
    out = out.replace(f"{PAGES}art/icons/", f"{base}icons/")  # O.meta_row / vh_meta_icon hard-code Pages
    out = out.replace("text-decoration:underline", "text-decoration:none")  # Taylor: no underlined links
    return render_ph(out)


# --------------------------------------------------------------------------- plain text


def build_text(issue, deadlines_url):
    L = []
    w = L.append
    w(f"OUR SPECIAL VILLAGE · {issue['month_year']}")
    w("View this email in your browser: {$url}")
    w("")
    w(f"{issue['month'].upper()} IN OUR SPECIAL VILLAGE")
    w("")
    for para in issue["note"]:
        w(plain(para))
        w("")
    w("With love,")
    w("Taylor")
    w("")
    w("In this issue: " + " · ".join(plain(lab) for _, lab in issue["chips"]))
    w("")
    w("----------------------------------------")
    w("THREE THINGS TO KNOW THIS MONTH")
    w("")
    for g in issue["three_things"]:
        dow, day, moy = g["chip"]
        for it in g["items"]:
            weekday = dow in ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
            w(f"{dow} {plain(moy)} {day} · {plain(it['title'])}" if weekday else plain(it["title"]))
            w("  " + plain(it["body"]))
            for h, lab in it.get("links", []):
                w(f"  {plain(lab)}: {h}")
            w("")
    w(f"See all deadlines: {deadlines_url}")
    w(plain(issue["confirmed"]))
    w("")
    w("----------------------------------------")
    w("THE NEXT DEEP DIVE · VILLAGE HALL")
    w("")
    vh = issue["village_hall"]
    w(f"Village Hall: {plain(vh['date'])}")
    w(plain(vh["time"]))
    w("Online")
    w(f"Topic and guest: {plain(vh['topic'])}")
    guests = vh.get("guests") or ([vh["guest"]] if vh.get("guest") else [])
    for g in guests:
        w(f"{plain(g['name'])} - {plain(g['role'])}. {plain(g['bio'])}")
        for h, lab in g.get("links", []):
            w(f"{plain(lab)}: {h}")
    if not guests:
        w(plain(vh["guest_placeholder"]))
    w(plain(vh["about"]))
    w(f"{plain(vh.get('button', 'Register for Village Hall'))}: {SITE}/village-hall")
    w("Choose what you can pay: Every family is welcome - choose $0, or give more to help cover another seat. $0 Welcome / $10 Helps / $20 Suggested / $35 Pay it forward")
    w("The meeting link is emailed to registrants.")
    w("")
    w("----------------------------------------")
    w("THE MONTH AHEAD")
    ev = issue["events"]
    w(plain(ev.get("intro", "Picked for sensory-sensitive kids and their families. Drive times are from Murfreesboro.")))
    w("")
    f = ev["featured"]
    w(f"{plain(f['title'])}  [Featured]")
    w(f"  {plain(f['meta'])}")
    if f.get("blurb"):
        w(f"  {plain(f['blurb'])}")
    if f.get("link"):
        w(f"  {plain(f['link'][1])}: {f['link'][0]}")
    w("")
    for e in ev["list"]:
        w(plain(e["title"]))
        w(f"  {plain(e['meta'])}")
        for extra in e.get("disclose") or []:
            w(f"  {plain(extra)}")
        if e.get("link"):
            w(f"  {plain(e['link'][1])}: {e['link'][0]}")
        w("")
    if ev.get("note"):
        w(plain(ev["note"]))
        w("")
    w(f"{plain(ev['calendar_label'])}: {SITE}/events")
    w("")
    w("----------------------------------------")
    w(issue.get("library_title", "From the library").upper())
    w("")
    for g in issue["guides"]:
        w(f"{plain(g['label'])} · {plain(g['title'])}")
        w(f"  {plain(g['blurb'])}")
        w(f"  {plain(g.get('cta', 'Read the guide'))}: {SITE}{g['path']}")
        w("")
    w("----------------------------------------")
    w("A LITTLE HOPE")
    w("From the Wall of Hope")
    w("")
    w(plain(issue["hope"]["quote"]))
    w(plain(issue["hope"]["who"]))
    w(f"Read more stories or share yours: {SITE}/hope")
    w("")
    w("----------------------------------------")
    w("ONE QUESTION, ANSWERED")
    w(f"Send us yours: {SITE}/contact")
    w("")
    q = issue["question"]
    w(f"{issue['month']}'s question: \"{plain(q['q'])}\"")
    w(plain(q["short"]))
    w("")
    for i, (t, body) in enumerate(q["steps"], start=1):
        w(f"{i}. {plain(t)} {plain(body.replace('{STEP}', '800-280-7837'))}")
    w("")
    for h, lab in q["links"]:
        w(f"{plain(lab)}: {h}")
    w(plain(q.get("disclaimer", "Parent-to-parent guidance, not medical or legal advice.")))
    w("")
    w("----------------------------------------")
    w("CONNECT WITH OTHER LOCAL PARENTS")
    w("")
    w("Our Special Village Online Parent Group")
    w("  ONLINE · WEEKLY · FREE")
    w("  Thursdays · 7:00-8:00 PM Central · Online")
    w("  Connect with parents and caregivers of neurodivergent and disabled children in a welcoming, judgment-free space.")
    w(f"  Good to know: No formal diagnosis required; {plain(issue.get('group_line', 'Drop in any Thursday'))}; Cameras are optional; Meetings are never recorded.")
    w(f"  Join the Online Group: {SITE}/group")
    w("")
    w("We Rock the Spectrum Parent Group")
    w("  IN PERSON · WEEKLY · FREE")
    w("  Wednesdays at 5:00 PM · We Rock the Spectrum Murfreesboro")
    w("  Connect with other parents of kids with special needs while children enjoy the gym. Gym staff watch the kids during group; childcare is available but not appropriate for all children.")
    w("  Good to know: Led by Cari Parr; $15 per child for kids to play; Gym staff watch children during group; not appropriate for all children; Discounted gym admission is available separately.")
    w(f"  Plan Your Visit: {O.WRTS_URL}")
    w("")
    w("----------------------------------------")
    w("ABOUT OUR SPECIAL VILLAGE")
    w("")
    w(O.ABOUT)
    w("")
    w(f"About the Village: {SITE}/about")
    w(f"How we check information: {SITE}/editorial-policy")
    w("")
    w("NUMBERS WORTH KEEPING")
    w("988 Suicide & Crisis Lifeline · Call or text any hour.")
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


# --------------------------------------------------------------------------- deadlines page


def build_deadlines(issue, back_url, back_label):
    sections = []
    for title, items in issue["all_deadlines"]:
        rows = "".join(O.deadline_item(dow, day, moy, t, body) for dow, day, moy, t, body in items)
        sections.append(f"<h2>{title}</h2>\n{rows}")
    page = O.build_deadlines_page()
    head_part = page.split("<main>", 1)[0]
    head_part = head_part.replace("</style>", (
        f".body a{{display:inline-block;margin:8px 8px 0 0;padding:6px 14px;border:1.5px solid {ACCENT};"
        "border-radius:999px;text-decoration:none;font-size:14px;line-height:18px;white-space:nowrap;}"
        ".back a{text-decoration:none;}\n</style>"))
    head_part = re.sub(r"<title>.*?</title>", f"<title>{issue['month_year']} deadlines · Our Special Village</title>", head_part)
    body = (f'<main>\n<p class="back"><a href="{back_url}">&larr; {back_label}</a></p>\n'
            f"<h1>All {issue['month']} deadlines</h1>\n"
            f'<p class="meta">{issue["deadlines_meta"]}</p>\n'
            + "\n".join(sections)
            + '\n<p class="meta" style="margin-top:28px;">If something changed, reply to the newsletter. A person reads it.</p>\n'
            "</main></body></html>\n")
    return render_ph(head_part + body)


# --------------------------------------------------------------------------- checks


def check(issue, email, browser, txt, deadlines):
    for s in (email, browser, txt, deadlines):
        assert "—" not in s and "&mdash;" not in s, f"{issue['id']}: em dash"
        assert "October" not in s.replace("October 1", ""), f"{issue['id']}: leftover October copy"
        assert "Mercedes" not in s and "Spooktacular" not in s
        assert "Microsoft Teams" not in s
    assert "{$url}" in email and "{$unsubscribe}" in email and "{$url}" in txt and "{$unsubscribe}" in txt
    assert 'href="{$url}"' not in browser and 'href="{$unsubscribe}"' not in browser
    assert "tmacocx.github.io/osv-newsletter-october-preview/art/" not in email
    assert "Three things to know this month" in email and "See all deadlines" in email
    assert email.count("Register for Village Hall") <= 1
    assert f"{issue['month']} in Our Special Village" in email
    assert 'href="tel:988"' in email
    order = ["id=\"deadlines\"", "id=\"village-hall\"", "id=\"events\"", "id=\"library\"",
             "id=\"hope\"", "id=\"question\"", "id=\"ongoing\""]
    idx = [email.find(x) for x in order]
    assert all(i > 0 for i in idx) and idx == sorted(idx), f"{issue['id']}: section order {idx}"
    for href, _ in issue["chips"]:
        assert f'id="{href[1:]}"' in email, href
    assert len(issue["three_things"]) >= 1
    assert len(issue["guides"]) == 2
    text = re.sub(r"<style.*?</style>", " ", email, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    words = len(re.sub(r"&\w+;", " ", text).split())
    assert 850 <= words <= 1600, f"{issue['id']}: word count {words}"
    assert len(email.encode()) < 102_000, f"{issue['id']}: {len(email.encode())}B would clip in Gmail"
    return words


# --------------------------------------------------------------------------- main


def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


def picker(issues):
    tabs = "".join(
        f'<button role="tab" data-id="{i["id"]}" aria-selected="{"true" if n == 0 else "false"}">{i["month"]}</button>'
        for n, i in enumerate(issues))
    todo = "".join(
        f'<section data-for="{i["id"]}"{" hidden" if n else ""}><h2>Still to fill in for {i["month"]}</h2><ul>'
        + "".join(f"<li>{t}</li>" for t in i["todo"]) + "</ul></section>"
        for n, i in enumerate(issues))
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Newsletters Nov to Feb</title>
<style>
:root{{--bg:{CREAM};--ink:{INK};--body:{BODY};--accent:{ACCENT};--card:#fff;--hair:{HAIR};}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--body);font-family:{FONT};}}
header{{position:sticky;top:0;z-index:2;background:var(--bg);border-bottom:1px solid var(--hair);padding:12px 16px;}}
.wrap{{max-width:980px;margin:0 auto;}}
h1{{margin:0 0 8px;color:var(--ink);font-size:18px;}}
.tabs{{display:flex;gap:8px;flex-wrap:wrap;}}
.tabs button{{font:inherit;font-weight:700;border:1px solid var(--hair);background:var(--card);color:var(--ink);border-radius:999px;padding:8px 16px;cursor:pointer;}}
.tabs button[aria-selected=true]{{background:var(--ink);color:{CREAM};border-color:var(--ink);}}
.row{{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:8px;font-size:14px;}}
.row a{{color:var(--accent);font-weight:700;}}
.row label{{display:flex;gap:6px;align-items:center;}}
.todo{{max-width:980px;margin:12px auto 0;padding:0 16px;}}
.todo section{{background:#fff8dc;border:1px dashed #b8912f;border-radius:12px;padding:10px 16px;font-size:14px;}}
.todo h2{{font-size:15px;margin:4px 0;color:var(--ink);}}
.todo ul{{margin:4px 0 6px;padding-left:18px;}}
.frame{{max-width:980px;margin:12px auto 32px;padding:0 16px;}}
iframe{{display:block;width:100%;height:80vh;min-height:600px;border:1px solid var(--hair);border-radius:12px;background:{CREAM};margin:0 auto;}}
iframe.phone{{width:390px;max-width:100%;}}
</style></head><body>
<header><div class="wrap"><h1>Our Special Village newsletters, November to February</h1>
<div class="tabs" role="tablist">{tabs}</div>
<div class="row"><label><input type="checkbox" id="phone"> Phone width</label>
<a id="open" href="{issues[0]['id']}/index.html" target="_blank" rel="noopener">Open full page</a>
<a id="dl" href="{issues[0]['id']}/deadlines.html" target="_blank" rel="noopener">All deadlines page</a></div></div></header>
<div class="todo">{todo}</div>
<div class="frame"><iframe id="f" title="Newsletter preview" src="{issues[0]['id']}/index.html"></iframe></div>
<script>
const f=document.getElementById('f'),open=document.getElementById('open'),dl=document.getElementById('dl');
function show(id){{f.src=id+'/index.html';open.href=id+'/index.html';dl.href=id+'/deadlines.html';
document.querySelectorAll('.tabs button').forEach(b=>b.setAttribute('aria-selected',b.dataset.id===id));
document.querySelectorAll('.todo section').forEach(s=>s.hidden=s.dataset.for!==id);
try{{localStorage.setItem('osv-nl-tab',id)}}catch(e){{}}}}
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>show(b.dataset.id));
document.getElementById('phone').onchange=e=>f.classList.toggle('phone',e.target.checked);
try{{const t=localStorage.getItem('osv-nl-tab');if(t&&document.querySelector('[data-id="'+t+'"]'))show(t)}}catch(e){{}}
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-export", help="also write newsletters/<id>/ and public/assets/newsletters/<id>/ into this site repo")
    ap.add_argument("--strict", action="store_true", help="fail while any placeholder remains")
    args = ap.parse_args()
    for issue in D.ISSUES:
        iid = issue["id"]
        folder = os.path.join(ROOT, "issues", iid)
        # Preview (relative art so it works anywhere the folder is hosted)
        email = build_html(issue, "art/", False, "deadlines.html", "index.html")
        browser = build_html(issue, "art/", True, "deadlines.html", "index.html")
        txt = build_text(issue, "deadlines.html")
        deadlines = build_deadlines(issue, "index.html", f"{issue['month']} newsletter preview")
        words = check(issue, email, browser, txt, deadlines)
        write(os.path.join(folder, "email.html"), email)
        write(os.path.join(folder, "index.html"), browser)
        write(os.path.join(folder, "email.txt"), txt)
        write(os.path.join(folder, "deadlines.html"), deadlines)
        n_ph = email.count("&#9998;")
        if args.strict:
            assert not n_ph and not has_ph(txt), f"{iid}: {n_ph} placeholders left"
        print(f"{iid}: email {len(email.encode())}B, words≈{words}, placeholders {n_ph}")

        if args.site_export:
            site = os.path.abspath(args.site_export)
            base = f"{{$site}}/assets/newsletters/{iid}/"
            dl_url = f"{{$site}}/newsletter/{iid}/deadlines"
            s_email = build_html(issue, base, False, dl_url, "{$url}")
            s_txt = build_text(issue, f"{SITE}/newsletter/{iid}/deadlines")
            s_dl = build_deadlines(issue, "{$url}", f"{issue['month']} newsletter")
            nd = os.path.join(site, "newsletters", iid)
            write(os.path.join(nd, "email.html"), s_email)
            write(os.path.join(nd, "email.txt"), s_txt)
            write(os.path.join(nd, "deadlines.html"), s_dl)
            meta = (
                "{\n"
                f'  "id": "{iid}",\n'
                f'  "subject": "{issue["subject"]}",\n'
                f'  "preheader": "{plain(issue["preheader"])}",\n'
                f'  "send_on": "{issue["send_on"]}",\n'
                '  "send_time": "09:00",\n'
                '  "pages": { "deadlines": "deadlines.html" }\n'
                "}\n")
            write(os.path.join(nd, "issue.json"), meta)
            ad = os.path.join(site, "public", "assets", "newsletters", iid)
            if os.path.isdir(ad):
                shutil.rmtree(ad)
            shutil.copytree(os.path.join(folder, "art"), ad)
    write(os.path.join(ROOT, "issues", "index.html"), picker(D.ISSUES))


if __name__ == "__main__":
    main()
