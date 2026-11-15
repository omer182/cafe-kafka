"""Free play: shot of the kitchen while cooking, then trip a chef and shoot again."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1400, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(800)
    pg.click("#hfree"); pg.wait_for_timeout(1000)
    pg.get_by_text("Open the kitchen").click(); pg.wait_for_timeout(1000)
    pg.click("#hire"); pg.wait_for_timeout(5500)
    pg.screenshot(path="/work/art/explore/game-cook.png")
    pg.click("#trip")
    for i in range(30):
        pg.wait_for_timeout(500)
        if pg.evaluate("S.chefs.some(c => c.down)"):
            pg.wait_for_timeout(700); break
    pg.screenshot(path="/work/art/explore/game-down.png")
    print("down:", pg.evaluate("S.chefs.filter(c => c.down).map(c => c.n)"), "errors:", errs or "none")
    b.close()
