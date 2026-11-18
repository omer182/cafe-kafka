# Lessons 10 and 11 at phone width: one mid-play frame each.
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    for lvl, name in [(9, "ph-ret"), (10, "ph-rep")]:
        pg.evaluate(f"enter({lvl})"); pg.wait_for_timeout(400); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
        pg.evaluate("$('#go').b.click(); S.speed=1"); pg.wait_for_timeout(14000)
        if lvl == 9: pg.evaluate("S.phase='free'; $('#lesson').hidden=true; toggleAud()"); pg.wait_for_timeout(4000)
        pg.evaluate("S.phase='free'; $('#lesson').hidden=true"); pg.wait_for_timeout(600)
        pg.locator('#cv').screenshot(path=f"/work/art/explore/{name}.png")
    print("errors:", errs or "none"); b.close()
