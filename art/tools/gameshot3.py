"""Free play with a big crowd, so diners go through waiting / upset / angry / happy."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1400, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(800)
    pg.click("#hfree"); pg.wait_for_timeout(1000)
    pg.get_by_text("Open the kitchen").click(); pg.wait_for_timeout(1000)
    pg.evaluate("S.rate = 2.2")
    for t in (6, 14, 22):
        pg.wait_for_timeout(8000 if t > 6 else 6000)
        pg.screenshot(path=f"/work/art/explore/diners-{t}.png", clip={"x": 366, "y": 130, "width": 564, "height": 150})
    print("errors:", errs or "none")
    b.close()
