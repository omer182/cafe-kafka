# Hire a chef in lesson 2 and log which cut-in is on screen over time (NEW CHEF then HUDDLE).
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1480, "height": 1000}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    pg.evaluate("enter(1)"); pg.wait_for_timeout(400); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
    pg.evaluate("$('#go').b.click()"); pg.wait_for_timeout(1500)
    pg.evaluate("S.rate=3")
    for i in range(60):
        if pg.evaluate("S.phase") == "explain": break
        pg.wait_for_timeout(500)
    pg.wait_for_timeout(1200); pg.evaluate("nextStep()"); pg.wait_for_timeout(900)
    pg.evaluate("$('#hire').b.click()")
    for i in range(30):
        pg.wait_for_timeout(300)
        r = pg.evaluate("[+NOW.toFixed(2), FX.filter(f=>f.kind==='cutin').map(f=>f.title+'@'+f.t0.toFixed(2)+'/'+f.dur).join(' '), +S.huddle.toFixed(1)]")
        print(f"{(i+1)*.3:4.1f}s", r)
        if i == 10: pg.screenshot(path="/work/art/explore/huddle-cut.png")
    print("errors:", errs or "none"); b.close()
