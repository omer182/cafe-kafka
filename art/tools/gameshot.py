"""Open the game, start free play, hire chefs, and screenshot the kitchen."""
import sys
from playwright.sync_api import sync_playwright
out = sys.argv[1] if len(sys.argv) > 1 else "/work/art/explore/game.png"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1400, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(800)
    pg.click("#hfree"); pg.wait_for_timeout(1200)
    pg.get_by_text("Open the kitchen").click(); pg.wait_for_timeout(1500)
    for _ in range(2):
        try:
            pg.click("#hire", timeout=1500); pg.wait_for_timeout(2500)
        except Exception as e:
            print("hire:", str(e)[:80])
    pg.wait_for_timeout(5000)
    pg.screenshot(path=out)
    print("errors:", errs or "none")
    b.close()
