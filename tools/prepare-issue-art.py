#!/usr/bin/env python3
"""Crop Taylor's village paintings into newsletter-sized JPGs for Nov 2026 - Feb 2027.

Every picture comes from the site's own art (public/images/village and
public/assets/art-pack-2026-09-clean). Nothing is drawn here: transparent
PNGs are flattened onto the newsletter cream and cropped to the sizes the
October issue uses (hero 1200 wide, feature art 600x262, guide art 490x228).

    python3 tools/prepare-issue-art.py --site ../OurSpecialVillage --headshot amanda.png
"""
import argparse
import os
import shutil

from PIL import Image

CREAM = (247, 241, 226)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

VILLAGE = "public/images/village"
PACK = "public/assets/art-pack-2026-09-clean/images"

# (source relative to the site repo, output name, width, height or None, vertical anchor 0..1)
ISSUE_ART = {
    "2026-11": [
        (f"{VILLAGE}/newsletter-fall.png", "hero.jpg", 1200, None, 0.5),
        (f"{VILLAGE}/village-hall-community.png", "village-hall.jpg", 600, 262, 0.55),
        (f"{VILLAGE}/sensory-friendly-fall.png", "featured.jpg", 600, 257, 0.5),
        (f"{PACK}/page-season-sets/wall-of-hope-fall.png", "wall-of-hope.jpg", 600, 262, 0.55),
        (f"{PACK}/category-season-sets/therapy-communication-fall.png", "guide-1.jpg", 490, 228, 0.5),
        (f"{PACK}/category-season-sets/funding-rights-fall.png", "guide-2.jpg", 490, 228, 0.5),
        (f"{PACK}/page-season-sets/resource-library-fall.png", "guide-3.jpg", 490, 228, 0.5),
    ],
    "2026-12": [
        (f"{VILLAGE}/newsletter-winter.png", "hero.jpg", 1200, None, 0.5),
        (f"{PACK}/page-season-sets/public-square-winter.png", "village-hall.jpg", 600, 262, 0.5),
        (f"{VILLAGE}/sensory-friendly-winter.png", "featured.jpg", 600, 257, 0.5),
        (f"{PACK}/page-season-sets/wall-of-hope-winter.png", "wall-of-hope.jpg", 600, 262, 0.55),
        (f"{PACK}/category-season-sets/getting-started-winter.png", "guide-1.jpg", 490, 228, 0.5),
        (f"{PACK}/category-season-sets/adult-life-transition-winter.png", "guide-2.jpg", 490, 228, 0.5),
    ],
    "2027-01": [
        (f"{VILLAGE}/newsletter-winter.png", "hero.jpg", 1200, None, 0.5),
        (f"{PACK}/page-season-sets/public-square-winter.png", "village-hall.jpg", 600, 262, 0.5),
        (f"{VILLAGE}/support-groups-winter.png", "featured.jpg", 600, 257, 0.5),
        (f"{PACK}/page-season-sets/wall-of-hope-winter.png", "wall-of-hope.jpg", 600, 262, 0.55),
        (f"{PACK}/category-season-sets/school-learning-winter.png", "guide-1.jpg", 490, 228, 0.5),
        (f"{PACK}/category-season-sets/funding-rights-winter.png", "guide-2.jpg", 490, 228, 0.5),
    ],
    "2027-02": [
        (f"{VILLAGE}/newsletter-winter.png", "hero.jpg", 1200, None, 0.5),
        (f"{PACK}/page-season-sets/public-square-winter.png", "village-hall.jpg", 600, 262, 0.5),
        (f"{VILLAGE}/about-community-builders-winter.png", "featured.jpg", 600, 257, 0.5),
        (f"{PACK}/page-season-sets/wall-of-hope-winter.png", "wall-of-hope.jpg", 600, 262, 0.55),
        (f"{PACK}/category-season-sets/therapy-communication-winter.png", "guide-1.jpg", 490, 228, 0.5),
        (f"{PACK}/category-season-sets/complex-bodies-winter.png", "guide-2.jpg", 490, 228, 0.5),
    ],
}

# Shared October assets reused as-is in every issue.
SHARED = ["signature-taylor.png", "osv-mark-80.png", "taylor-hickok-160.jpg", "about-family-bowling-small.jpg",
          "icons/calendar.png", "icons/clock.png", "icons/clock-gold.png", "icons/video.png",
          "icons/video-gold.png", "icons/pin.png"]


def flatten(im):
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, CREAM)
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def fit(im, w, h, anchor):
    """Scale to width w; if h is set, cover-crop to w x h anchored vertically."""
    if h is None:
        return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - w) // 2
    top = round((im.height - h) * anchor)
    return im.crop((left, top, left + w, top + h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True, help="path to the OurSpecialVillage repo")
    ap.add_argument("--headshot", required=True, help="Amanda Rains headshot (Nov Village Hall)")
    args = ap.parse_args()
    for issue, items in ISSUE_ART.items():
        out = os.path.join(ROOT, "issues", issue, "art")
        os.makedirs(os.path.join(out, "icons"), exist_ok=True)
        for src, name, w, h, anchor in items:
            im = fit(flatten(Image.open(os.path.join(args.site, src))), w, h, anchor)
            im.save(os.path.join(out, name), "JPEG", quality=84, optimize=True, progressive=True)
        for name in SHARED:
            shutil.copyfile(os.path.join(ROOT, "art", name), os.path.join(out, name))
    # Amanda Rains: head-and-shoulders portrait at the same 320x418 as October's guest photo.
    im = flatten(Image.open(args.headshot))
    crop_w = round(im.width * 0.72)
    crop_h = round(crop_w * 418 / 320)
    left = (im.width - crop_w) // 2
    top = round(im.height * 0.04)
    im = im.crop((left, top, left + crop_w, top + crop_h)).resize((320, 418), Image.LANCZOS)
    im.save(os.path.join(ROOT, "issues", "2026-11", "art", "amanda-rains-160.jpg"), "JPEG",
            quality=86, optimize=True, progressive=True)
    for issue in ISSUE_ART:
        folder = os.path.join(ROOT, "issues", issue, "art")
        total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(folder) for f in fs)
        print(f"{issue}: {total // 1024} KB of art")


if __name__ == "__main__":
    main()
