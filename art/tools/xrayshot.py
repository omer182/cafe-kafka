# Lesson 1 "X-ray on" step: the focus frame on the brass clip with X-ray turned on.
import sys
from playwright.sync_api import sync_playwright
out = sys.argv[1] if len(sys.argv) > 1 else "/work/art/explore/xr-step.png"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    pg.evaluate("enter(0)"); pg.wait_for_timeout(400); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
    pg.evaluate("$('#go').b.click()"); pg.wait_for_timeout(4000)
    for i in range(40):
        t = pg.evaluate("STEP()?.title")
        if t == "X-ray on": break
        pg.evaluate("S.phase==='explain' ? nextStep() : (S.phase='explain', nextStep())"); pg.wait_for_timeout(250)
    pg.wait_for_timeout(1500); pg.evaluate("setXray(true)"); pg.wait_for_timeout(1500)
    print("step:", pg.evaluate("STEP()?.title"), "phase:", pg.evaluate("S.phase"))
    box = pg.evaluate("(()=>{const a=clipPos(0,0),r=cv.getBoundingClientRect();return [r.left+a.x*K, r.top+a.y*K]})()")
    pg.screenshot(path=out, clip={"x": max(0, box[0] - 260), "y": max(0, box[1] - 200), "width": 760, "height": 420})
    print("errors:", errs or "none"); b.close()
