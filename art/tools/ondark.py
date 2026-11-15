import sys
from PIL import Image
for p in sys.argv[1:]:
    im = Image.open(p).convert("RGBA"); bg = Image.new("RGBA", im.size, "#1B1E22")
    bg.alpha_composite(im); bg.convert("RGB").save(p.replace(".png", "-dark.png"))
