from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(2600)
    print("home buttons:", pg.locator(".cta button").all_inner_texts())
    pg.click("#hstart"); pg.wait_for_timeout(800)
    print("pills:", pg.locator("#pills button").all_inner_texts())
    pg.screenshot(path="/work/art/explore/nofree.png", clip={"x": 0, "y": 0, "width": 1440, "height": 70})
    print("errors:", errs or "none"); b.close()
