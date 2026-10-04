#!/usr/bin/env python3
"""October 2026 as a short note Taylor can paste into Outlook (Oct 1, 2026).

Outlook drops fonts, textures and rounded shapes when a designed email is pasted in,
so the look lives in pictures Outlook keeps: an envelope masthead (Issue No. 1), the
October painting, a dusk band with a peek at the full newsletter, and the site's tape.
Around them are only plain tables, solid colours and fixed widths, which a paste keeps.
Taylor, Oct 1: say it's our first edition and a test run (it will look even better once
we move to a newsletter service), ask for feedback, and push people to tap through to the
full newsletter. The buttons open the full newsletter on the website.
Pictures load from this public repo at one fixed commit.

    python3 tools/outlook-note.py --sha <commit that has art/outlook/> --out october-2026-note.html
"""
import argparse

RAW = "https://raw.githubusercontent.com/tmacocx/osv-newsletter-october-preview/{sha}/art/"
SITE = "https://ourspecialvillagetn.com"
FULL = f"{SITE}/newsletter/october-2026"
UNSUB = "mailto:hello@ourspecialvillagetn.com?subject=Unsubscribe"

CREAM, PAPER, NOTE, INK, NIGHT, BODY = "#f7f1e2", "#fffdf7", "#fbf0d2", "#1d2c4c", "#14203a", "#3a4760"
GOLD, GOLD_DARK, SAND, MUTED = "#d7a43e", "#7a5b13", "#e9dcbd", "#5d6577"
SANS = "'Segoe UI',Arial,Helvetica,sans-serif"
W = 600


def para(text, size=17, color=BODY, margin="0 0 16px 0", weight="normal", align="left"):
    return (f'<p style="margin:{margin};font-family:{SANS};font-size:{size}px;line-height:{round(size * 1.55)}px;'
            f'color:{color};font-weight:{weight};text-align:{align};">{text}</p>')


def pic(src, w, h, alt="", href=None, style=""):
    tag = (f'<img src="{src}" width="{w}" height="{h}" alt="{alt}" '
           f'style="display:block;width:{w}px;height:{h}px;border:0;{style}">')
    return f'<a href="{href}" style="text-decoration:none;">{tag}</a>' if href else tag


def button(href, label, bg=GOLD, fg=INK, size=19, pad="16px 34px"):
    # A coloured table cell, so the button keeps its colour when pasted into Outlook.
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:0 auto;">'
            f'<tr><td align="center" bgcolor="{bg}" style="background-color:{bg};border-radius:999px;padding:{pad};">'
            f'<a href="{href}" style="font-family:{SANS};font-size:{size}px;line-height:{size + 4}px;font-weight:bold;'
            f'color:{fg};text-decoration:none;display:inline-block;">{label}</a></td></tr></table>')


def build(sha, full=FULL):
    art = RAW.format(sha=sha)
    inside = [
        "The dates to know before fall break",
        "A free Village Hall on Saturday, October 10, with Mercedes Lawson on IEPs and the school system",
        "Sensory-friendly events all month, including the Sensory Spooktacular on Sunday, October 25",
        "Two new guides and one parent question, answered",
    ]
    rows = "".join(
        f'<tr><td width="40" valign="top" style="width:40px;padding:0 12px 14px 0;">'
        f'<img src="{art}outlook/num-{i}.png" width="28" height="28" alt="{i}." style="display:block;width:28px;height:28px;border:0;"></td>'
        f'<td valign="top" style="padding:2px 0 14px 0;font-family:{SANS};font-size:17px;line-height:25px;color:{BODY};">{t}</td></tr>'
        for i, t in enumerate(inside, 1))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>October in Our Special Village</title>
</head>
<body style="margin:0;padding:0;background-color:{CREAM};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{CREAM}" style="background-color:{CREAM};">
<tr><td align="center" style="padding:20px 0 28px 0;">
<table role="presentation" width="{W}" cellpadding="0" cellspacing="0" border="0" bgcolor="{CREAM}" style="width:{W}px;background-color:{CREAM};">

<tr><td style="padding:0 0 10px 0;">{pic(f"{art}outlook/masthead.png", W, 125, "Our Special Village. Issue No. 1, October 2026.", full)}</td></tr>
<tr><td style="padding:0;">{pic(f"{art}outlook/october-hero-card.jpg", W, 510, "October in Our Special Village: it takes a village, welcome to ours. A painted autumn street of brick houses and neighbors.", full)}</td></tr>

<tr><td bgcolor="{PAPER}" style="background-color:{PAPER};padding:30px 36px 30px 36px;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 18px 0;"><tr>
  <td bgcolor="{SAND}" style="background-color:{SAND};border-radius:999px;padding:5px 14px;font-family:{SANS};font-size:12px;line-height:16px;font-weight:bold;letter-spacing:1.5px;color:{GOLD_DARK};">A NOTE FROM TAYLOR</td>
  </tr></table>
  {para("Hi friends,", 19, INK, weight="bold")}
  {para("Welcome to the very first edition of the Our Special Village newsletter! I&rsquo;m so glad you&rsquo;re here.")}
  {para("Think of this one as our first draft. I&rsquo;m sending it from my own inbox while we get set up with a proper newsletter service, so future issues will arrive looking even better. For now, the full newsletter lives on our website, with all the pictures, dates and details in one place.")}
  {para("Here&rsquo;s what&rsquo;s waiting for you inside:", margin="0 0 14px 0")}
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 12px 0;">{rows}</table>
  {button(full, "Read the full newsletter")}
  {para("With love,", margin="28px 0 4px 0")}
  <img src="{art}signature-taylor.png" width="106" height="61" alt="Taylor" style="display:block;width:106px;height:61px;border:0;margin:0 0 4px 0;">
  {para("Dr. Taylor Hickok &middot; Our Special Village", 15, MUTED, "0")}
</td></tr>

<tr><td bgcolor="{NIGHT}" style="background-color:{NIGHT};padding:0;">
  {pic(f"{art}outlook/dusk-top.jpg", W, 171)}
</td></tr>
<tr><td bgcolor="{NIGHT}" align="center" style="background-color:{NIGHT};padding:6px 36px 0 36px;">
  {para("The full newsletter is one tap away", 26, "#fffcf5", "0 0 8px 0", "bold", "center")}
  {para("Tap below to see every date, event and guide, with all the pictures.", 17, SAND, "0", align="center")}
</td></tr>
<tr><td bgcolor="{NIGHT}" style="background-color:{NIGHT};padding:0;">
  {pic(f"{art}outlook/peek-inside.jpg", W, 330, "A peek inside: the fall break dates, Village Hall on Saturday, October 10 (free), and the month's events.", full)}
</td></tr>
<tr><td bgcolor="{NIGHT}" align="center" style="background-color:{NIGHT};padding:4px 36px 34px 36px;border-bottom:5px solid {GOLD};">
  {button(full, "Open the October newsletter", size=20, pad="18px 38px")}
  {para("It opens on our website, ourspecialvillagetn.com.", 14, SAND, "14px 0 0 0", align="center")}
</td></tr>

<tr><td align="center" style="padding:34px 40px 0 40px;">
  <img src="{art}decor/tape-cream.png" width="124" height="44" alt="" style="display:block;width:124px;height:44px;border:0;margin:0 auto -22px auto;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td bgcolor="{NOTE}" style="background-color:{NOTE};padding:30px 30px 24px 30px;border:1px solid #ecdcb2;">
    {para("P.S. Tell me what you think", 19, INK, "0 0 8px 0", "bold")}
    {para("Since this is our first try, your feedback means a lot. Just hit reply and tell me what helped and what you&rsquo;d like to see next time.", 16, BODY, "0")}
  </td></tr></table>
</td></tr>

<tr><td align="center" style="padding:30px 10px 6px 10px;">
  {para("Know a family who could use this? Forward it along. Anyone can join at", 15, BODY, "0 0 12px 0", align="center")}
  {button(f"{SITE}/newsletter", "ourspecialvillagetn.com/newsletter", INK, "#ffffff", 15, "11px 22px")}
</td></tr>
<tr><td align="center" style="padding:22px 10px 0 10px;">
  {para("You&rsquo;re getting this because you joined the newsletter at ourspecialvillagetn.com.", 13, MUTED, "0 0 10px 0", align="center")}
  {button(UNSUB, "Unsubscribe", SAND, INK, 13, "7px 18px")}
  {para("Our Special Village is owned and operated by Little Luminaries Therapy Services, PLLC<br>1810 Ward Dr, Suite 101, Murfreesboro, TN 37129", 12, MUTED, "14px 0 0 0", align="center")}
</td></tr>

</table>
</td></tr>
</table>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sha", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--full", default=FULL, help="where the buttons go (the full newsletter online)")
    args = ap.parse_args()
    html = build(args.sha, args.full)
    assert "—" not in html and "&mdash;" not in html
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {args.out}: {len(html.encode())}B")


if __name__ == "__main__":
    main()
