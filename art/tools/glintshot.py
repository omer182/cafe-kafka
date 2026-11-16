from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 2000, "height": 1122}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(2600); pg.screenshot(path="/work/art/explore/hero-2k.png")
    box = pg.locator(".henrikw").bounding_box()
    t0 = 1.8 + 3.2 * .8          # peak of the first glint
    pg.wait_for_timeout(int(t0 * 1000) - 2600 + 3200); pg.screenshot(path="/work/art/explore/glint.png", clip={"x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"] * .6})
    print(errs or "ok"); b.close()
