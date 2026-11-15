"""Trigger each manga moment in free play and screenshot it mid-animation."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(800)
    pg.click("#hfree"); pg.wait_for_timeout(800)
    pg.get_by_text("Open the kitchen").click(); pg.wait_for_timeout(500)
    box = pg.locator("#cv").bounding_box()
    clip = {"x": box["x"], "y": box["y"], "width": box["width"], "height": min(box["height"], 900 - box["y"])}
    # 1. first dish served: impact frame, then the ORDER UP cut-in
    for i in range(80):
        pg.wait_for_timeout(100)
        if pg.evaluate("FX.some(f => f.kind === 'impact')"): break
    pg.wait_for_timeout(150); pg.screenshot(path="/work/art/explore/fx-1-served.png", clip=clip)
    pg.wait_for_timeout(1000); pg.screenshot(path="/work/art/explore/fx-2-orderup.png", clip=clip)
    pg.wait_for_timeout(1800)
    # 2. hire: NEW CHEF cut-in
    pg.click("#hire"); pg.wait_for_timeout(450); pg.screenshot(path="/work/art/explore/fx-3-hire.png", clip=clip)
    pg.wait_for_timeout(2600)
    # 3. trip: CHEF DOWN cut-in
    pg.click("#trip")
    for i in range(60):
        pg.wait_for_timeout(100)
        if pg.evaluate("FX.some(f => f.kind === 'cutin' && f.title === 'CHEF DOWN!')"): break
    pg.wait_for_timeout(450); pg.screenshot(path="/work/art/explore/fx-4-down.png", clip=clip)
    print("errors:", errs or "none")
    b.close()
