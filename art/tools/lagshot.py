# Lesson 2 "Falling behind": crowd to max, then shoot the explain frame around the waiting pile.
import sys
from playwright.sync_api import sync_playwright
out = sys.argv[1] if len(sys.argv) > 1 else "/work/art/explore/lag-step.png"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1480, "height": 1000}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    pg.evaluate("enter(1)"); pg.wait_for_timeout(400); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
    pg.evaluate("$('#go').b.click()"); pg.wait_for_timeout(1500)
    pg.evaluate("S.rate=3; const r=$('#rate'); if(r){r.value=3; r.dispatchEvent(new Event('input',{bubbles:true})); r.dispatchEvent(new Event('change',{bubbles:true}))}")
    for i in range(60):
        if pg.evaluate("S.phase") == "explain": break
        pg.wait_for_timeout(500)
    pg.evaluate("setXray(true)"); pg.wait_for_timeout(1500)
    print("step:", pg.evaluate("STEP()?.title"), "phase:", pg.evaluate("S.phase"), "lag:", pg.evaluate("totalLag()"))
    pg.screenshot(path=out)
    # continue: card fades, then a hire -> NEW CHEF cut-in; card must wait for it
    pg.evaluate("nextStep()"); pg.wait_for_timeout(200); print("fading:", pg.evaluate("$('#lesson').className"))
    pg.wait_for_timeout(600); print("after fade hidden:", pg.evaluate("$('#lesson').hidden"), "step:", pg.evaluate("STEP().title"))
    pg.evaluate("$('#hire').b.click()"); pg.wait_for_timeout(1300)
    pg.screenshot(path=out.replace('.png','-cut.png'))
    t0 = pg.evaluate("NOW")
    for i in range(40):
        if pg.evaluate("S.phase") == "explain": break
        pg.wait_for_timeout(250)
    print("card after", round(pg.evaluate("NOW") - t0 + 1.3, 1), "s; cutins live:", pg.evaluate("FX.filter(f=>f.kind==='cutin'&&NOW-f.t0<f.dur).length"))
    pg.wait_for_timeout(700); pg.screenshot(path=out.replace('.png','-hire.png'))
    print("errors:", errs or "none"); b.close()
