"""Render manga-fx.html at fixed times and stitch an animated GIF + a keyframe strip."""
from playwright.sync_api import sync_playwright
from PIL import Image
import io
FPS = 15; LOOP = 3.4
frames = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 960, "height": 540})
    for i in range(int(LOOP * FPS)):
        t = i / FPS
        pg.goto(f"file:///work/explore/manga-fx.html?t={t:.3f}")
        pg.wait_for_function("window.READY === true"); pg.wait_for_timeout(80)
        frames.append(Image.open(io.BytesIO(pg.screenshot())).convert("RGB"))
    b.close()
small = [f.resize((640, 360), Image.LANCZOS) for f in frames]
small[0].save("/work/explore/manga-fx.gif", save_all=True, append_images=small[1:], duration=int(1000 / FPS), loop=0, optimize=True)
keys = [0.3, 0.64, 0.8, 1.4, 2.3]
strip = Image.new("RGB", (960, 270 * ((len(keys) + 1) // 2)), "#0F1113")
for j, t in enumerate(keys):
    f = frames[min(len(frames) - 1, round(t * FPS))].resize((480, 270), Image.LANCZOS)
    strip.paste(f, ((j % 2) * 480, (j // 2) * 270))
strip.save("/work/explore/manga-fx-keys.png")
print("frames", len(frames))
