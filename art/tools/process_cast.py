"""Turn generated character art into game-ready files.

Input:  /in/<who>_<kind>[_<variant>].(png|webp|jpg), e.g. yuki_chibi_cook.webp
Output: /out/<who>/<kind>[-<variant>].webp, trimmed and sized for how the game uses it,
        plus /out/manifest.json listing everything.

If an image has no transparency (solid background), the background is flood-filled
away from the borders. The dark outline stops the fill, so white clothing survives.
"""
import glob
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFilter

IN, OUT = "/in", "/out"
SIZE = {                      # longest-side target per kind (about 2x what the game draws)
    "chibi": ("h", 320),      # kitchen sprite, drawn ~120-160px tall
    "bust": ("w", 900),       # manga cut-in panel
    "portrait": ("h", 1200),  # intro / lesson panel
    "sheet": ("w", 1536),     # reference only
    "food": ("w", 256),
}


def cutout(im):
    im = im.convert("RGBA")
    a = im.split()[3]
    if a.getextrema()[0] < 250:          # already has real transparency
        return im
    # flood-fill the background from every border pixel that looks like background
    bg = im.convert("RGB")
    mask = Image.new("L", im.size, 0)
    ref = bg.getpixel((2, 2))
    W, H = im.size
    seeds = [(x, 0) for x in range(0, W, 8)] + [(x, H - 1) for x in range(0, W, 8)] + \
            [(0, y) for y in range(0, H, 8)] + [(W - 1, y) for y in range(0, H, 8)]
    work = bg.copy()
    for s in seeds:
        if sum(abs(p - q) for p, q in zip(work.getpixel(s), ref)) < 40:
            ImageDraw.floodfill(work, s, (255, 0, 255), thresh=38)
    for y in range(H):
        for x in range(W):
            if work.getpixel((x, y)) == (255, 0, 255):
                mask.putpixel((x, y), 255)
    alpha = Image.eval(mask.filter(ImageFilter.GaussianBlur(0.8)), lambda v: 255 - v)
    im.putalpha(alpha)
    return im


def trim(im, pad=6):
    box = im.split()[3].point(lambda v: 255 if v > 16 else 0).getbbox()
    if not box:
        return im
    l, t, r, b = box
    return im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad)))


def main():
    manifest = {}
    only = set(sys.argv[1:])
    for f in sorted(glob.glob(f"{IN}/*")):
        base = os.path.splitext(os.path.basename(f))[0]
        parts = base.split("_")
        if len(parts) < 2 or (only and parts[0] not in only):
            continue
        who, kind, variant = parts[0], parts[1], "-".join(parts[2:])
        if kind not in SIZE:
            print("skip (unknown kind)", base); continue
        im = trim(cutout(Image.open(f)))
        axis, n = SIZE[kind]
        k = n / (im.height if axis == "h" else im.width)
        if k < 1:
            im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        name = kind + (f"-{variant}" if variant else "")
        os.makedirs(f"{OUT}/{who}", exist_ok=True)
        dst = f"{OUT}/{who}/{name}.webp"
        im.save(dst, "WEBP", quality=88, method=6)
        manifest.setdefault(who, {})[name] = {"file": f"{who}/{name}.webp", "w": im.width, "h": im.height}
        print(f"{base:28s} -> {dst}  {im.width}x{im.height}  {os.path.getsize(dst) // 1024}KB")
    old = {}
    if os.path.exists(f"{OUT}/manifest.json"):
        old = json.load(open(f"{OUT}/manifest.json"))
    for who, v in manifest.items():
        old.setdefault(who, {}).update(v)
    json.dump(old, open(f"{OUT}/manifest.json", "w"), indent=1, sort_keys=True)


main()
