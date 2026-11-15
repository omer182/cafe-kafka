from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(2600)
    box = pg.locator(".demo").bounding_box()
    pg.screenshot(path="/work/art/explore/hero-a.png", clip=box)
    pg.wait_for_timeout(1300); pg.screenshot(path="/work/art/explore/hero-b.png", clip=box)
    print("errors:", errs or "none")
    b.close()
