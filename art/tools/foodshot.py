from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(800)
    pg.click("#hfree"); pg.wait_for_timeout(800)
    pg.get_by_text("Open the kitchen").click(); pg.wait_for_timeout(500)
    pg.click("#hire"); pg.wait_for_timeout(500)
    pg.locator("button", has_text="Open the dessert station").first.click(); pg.wait_for_timeout(500)
    pg.evaluate("S.rate = 1.6"); pg.wait_for_timeout(14000)
    box = pg.locator("#cv").bounding_box()
    pg.screenshot(path="/work/art/explore/food-game.png", clip={"x": box["x"], "y": box["y"], "width": box["width"], "height": min(box["height"], 900 - box["y"])})
    print("errors:", errs or "none")
    b.close()
