#!/usr/bin/env python3
"""Make the email's pictures safe for dark mode.

Gmail's apps and Outlook on Windows repaint an email for dark mode by themselves: light
backgrounds go dark and dark text goes light, but pictures (and background pictures) stay as
they are. Anything painted onto a cream or sky background then shows up as a pale box, and
text laid over a background picture turns pale on pale.

So every picture that sits on (or is) a background is turned into a see-through version:
the background colour becomes transparent and the email paints that colour behind it. In light
mode the two add up to exactly the old picture; in dark mode the paintings float on the dark
page and the text over the sky stays readable.

    python3 tools/dark-safe-art.py            # all issues + shared decor (idempotent)

Needs Pillow and numpy. Run after tools/render-decor.mjs.
"""
import json, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)


def rgbhex(c):
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in c)


def color_to_alpha(rgb, base, boost=1.0):
    """GIMP's colour-to-alpha against `base`, with optional `boost` (>=1) that makes the
    picture more solid. Either way, painting the result over `base` gives back `rgb`."""
    P = rgb.astype(float)
    B = base.reshape(1, 1, 3)
    up = np.where(P > B, (P - B) / np.maximum(255 - B, 1e-6), 0)
    down = np.where(P < B, (B - P) / np.maximum(B, 1e-6), 0)
    a = np.maximum(up, down).max(axis=2)
    a = np.clip(a * boost, 0, 1)
    safe = np.maximum(a, 1e-6)[..., None]
    C = np.clip(B + (P - B) / safe, 0, 255)
    C = np.where(a[..., None] > 0, C, B)
    return np.dstack([C, a * 255]).round().astype(np.uint8)


def edge_base(rgb, pct=99.0):
    """The picture's own background: the light end of its border pixels."""
    border = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    return np.array([np.percentile(border[:, c], pct) for c in range(3)])


def save(arr, out, quantize=False):
    im = Image.fromarray(arr, "RGBA")
    if quantize:
        im = im.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
    im.save(out, optimize=True)
    return os.path.getsize(out)


def has_alpha(path):
    im = Image.open(path)
    return im.mode in ("RGBA", "LA", "PA") and im.getchannel("A").getextrema()[0] < 255


# Shared decor: background pictures and pictures that fade into the cream page. Each one is cut
# against the colour the email paints behind it (the cell's bgcolor, or the cream page).
DECOR_BASES = {
    "cork.png": "#ecd9ae",      # CORK: the jump board and the pinboards
    "ruled.png": "#fffdf7",     # NOTE: the index card's ruled lines
    "stars.png": "#14203a",     # NAVY_DEEP: the starry night behind the parent groups
    "dusk-top.png": "#f7f1e2",  # CREAM: the sunset sliding into that night
    "dusk-wave.png": "#f7f1e2", # CREAM: the wave back to the page
}


def decor(folder):
    for name, base in DECOR_BASES.items():
        f = os.path.join(folder, name)
        if not os.path.exists(f) or has_alpha(f):
            continue
        rgb = np.asarray(Image.open(f).convert("RGB"))
        n = save(color_to_alpha(rgb, hexrgb(base)), f)
        print(f"  {os.path.relpath(f, ROOT)}: see-through on {base} ({n // 1024}KB)")


def sky(art_dir):
    """The hero's sky goes behind the title as a background picture. It becomes a see-through
    wash over its own lightest colour, which the email paints behind it (dark-safe.json)."""
    src = os.path.join(art_dir, "hero-sky.jpg")
    if not os.path.exists(src):
        return
    rgb = np.asarray(Image.open(src).convert("RGB"))
    base = rgb.reshape(-1, 3).max(axis=0).astype(float)
    n = save(color_to_alpha(rgb, base), os.path.join(art_dir, "hero-sky.png"))
    meta_path = os.path.join(art_dir, "dark-safe.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    meta["hero_sky_bg"] = rgbhex(base)
    with open(meta_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    print(f"  {os.path.relpath(src, ROOT)} -> hero-sky.png on {rgbhex(base)} ({n // 1024}KB)")


def _step(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def _smooth_alpha(a, grow=9, blur=6):
    """A softer alpha that never drops below `a` (so the colours stay exact): JPEG noise in the
    original makes colour-to-alpha speckled, which shows as blocks over a dark page."""
    from PIL import ImageFilter
    im = Image.fromarray((a * 255).round().astype(np.uint8), "L")
    im = im.filter(ImageFilter.MaxFilter(grow)).filter(ImageFilter.GaussianBlur(blur))
    return np.maximum(a, np.asarray(im).astype(float) / 255)


def _cut(P, base, floor, boost=1.0, solid=None):
    """Colour-to-alpha with a floor: alpha = max(the minimum alpha, floor). Exact over `base`.
    `solid` marks painted shapes that stay opaque; they are left out of the smoothing so no pale
    halo of sky grows around them."""
    B = base.reshape(1, 1, 3)
    up = np.where(P > B, (P - B) / np.maximum(255 - B, 1e-6), 0)
    down = np.where(P < B, (B - P) / np.maximum(B, 1e-6), 0)
    need = np.maximum(up, down).max(axis=2)
    soft = np.clip(need * boost, 0, 1)
    if solid is not None:
        from PIL import ImageFilter
        near = Image.fromarray(((solid > 0.01) * 255).astype(np.uint8), "L").filter(ImageFilter.MaxFilter(15))
        soft = soft * (np.asarray(near) == 0)
        floor = np.maximum(floor, solid)
    a = np.clip(np.maximum(_smooth_alpha(soft), floor), need, 1)
    C = np.clip(B + (P - B) / np.maximum(a, 1e-6)[..., None], 0, 255)
    return np.dstack([C, a * 255]).round().astype(np.uint8)


def land(art_dir):
    """The hills and the village under the title. The painted sky at the top of this picture melts
    into the see-through sky above it, so in dark mode the village sits under a night sky with the
    sun on the horizon instead of in a pale box. Two slices on the sky's colour: a see-through strip
    of sky with the far town and hills standing solid in it, then the painting itself as before (JPEG)."""
    src = os.path.join(art_dir, "hero-land.jpg")
    meta_path = os.path.join(art_dir, "dark-safe.json")
    if not os.path.exists(src) or not os.path.exists(meta_path):
        return
    meta = json.load(open(meta_path))
    P = np.asarray(Image.open(src).convert("RGB")).astype(float)
    H = P.shape[0]
    # the far hills are periwinkle (blue above red) and the sky is warm: the strip runs down into
    # the first row of hills that crosses the whole picture, on the 16px JPEG block grid
    blue = P[..., 2] - P[..., 0]
    solid = (blue > 4).mean(axis=1) > 0.99
    t = next(r for r in range(16, H // 2, 16) if solid[r - 8:r + 1].all())
    # the hills (and the town on them) are darker than the sky; the sun's glow is darker too but
    # far warmer. Lightness, not hue, finds the edges: the JPEG keeps colour at half resolution.
    S = P[:t]
    luma = S @ np.array([0.299, 0.587, 0.114])
    hills = _step((236 - luma) / 12) * _step((S[..., 2] - S[..., 0] + 45) / 20)
    # the sky by the horizon is paler than up top, so this strip gets its own (lightest) sky colour
    base = np.percentile(P[:t][hills < 0.01], 99.5, axis=0).round()
    n1 = save(_cut(P[:t], base, 0, solid=hills), os.path.join(art_dir, "hero-land-top.png"))
    meta["hero_land_bg"] = rgbhex(base)
    # same quantisation tables and a cut on the block grid, so the painting is barely re-touched
    from PIL import JpegImagePlugin
    jpg = Image.open(src)
    jpg.crop((0, t, P.shape[1], H)).save(os.path.join(art_dir, "hero-land-mid.jpg"), qtables=jpg.quantization,
                                         subsampling=JpegImagePlugin.get_sampling(jpg), optimize=True)
    meta["hero_land"] = [t, H - t]
    with open(meta_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    print(f"  {os.path.relpath(src, ROOT)} -> sky strip {t}px ({n1 // 1024}KB) + painting")


def mark_disc(art_dir, paper="#fffcf5"):
    """The footer's pin sits in a paper circle. Painting the circle into the picture keeps it
    paper-white when an app darkens the footer around it."""
    src = os.path.join(art_dir, "osv-mark-80.png")
    if not os.path.exists(src):
        return
    mark = Image.open(src).convert("RGBA")
    size = mark.size[0]
    scale = 4
    big = Image.new("L", (size * scale, size * scale), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(big).ellipse((0, 0, size * scale - 1, size * scale - 1), fill=255)
    disc = Image.new("RGBA", mark.size, tuple(int(v) for v in hexrgb(paper)) + (255,))
    disc.putalpha(big.resize(mark.size, Image.LANCZOS))
    disc.alpha_composite(mark)
    out = os.path.join(art_dir, "osv-mark-disc.png")
    disc.save(out, optimize=True)
    print(f"  {os.path.relpath(out, ROOT)}")


def main():
    cfg = json.load(open(os.path.join(ROOT, "tools", "decor.json")))
    decor(os.path.join(ROOT, cfg["shared_out"]))
    for iss in cfg["issues"]:
        art_dir = os.path.join(ROOT, iss["out"])
        sky(art_dir)
        land(art_dir)
        mark_disc(art_dir)


if __name__ == "__main__":
    main()
