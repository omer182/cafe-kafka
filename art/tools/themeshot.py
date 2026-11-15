"""Screens for theme work: home, lesson intro card, lesson in play."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    pg.screenshot(path="/work/art/explore/theme-home.png")
    pg.click("#hstart"); pg.wait_for_timeout(1200)
    pg.screenshot(path="/work/art/explore/theme-intro.png")
    for _ in range(4):
        btn = pg.locator(".veil:not([hidden]) .bell, .veil:not([hidden]) .btn.gold")
        if not btn.count(): break
        btn.first.click(); pg.wait_for_timeout(800)
    pg.wait_for_timeout(9000)
    pg.screenshot(path="/work/art/explore/theme-play.png")
    print("errors:", errs or "none")
    b.close()
