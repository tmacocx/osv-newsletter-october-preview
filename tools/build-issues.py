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
sp, major_sp, padrow, anchor = O.sp, O.major_sp, O.padrow, O.anchor
section_head, card, rows_table, row, chip, item = (O.section_head, O.card, O.rows_table,
                                                    O.row, O.chip, O.item)
button, group_card, step, price_boxes, disclose = (
    O.button, O.group_card, O.step, O.price_boxes, O.disclose)
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
    h = re.sub(r"<!-- MailerLite:.*?-->\n<!-- Built by.*?-->\n",
               f"<!-- Subject \"{issue['subject']}\". Merge tags {{$url}} and {{$unsubscribe}}. "
               f"Built by tools/build-issues.py (same template as the Oct 2026 issue); edit tools/issue_data.py. -->\n",
               h, flags=re.S)
    return h


def pic(src, alt, width=600, height=None, style="border-radius:12px;", cls="os-card-art"):
    return O.img(src, width, alt, height, style=style, cls=cls)


def btn_row(links, margin="4px 0 0 0", kind=None):
    """Taylor's rule: buttons, never underlined text links."""
    return O.pill_row(links, margin=margin, kind=kind)


def three_things(issue):
    rows = []
    groups = issue["three_things"]
    for gi, g in enumerate(groups):
        body = ""
        for ii, it in enumerate(g["items"]):
            if ii:
                body += (f'<div style="margin:14px 0 14px 0;border-top:1px solid {O.TAG_RULE};font-size:0;'
                         f'line-height:0;height:1px;">&nbsp;</div>')
            body += item(it["title"], [it["body"]], featured=True)
            if it.get("links"):
                body += btn_row(it["links"])
        rows.append(row(chip(*g["chip"]), body, last=(gi == len(groups) - 1), featured=True, line=O.TAG_RULE))
    return rows_table(rows)


def village_hall(issue, art):
    """Same pieces as October: bunting, the hall in its landscape, fact pills, the notice board, the ticket."""
    vh = issue["village_hall"]
    guests = vh.get("guests") or ([vh["guest"]] if vh.get("guest") else [])
    photo_ph = p(ph("Photo"), 13, 18, INK, 700, extra="text-align:center;")
    if guests:
        guests_html = "".join(
            O.guest_block(g, art, first=(i == 0),
                          photo_src=art(f"guest-{i + 1}-print.jpg") if g.get("photo") else None,
                          placeholder=photo_ph)
            for i, g in enumerate(guests))
    else:
        guests_html = p(vh["guest_placeholder"], 15, 23, BODY, 400)
    out = [O.fullrow(O.img(art(O.DECOR + "bunting.png"), 600, "", style="max-width:none;")),
           padrow(anchor("village-hall") + O.hand("The next deep dive", 22, O.GOLD_INK, "8px 0 0 0")
                  + O.h2("Village Hall", "2px 0 0 0", 40, 44)
                  + p("One topic. One guest expert. Your questions.", 19, 25, INK, 500, margin="6px 0 0 0",
                      extra=f"font-family:{O.DISPLAY};")),
           O.fullrow(O.img(art("vh-land.jpg"), 600, vh["art_alt"], style="max-width:none;")),
           padrow(O.fact_pills(vh["date"], [vh["time"], "Online"])),
           sp(12),
           padrow(O.board(art, O.poster(art, "Topic and guests" if len(guests) > 1 else "Topic and guest",
                                        vh["topic"], guests_html, vh["about"]))),
           sp(18),
           padrow(O.ticket(art, button(f"{SITE}/village-hall", vh.get("button", "Register for Village Hall"), GOLD, INK,
                                       align="center"), price_boxes()))]
    return "\n".join(out)


def month_ahead(issue, art):
    ev = issue["events"]
    f = ev["featured"]
    link = f.get("link")
    art_html = pic(f.get("photo_url") or art(f.get("photo", "featured.jpg")), f["art_alt"], style="border-radius:12px;margin:0 auto;")
    if link:
        art_html = f'<a href="{link[0]}" style="display:block;text-decoration:none;">{art_html}</a>'
    copy = (O.hand("Featured", 21, O.GOLD_INK, "12px 0 0 0")
            + p(f["title"], 19, 25, INK, 700, margin="4px 0 0 0")
            + p(f["meta"], 16, 24, BODY, 400, margin="6px 0 0 0")
            + (p(f["blurb"], 15, 22, BODY, 400, margin="6px 0 0 0") if f.get("blurb") else "")
            + (btn_row([link], "6px 0 0 0", kind="gold") if link else ""))
    out = [section_head("events", "The month ahead", ev.get(
        "intro", "Picked for sensory-sensitive kids and their families. Drive times are from Murfreesboro."), eyebrow="Happening soon"),
           sp(14), padrow(card(art_html + copy, pad="12px 12px 18px 12px"))]
    if ev["list"]:
        # Events on the same day share one date chip (lighter email, easier to scan).
        groups = []
        for e in ev["list"]:
            if groups and groups[-1][0] == e["chip"]:
                groups[-1][1].append(e)
            else:
                groups.append((e["chip"], [e]))
        rows = []
        for i, (ch, evs) in enumerate(groups):
            content = ""
            for k, e in enumerate(evs):
                block = item(e["title"], [e["meta"]] + disclose(e.get("disclose") or []))
                if e.get("link") or e.get("links"):
                    block += btn_row(e.get("links") or [e["link"]])
                content += block if k == 0 else f'<div style="margin-top:14px;">{block}</div>'
            rows.append(row(chip(*ch), content, last=(i == len(groups) - 1), tight=True))
        out += [sp(20), padrow(O.calendar_page(art, rows_table(rows)))]
    if ev.get("note"):
        out += [sp(12), padrow(p(ev["note"], 14, 21, MUTED, 400, extra="text-align:center;"))]
    out += [sp(20), padrow(button(f"{SITE}/events", ev["calendar_label"], INK, CREAM, align="center"))]
    return "\n".join(out)


def wall_of_hope(issue, art):
    """A parent's words pinned to the Wall of Hope board, with the painting as the print on the note."""
    h = issue["hope"]
    inner = (O.hand("From the Wall of Hope")
             + f'<div style="margin:10px 0 12px 0;">{pic(art("wall-of-hope.jpg"), h["art_alt"], style="border-radius:8px;margin:0 auto;")}</div>'
             + p(h["quote"], 18, 27, INK, 700)
             + O.hand(h["who"], 23, O.GOLD_INK, "12px 0 0 0")
             + btn_row([(f"{SITE}/hope", "Read more stories"), (f"{SITE}/hope", "Share yours")], "12px 0 0 0"))
    fold = (f'<tr><td align="right" style="padding:6px 0 0 0;font-size:0;line-height:0;">'
            f'{O.img(art(O.DECOR + "fold.png"), 34, "", 34, fluid=False, style="display:inline-block;border-radius:0 0 6px 0;")}</td></tr>')
    note = O.paper(inner, "4px 24px 0 24px", O.NOTE, "6px", "os-tl", top=O.pins_row(art, center=True), bottom=fold)
    return (section_head("hope", "A little hope", "Real words from local parents, shared with permission.", eyebrow="One hopeful story")
            + sp(8) + padrow(O.img(art(O.DECOR + "garland.png"), 532, "")) + padrow(O.board(art, note)))


def library(issue, art):
    books = []
    for i, g in enumerate(issue["guides"], start=1):
        books.append(O.book(
            art, g["label"],
            O.img(art(f"guide-{i}.jpg"), 490, g["art_alt"], 228, style="border-radius:10px;margin:0 0 12px 0;", cls="os-card-art"),
            p(g["title"], 18, 24, INK, 700) + p(g["blurb"], 15, 22, BODY, 400, margin="8px 0 0 0")
            + f'<div class="os-card-cta">{btn_row([(SITE + g["path"], g.get("cta", "Read the guide"))])}</div>', i - 1))
    return (section_head("library", issue.get("library_title", "From the library"), eyebrow="Resource Library") + sp(14)
            + padrow(O.browser_cols(*books, gap=18)))


def question(issue, art):
    q = issue["question"]
    steps = rows_table([step(i + 1, f'{b(t)} {body.replace("{STEP}", tel("800-280-7837", "+18002807837"))}',
                             last=(i == len(q["steps"]) - 1))
                        for i, (t, body) in enumerate(q["steps"])])
    q_head = (f'<table {O.T} width="100%" style="width:100%;"><tr><td valign="top">'
              + O.hand(f"{issue['month']}&rsquo;s question") + '</td>' + O.question_mark() + '</tr></table>'
              + p(f"&ldquo;{q['q']}&rdquo;", 20, 27, INK, 700, margin="4px 0 0 0")
              + p(q["short"], 16, 24, BODY, 400, margin="8px 0 0 0"))
    q_foot = (btn_row(q["links"] + [(f"{SITE}/contact", "Send us your question")], margin="0")
              + p(q.get("disclaimer", "Parent-to-parent guidance, not medical or legal advice."), 13, 20, MUTED, 400,
                  margin="10px 0 0 0", cls="os-tiny"))
    return (section_head("question", "One question, answered",
                         "One real question from a local parent, answered plainly.", eyebrow="Parent to parent")
            + sp(14) + padrow(O.index_card(art, q_head, steps, q_foot)))


def connect(issue, art):
    online = group_card(
        [], "Our Special Village Online Parent Group",
        [("calendar", "Thursdays"), ("clock", "7:00&ndash;8:00 PM Central"), ("video", "Online")],
        "Connect with parents and caregivers of neurodivergent and disabled children "
        "in a welcoming, judgment-free space.",
        ["No formal diagnosis required", issue.get("group_line", "Drop in any Thursday"),
         "Cameras are optional", "Meetings are never recorded"],
        f"{SITE}/group", "Join the Online Group", secondary=["ONLINE", "WEEKLY", "FREE"], art=art, tilt="os-tl")
    werock = group_card(
        [], "We Rock the Spectrum Parent Group",
        [("calendar", "Wednesdays at 5:00 PM"), ("pin", "We Rock the Spectrum Murfreesboro")],
        "Connect with other parents of kids with special needs while children enjoy the gym. "
        "Gym staff watch the kids during group; childcare is available but not appropriate for all children.",
        ["Led by Cari Parr", "$15 per child for kids to play",
         "Gym staff watch children during group; not appropriate for all children",
         "Discounted gym admission is available separately."],
        O.WRTS_URL, "Plan Your Visit", secondary=["IN PERSON", "WEEKLY", "FREE"], art=art, tilt="os-tr")
    return O.dusk_band(art, "ongoing", "The heart of the village", "Connect with other local parents",
                       '<div class="os-browser-cols os-equal-pair" style="display:block;width:100%;">'
                       f'<div class="os-browser-col" style="display:block;width:100%;margin:0 0 20px 0;box-sizing:border-box;">{online}</div>'
                       f'<div class="os-browser-col" style="display:block;width:100%;margin:0;box-sizing:border-box;">{werock}</div>'
                       '</div>')


def build_html(issue, base, browser, deadlines_url, view_url):
    """Mirror of O.build_html with this issue's content: the same site-style pieces in the same
    order (events, deadlines, Village Hall, library, Wall of Hope, question, groups, Taylor's note)."""
    art = lambda f: f"{base}{f}"
    T = O.T
    o = [head(issue)]
    o.append(f'<body id="os-body" class="os-bg" bgcolor="{CREAM}" style="margin:0;padding:0;background-color:{CREAM};width:100%;overflow-x:hidden;">')
    o.append(f'<span style="display:none;font-size:1px;color:{CREAM};line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{plain(issue["preheader"])}</span>')
    o.append(f'<table {T} class="os-bg" width="100%" bgcolor="{CREAM}" style="width:100%;background-color:{CREAM};">'
             f'<tr><td align="center" style="padding:14px 10px 40px 10px;font-family:{FONT};color:{BODY};">'
             f'<table {T} class="os-wrap" width="600" style="width:100%;max-width:600px;">')
    view_href = view_url if browser else "{$url}"
    unsub_href = O.BROWSER_UNSUB_URL if browser else "{$unsubscribe}"

    # --- Opening: top bar, header, the village in its landscape, Taylor's small letter beside the jump
    # buttons (Taylor, Oct 3), then events, deadlines, Village Hall and the rest ---
    o.append(f'<tr><td style="padding:0 0 12px 0;">{O.top_bar(issue["month_year"], view_href)}</td></tr>')
    o.append(padrow(O.site_header(art, SITE), pad="0 16px 14px 16px"))
    o.append(O.hero(art, f'{issue["month"]} in Our <span class="os-hl">Special Village</span>',
                    "fall" if issue["id"] == "2026-11" else "winter", land_alt=issue["hero_alt"]))
    o.append(sp(26))
    o.append(padrow(O.opening_block(art, O.note_paras(issue["note"], issue.get("note_highlight")), O.JUMPS)))

    o.append(major_sp())
    o.append(month_ahead(issue, art))

    # --- Three things: the deadline tag ---
    o.append(major_sp())
    o.append(section_head("deadlines", "Three things to know this month", eyebrow="Deadline watch"))
    o.append(sp(14))
    o.append(padrow(O.tag_card(art, three_things(issue))))
    o.append(sp(16))
    o.append(padrow(button(deadlines_url, "See all deadlines", INK, CREAM)
                    + p(issue["confirmed"], 13, 20, MUTED, 400, margin="8px 0 0 0", cls="os-confirm")))

    o.append(major_sp())
    o.append(village_hall(issue, art))
    o.append(major_sp())
    o.append(library(issue, art))
    o.append(major_sp())
    o.append(wall_of_hope(issue, art))
    o.append(major_sp())
    o.append(question(issue, art))
    o.append(sp(34))
    o.append(connect(issue, art))

    # --- About, numbers, forward, footer: identical to October ---
    o.append(major_sp())
    o.append(padrow(O.about_card(art, O.ABOUT, [(f"{SITE}/about", "About the Village"),
                                                (f"{SITE}/editorial-policy", "How we check information")])))
    o.append(sp(20))
    o.append(padrow(O.numbers_card(art, O.NUMBERS)))
    o.append(sp(22))
    o.append(padrow(O.forward_line(SITE)))
    o.append(sp(30))
    o.append(O.footer_rows(art, SITE, unsub_href, O.OWNER_LINE))
    o.append('</table></td></tr></table></body></html>')
    return render_ph(O.compact("\n".join(o) + "\n"))


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
    w("In this issue: " + " · ".join(lab for _, lab in O.JUMPS))
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
        for href, label in e.get("links") or ([e["link"]] if e.get("link") else []):
            w(f"  {plain(label)}: {href}")
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
    w(O.OWNER_LINE)
    w(O.OWNER_ADDRESS)
    return O.reorder_text("\n".join(L) + "\n")


# --------------------------------------------------------------------------- deadlines page


def build_deadlines(issue, back_url, back_label):
    sections = []
    for title, items in issue["all_deadlines"]:
        rows = "".join(O.deadline_item(dow, day, moy, t, body) for dow, day, moy, t, body in items)
        sections.append(f"<h2>{title}</h2>\n{rows}")
    page = O.build_deadlines_page()
    head_part = page.split("<main>", 1)[0]
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
    assert f'{issue["month"]} in Our <span class="os-hl">Special Village</span>' in email
    assert 'href="tel:988"' in email
    for s in (email, browser, txt):  # Taylor's ownership line, word for word, at the very bottom
        assert O.OWNER_LINE in s and O.OWNER_ADDRESS in s and "PLLC" not in s, f"{issue['id']}: ownership line"
    assert txt.rstrip().endswith(O.OWNER_LINE + "\n" + O.OWNER_ADDRESS), f"{issue['id']}: ownership line not last"
    order = ["id=\"note\"", "id=\"events\"", "id=\"deadlines\"", "id=\"village-hall\"", "id=\"library\"",
             "id=\"hope\"", "id=\"question\"", "id=\"ongoing\""]
    idx = [email.find(x) for x in order]
    assert all(i > 0 for i in idx) and idx == sorted(idx), f"{issue['id']}: section order {idx}"
    for href, _ in O.JUMPS:
        assert f'id="{href[1:]}"' in email, href
    assert len(issue["three_things"]) >= 1
    assert 2 <= len(issue["guides"]) <= 3
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
        # The site's pins, tape, cork, bunting... (tools/render-decor.mjs) ride along with each issue's art.
        shutil.copytree(os.path.join(ROOT, "art", "decor"), os.path.join(folder, "art", "decor"), dirs_exist_ok=True)
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
            live_size = len(s_email.replace("{$site}", SITE).encode())
            assert live_size < 100_000, f"{iid}: {live_size}B with full image URLs would clip in Gmail"
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
