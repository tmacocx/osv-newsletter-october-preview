# OSV October 2026 newsletter preview (temporary)

Customer preview for Taylor Hickok. Not production MailerLite send.

- Preview (GitHub Pages): https://tmacocx.github.io/osv-newsletter-october-preview/
- `index.html` and `newsletter-october-subscriber-preview.html` are identical copies of the email.
- `newsletter-october-2026.txt` is the plain-text alternative for the MailerLite send.
- `tools/build-october-2026.py` generates both HTML files and the `.txt`. Edit that, then re-run it.
- `research-notes-october-2026.md` - sources, T299 and T303 checklist mapping, and editor to-dos before send.

## MailerLite settings (T303)

- **Subject:** `October: sensory-friendly events + deadlines` (44 chars; the hero stays "October in the Village")
- **Preheader:** `Two deadlines land Monday, October 5. Plus sensory-friendly fall outings with drive times, two new guides, and one IEP question answered.`
- Two links use MailerLite link variables and only resolve inside MailerLite: **View in browser** → `{$url}`, **Unsubscribe in one click** → `{$unsubscribe}`. They 404 on the GitHub Pages preview by design. Confirm `{$url}` in a test send.
- Attach `newsletter-october-2026.txt` as the plain-text part.
- "In this issue" uses in-email anchors (`#deadlines`, `#events`, `#library`, `#hope`, `#question`, `#village-hall`). They work in Apple Mail, Outlook, Yahoo, and Gmail on the web; the Gmail mobile apps ignore them.

New art (`art/signature-taylor.png`, `art/about-family-bowling.jpg`) 404s on Pages until this branch is merged to `main`.
