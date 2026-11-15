"""Contact sheet: art/sprites/*.png on the page's dark background, plus small sizes."""
import sys, glob, os
from PIL import Image, ImageDraw
src = sorted(glob.glob("/work/sprites/*.png"))
names = sys.argv[1:] or [os.path.basename(p)[:-4] for p in src]
cell = 200; small = (56, 32)
W = cell * len(names); H = cell + 80
img = Image.new("RGB", (W, H), "#16191C"); d = ImageDraw.Draw(img)
for i, n in enumerate(names):
    s = Image.open(f"/work/sprites/{n}.png").convert("RGBA")
    big = s.copy(); big.thumbnail((cell - 16, cell - 16), Image.LANCZOS)
    img.paste(big, (i * cell + (cell - big.width) // 2, 8), big)
    x = i * cell + 20
    for sz in small:
        t = s.copy(); t.thumbnail((sz, sz), Image.LANCZOS)
        img.paste(t, (x, cell + 4), t); x += sz + 14
    d.text((i * cell + 8, H - 16), n, fill="#7D868E")
img.save("/work/sheet.png")
print("sheet", img.size)
