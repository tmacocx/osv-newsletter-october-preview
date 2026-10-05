#!/usr/bin/env python3
"""The October note as an email file with its pictures built in (Oct 1, 2026).

Outlook hides pictures that load from the internet until the reader clicks "Download
pictures", so the pasted note showed up bare. This packs the same note (tools/outlook-note.py)
into an .eml with every picture attached inside the message, which Outlook shows right away.
"X-Unsent: 1" makes the Outlook app open it as a new draft: add people in BCC and send.

    python3 tools/outlook-eml.py --out october-2026-note.eml
"""
import argparse
import importlib.util
import os
import re
from email.message import EmailMessage
from email.policy import SMTP

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SUBJECT = "Our very first newsletter is here!"

spec = importlib.util.spec_from_file_location("outlook_note", os.path.join(ROOT, "tools", "outlook-note.py"))
note = importlib.util.module_from_spec(spec)
spec.loader.exec_module(note)

TEXT = """Hi friends,

Welcome to the very first edition of the Our Special Village newsletter! I'm so glad you're here.

Think of this one as our first draft. I'm sending it from my own inbox while we get set up with a proper newsletter service, so future issues will arrive looking even better. For now, the full newsletter lives on our website, with all the pictures, dates and details in one place.

Read the full newsletter: {full}

Here's what's waiting for you inside:
1. The dates to know before fall break
2. A free Village Hall on Saturday, October 10, with Mercedes Lawson on IEPs and the school system
3. Sensory-friendly events all month, including the Sensory Spooktacular on Sunday, October 25
4. Two new guides and one parent question, answered

With love,
Taylor
Dr. Taylor Hickok, Our Special Village

P.S. Since this is our first try, your feedback means a lot. Just hit reply and tell me what helped and what you'd like to see next time.

Know a family who could use this? Forward it along. Anyone can join at https://ourspecialvillagetn.com/newsletter

You're getting this because you joined the newsletter at ourspecialvillagetn.com. To unsubscribe, reply with "Unsubscribe".
Our Special Village is owned and operated by Little Luminaries Therapy Services, PLLC
1810 Ward Dr, Suite 101, Murfreesboro, TN 37129
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--full", default=note.FULL, help="where the buttons go (the full newsletter online)")
    args = ap.parse_args()
    marker = "@@ART@@/"
    html = note.build("SHA", args.full).replace(note.RAW.format(sha="SHA"), marker)
    pics = sorted(set(re.findall(re.escape(marker) + r'([^"]+)', html)))
    cids = {}
    for rel in pics:
        cid = re.sub(r"[^a-z0-9]+", "-", rel.lower()).strip("-") + "@ourspecialvillagetn.com"
        cids[rel] = cid
        html = html.replace(marker + rel, f"cid:{cid}")
    assert marker not in html and "raw.githubusercontent" not in html

    msg = EmailMessage(policy=SMTP)
    msg["Subject"] = SUBJECT
    msg["X-Unsent"] = "1"
    msg.set_content(TEXT.format(full=args.full))
    msg.add_alternative(html, subtype="html")
    html_part = msg.get_payload()[1]
    for rel, cid in cids.items():
        path = os.path.join(ROOT, "art", rel)
        ext = os.path.splitext(rel)[1].lower()
        sub = {".png": "png", ".jpg": "jpeg", ".jpeg": "jpeg"}[ext]
        with open(path, "rb") as f:
            html_part.add_related(f.read(), "image", sub, cid=f"<{cid}>", filename=os.path.basename(rel),
                                  disposition="inline")
    data = bytes(msg)
    with open(args.out, "wb") as f:
        f.write(data)
    print(f"wrote {args.out}: {len(data)}B, {len(cids)} pictures inside")


if __name__ == "__main__":
    main()
