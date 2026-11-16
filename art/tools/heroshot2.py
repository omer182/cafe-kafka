from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h, n in [(1600, 900, "wide"), (1280, 800, "mid"), (390, 844, "phone")]:
        pg = b.new_page(viewport={"width": w, "height": h}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file:///work/index.html"); pg.wait_for_timeout(1800)
        pg.screenshot(path=f"/work/art/explore/hero-{n}.png"); print(n, errs or "ok"); pg.close()
    b.close()
