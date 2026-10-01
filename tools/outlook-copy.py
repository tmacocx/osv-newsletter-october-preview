#!/usr/bin/env python3
"""October 2026 as a send-it-yourself copy for Outlook (Taylor's first run, Oct 2026).

Same email as newsletter-october-subscriber-preview.html, minus the MailerLite parts:
pictures load from this public repo at one fixed commit, so they never change after
sending; no "View in browser" button (no merge tag to fill it); Unsubscribe is an email
to hello@ourspecialvillagetn.com; the hidden inbox preview line is dropped because a
paste into Outlook can show it at the top.

    python3 tools/outlook-copy.py --sha <commit that has art/> --out october-2026-outlook.html
"""
import argparse
import os
import re
import subprocess
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = "https://raw.githubusercontent.com/tmacocx/osv-newsletter-october-preview/{sha}/"
UNSUB = "mailto:hello@ourspecialvillagetn.com?subject=Unsubscribe"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sha", required=True, help="commit whose art/ the pictures load from")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["python3", os.path.join(ROOT, "tools", "build-october-2026.py"),
                        "--base", RAW.format(sha=args.sha), "--out", tmp], check=True, capture_output=True)
        s = open(os.path.join(tmp, "newsletter-october-subscriber-preview.html"), encoding="utf-8").read()
    s, n = re.subn(r'&nbsp;&nbsp; <a [^>]*href="\{\$url\}"[^>]*>View in browser</a>', "", s)
    assert n == 1, "view in browser button"
    s, n = re.subn(r'(<a [^>]*href=")\{\$unsubscribe\}("[^>]*>)Unsubscribe in one click</a>', rf"\g<1>{UNSUB}\g<2>Unsubscribe</a>", s)
    assert n == 1, "unsubscribe button"
    s, n = re.subn(r'(<body[^>]*>\n?)<span style="display:none;[^>]*>.*?</span>', r"\1", s, count=1, flags=re.S)
    assert n == 1, "preheader"
    s = re.sub(r"<!-- MailerLite:[^>]*-->\n?", "", s)
    assert "{$" not in s, "merge tag left"
    assert not re.search(r'(src=|background=|url\()"?art/', s), "relative picture left"
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"wrote {args.out}: {len(s.encode())}B")


if __name__ == "__main__":
    main()
