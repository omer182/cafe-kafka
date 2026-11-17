# New lesson focus: shapes only. Lesson 1 clip/ticket, lesson 2 pile/head chef/Yuki, plus a forced station spotlight.
from playwright.sync_api import sync_playwright
def until_explain(pg, n=100):
    for i in range(n):
        if pg.evaluate("S.phase === 'explain' && !S.leaving"): return True
        pg.wait_for_timeout(250)
def nxt(pg): pg.evaluate("nextStep()"); pg.wait_for_timeout(700)
def shot(pg, name):
    pg.wait_for_timeout(900)
    print(name, "->", pg.evaluate("STEP().title"))
    pg.screenshot(path=f"/work/art/explore/f-{name}.png")
def start(pg, lvl):
    pg.evaluate(f"enter({lvl})"); pg.wait_for_timeout(400); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
    pg.evaluate("$('#go').b.click()"); pg.wait_for_timeout(1500)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1480, "height": 1000}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    start(pg, 0)
    for i in range(3):
        until_explain(pg); shot(pg, f"l1s{i+1}"); nxt(pg)
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    start(pg, 1); pg.evaluate("S.rate=3")
    until_explain(pg); shot(pg, "l2pile"); nxt(pg)
    pg.evaluate("$('#hire').b.click()"); until_explain(pg); shot(pg, "l2head"); nxt(pg)
    until_explain(pg); shot(pg, "l2yuki")
    pg.evaluate("LV().steps[S.si].at = () => stationAt(0)"); shot(pg, "spot")
    print("errors:", errs or "none"); b.close()
