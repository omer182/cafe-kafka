from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 2000, "height": 1122})
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(2600)
    pg.add_style_tag(content=".glint::before,.glint::after{animation:none!important;transform:translate(-50%,-50%) scale(1)!important}")
    pg.wait_for_timeout(200)
    box = pg.locator(".henrikw").bounding_box()
    pg.screenshot(path="/work/art/explore/glint.png", clip={"x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"] * .6})
    b.close()
