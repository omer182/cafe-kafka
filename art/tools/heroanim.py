from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 900}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html")
    prev = 0
    for t in (350, 650, 1100, 2400):
        pg.wait_for_timeout(t - prev); prev = t
        pg.screenshot(path=f"/work/art/explore/heroanim-{t}.png")
    for w, h, n in [(1280, 800, "mid"), (1920, 1080, "big"), (390, 844, "phone")]:
        q = b.new_page(viewport={"width": w, "height": h}); q.goto("file:///work/index.html"); q.wait_for_timeout(2600); q.screenshot(path=f"/work/art/explore/hero-{n}.png"); q.close()
    print(errs or "ok"); b.close()
