from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(800)
    pg.click("#hfree"); pg.wait_for_timeout(800)
    pg.get_by_text("Open the kitchen").click(); pg.wait_for_timeout(3000)
    box = pg.locator("#cv").bounding_box(); clip = {"x": box["x"], "y": box["y"], "width": box["width"], "height": min(box["height"], 900 - box["y"])}
    pg.screenshot(path="/work/art/explore/hc-idle.png", clip=clip)
    pg.locator("button", has_text="Add a rail").first.click(); pg.wait_for_timeout(500)
    pg.screenshot(path="/work/art/explore/hc-huddle.png", clip=clip)
    pg.wait_for_timeout(1300); pg.screenshot(path="/work/art/explore/hc-huddle2.png", clip=clip)
    print("errors:", errs or "none")
    b.close()
