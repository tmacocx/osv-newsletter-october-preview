# OSV October 2026 newsletter preview (temporary)

Customer preview for Taylor Hickok. Not production MailerLite send.

- Preview (GitHub Pages): https://tmacocx.github.io/osv-newsletter-october-preview/
- `index.html` and `newsletter-october-subscriber-preview.html` are identical copies of the email.
- `research-notes-october-2026.md` — sources for every event and deadline in the issue, what was removed and why, the T299 checklist mapping, and editor to-dos before send.

## MailerLite settings (T299)

- **Subject:** `October: sensory-friendly events + deadlines` (44 chars; the hero stays "October in the Village")
- **Preheader:** `Sensory-friendly fall outings with drive times, deadlines sorted by school, insurance, money, and community, two new guides, and one IEP question answered.`
- Two links use MailerLite link variables and only resolve inside MailerLite: **View in browser** → `{$url}`, **Unsubscribe in one click** → `{$unsubscribe}`. They 404 on the GitHub Pages preview by design.
- "In this issue" uses in-email anchors (`#events`, `#deadlines`, `#library`, `#hope`, `#question`, `#village-hall`). They work in Apple Mail, Outlook, Yahoo, and Gmail on the web; the Gmail mobile apps ignore them.
