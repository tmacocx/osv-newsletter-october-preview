#!/usr/bin/env python3
"""October 2026 as a short note Taylor can paste into Outlook (Oct 1, 2026).

Outlook drops fonts, textures and rounded shapes when a designed email is pasted in,
so this sends a simple note instead: the October picture, a few lines (Taylor, Oct 1: say it's
her first newsletter and a test run, ask for feedback, a newsletter service is coming), and one big
button to the full newsletter online. Only plain tables, colours and pictures, which
Outlook keeps. Pictures load from this public repo at one fixed commit.

    python3 tools/outlook-note.py --sha <commit that has art/outlook/> --out october-2026-note.html
"""
import argparse

RAW = "https://raw.githubusercontent.com/tmacocx/osv-newsletter-october-preview/{sha}/art/"
FULL = "https://tmacocx.github.io/osv-newsletter-october-preview/"
SITE = "https://ourspecialvillagetn.com"
UNSUB = "mailto:hello@ourspecialvillagetn.com?subject=Unsubscribe"

CREAM, PAPER, INK, BODY, GOLD, GOLD_DARK, MUTED = "#f7f1e2", "#fffdf7", "#1d2c4c", "#3a4760", "#d7a43e", "#7a5b13", "#5d6577"
SANS = "Mulish,'Segoe UI',Arial,Helvetica,sans-serif"
HEAD = "Outfit,'Segoe UI',Arial,Helvetica,sans-serif"


def para(text, size=17, color=BODY, margin="0 0 16px 0", weight="normal"):
    return (f'<p style="margin:{margin};font-family:{SANS};font-size:{size}px;line-height:{round(size * 1.55)}px;'
            f'color:{color};font-weight:{weight};">{text}</p>')


def button(href, label, bg=GOLD, fg=INK, size=18, pad="15px 30px"):
    # A coloured table cell, so the button keeps its colour when pasted into Outlook.
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:0 auto;">'
            f'<tr><td align="center" bgcolor="{bg}" style="background-color:{bg};border-radius:999px;padding:{pad};">'
            f'<a href="{href}" style="font-family:{HEAD};font-size:{size}px;line-height:{size + 4}px;font-weight:bold;'
            f'color:{fg};text-decoration:none;display:inline-block;">{label}</a></td></tr></table>')


def build(sha):
    art = RAW.format(sha=sha)
    inside = [
        "The dates to know before fall break",
        "A free Village Hall on Saturday, October 10, with Mercedes Lawson on IEPs and the school system",
        "Sensory-friendly events all month, including the Sensory Spooktacular on Sunday, October 25",
        "Two new guides and one parent question, answered",
    ]
    rows = "".join(
        f'<tr><td valign="top" style="padding:0 10px 10px 0;font-family:{SANS};font-size:17px;line-height:26px;color:{GOLD};">&#9679;</td>'
        f'<td valign="top" style="padding:0 0 10px 0;font-family:{SANS};font-size:17px;line-height:26px;color:{BODY};">{t}</td></tr>'
        for t in inside)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>October in Our Special Village</title>
</head>
<body style="margin:0;padding:0;background-color:{CREAM};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{CREAM}" style="background-color:{CREAM};">
<tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;">
<tr><td align="center" style="padding:0 0 14px 0;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
  <td style="padding:0 10px 0 0;"><img src="{art}osv-mark-80.png" width="40" height="40" alt="" style="display:block;border:0;"></td>
  <td style="font-family:{HEAD};font-size:20px;line-height:24px;font-weight:bold;color:{INK};">Our Special Village</td>
  </tr></table>
</td></tr>
<tr><td style="padding:0;">
  <a href="{FULL}" style="text-decoration:none;"><img src="{art}outlook/october-hero-card.jpg" width="600" alt="October in Our Special Village: it takes a village, welcome to ours. A painted autumn street of brick houses and neighbors."
   style="display:block;width:100%;max-width:600px;height:auto;border:0;"></a>
</td></tr>
<tr><td bgcolor="{PAPER}" style="background-color:{PAPER};padding:30px 30px 26px 30px;border-bottom:4px solid {GOLD};">
  {para("Hi friends,")}
  {para("This is my very first Our Special Village newsletter, and it&rsquo;s a bit of a test run! I&rsquo;m sending it from my own email for now, and we&rsquo;ll be moving to a real newsletter service soon.")}
  {para("I&rsquo;d love your feedback, so just hit reply and tell me what helped and what you&rsquo;d like to see next time.")}
  {para("I put everything on one page so it&rsquo;s easy to read on your phone. Here&rsquo;s what&rsquo;s inside this month:")}
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 22px 0;">{rows}</table>
  {button(FULL, "Read the October newsletter")}
  {para("With love,", margin="26px 0 4px 0")}
  <img src="{art}signature-taylor.png" width="106" height="61" alt="Taylor" style="display:block;border:0;margin:0 0 4px 0;">
  {para("Dr. Taylor Hickok &middot; Our Special Village", 15, MUTED, "0")}
</td></tr>
<tr><td align="center" style="padding:24px 10px 6px 10px;">
  {para("Know a family who could use this? Forward it along. Anyone can join at", 15, BODY, "0 0 12px 0")}
  {button(f"{SITE}/newsletter", "ourspecialvillagetn.com/newsletter", INK, "#ffffff", 15, "11px 22px")}
</td></tr>
<tr><td align="center" style="padding:22px 10px 0 10px;">
  {para("You&rsquo;re getting this because you joined the newsletter at ourspecialvillagetn.com.", 13, MUTED, "0 0 10px 0")}
  {button(UNSUB, "Unsubscribe", "#e8dcc2", INK, 13, "7px 18px")}
  {para("Our Special Village is owned and operated by Little Luminaries Therapy Services, PLLC<br>1810 Ward Dr, Suite 101, Murfreesboro, TN 37129", 12, MUTED, "14px 0 0 0")}
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
    args = ap.parse_args()
    html = build(args.sha)
    assert "—" not in html and "&mdash;" not in html
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {args.out}: {len(html.encode())}B")


if __name__ == "__main__":
    main()
