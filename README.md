# OSV October 2026 newsletter preview (temporary)

Customer preview for Taylor Hickok. Not production MailerLite send.

- Preview (GitHub Pages): https://tmacocx.github.io/osv-newsletter-october-preview/
- Full deadlines companion: https://tmacocx.github.io/osv-newsletter-october-preview/deadlines-october-2026.html
- `index.html` is the **browser/desktop preview** (wider layout, real view/unsubscribe links).
- `newsletter-october-subscriber-preview.html` is the **MailerLite/email** HTML (600px + `{$url}` / `{$unsubscribe}`).
- `newsletter-october-2026.txt` is the plain-text alternative for the MailerLite send.
- `tools/build-october-2026.py` generates both HTML files, the `.txt`, and `deadlines-october-2026.html`. Edit that, then re-run it.
- `research-notes-october-2026.md` - sources and checklist mapping.

## T299 content/structure shorten (second-round Hickok)

Material shorten (keep Vincent/T323 art): short welcome, no TOC, “Three things to know this month” + See all deadlines, month-ahead heading before featured Discovery card, no autumn collage, ≤4 secondary events + full calendar button, landscape guide thumbs, no Wall of Hope, 3-step IEP + Village Hall navy CTA (no standalone VH section), Ongoing this month, condensed About. Target 750–1000 words.

## MailerLite settings

- **Subject:** `October: sensory-friendly events + deadlines` (44 chars)
- **Preheader:** Fall break / three things / Discovery / guides / IEP (see build script)
- **Email:** View in browser → `{$url}`, Unsubscribe → `{$unsubscribe}`.
- **Browser preview (`index.html`):** real destinations (Pages URL + `/newsletter`).
- Attach `newsletter-october-2026.txt` as the plain-text part.

## November 2026 to February 2027 issues

Same template as October, one folder per month in `issues/` (`issues/index.html` is a month picker).

- `python3 tools/prepare-issue-art.py --site ../OurSpecialVillage --headshot <amanda.png>` crops Taylor's fall/winter paintings.
- `python3 tools/build-issues.py` builds `index.html`, `email.html`, `email.txt` and `deadlines.html` per issue.
  Add `--site-export ../OurSpecialVillage` to write `newsletters/<id>/` and `public/assets/newsletters/<id>/` for the site's sender.
- Content lives in `tools/issue_data.py`. Yellow dashed boxes are placeholders; `--strict` fails until they are filled.
- Sources: `research-notes-nov-2026-feb-2027.md`.
