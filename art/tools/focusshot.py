"""Lesson 1: step through until a step highlights the chef, screenshot it."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(800)
    pg.click("#hstart"); pg.wait_for_timeout(600)
    for _ in range(4):
        btn = pg.locator(".veil:not([hidden]) .bell, .veil:not([hidden]) .btn.gold")
        if not btn.count(): break
        btn.first.click(); pg.wait_for_timeout(600)
    for i in range(40):
        pg.wait_for_timeout(500)
        t = pg.evaluate("S.phase === 'explain' && (STEP().title || '')")
        if t == 'An order comes in': break
        nxt = pg.locator(".lesson:not([hidden]) .btn.gold")
        if t and nxt.count(): nxt.first.click()
    pg.wait_for_timeout(700)
    box = pg.locator("#cv").bounding_box()
    pg.screenshot(path="/work/art/explore/focus.png", clip={"x": box["x"], "y": box["y"], "width": box["width"], "height": min(box["height"], 900 - box["y"])})
    print("step:", t, "errors:", errs or "none")
    b.close()
