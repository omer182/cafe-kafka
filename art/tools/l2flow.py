# Lesson 2: lag -> hire -> rebalance card -> idle card; lesson 3: huddle card still fires.
from playwright.sync_api import sync_playwright
def until_explain(pg, n=80):
    for i in range(n):
        if pg.evaluate("S.phase") == "explain": return True
        pg.wait_for_timeout(250)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1480, "height": 1000}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    pg.evaluate("enter(1)"); pg.wait_for_timeout(400); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
    pg.evaluate("$('#go').b.click()"); pg.wait_for_timeout(1500); pg.evaluate("S.rate=3")
    until_explain(pg); pg.wait_for_timeout(800); pg.evaluate("nextStep()"); pg.wait_for_timeout(1000)
    pg.evaluate("$('#hire').b.click()"); until_explain(pg); pg.wait_for_timeout(900)
    print("card:", pg.evaluate("STEP().title")); pg.screenshot(path="/work/art/explore/l2-rebalance.png")
    pg.evaluate("nextStep()"); pg.wait_for_timeout(700); until_explain(pg); pg.wait_for_timeout(900)
    print("card:", pg.evaluate("STEP().title")); pg.screenshot(path="/work/art/explore/l2-idle.png")
    pg.evaluate("load(2)"); pg.wait_for_timeout(400); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
    pg.evaluate("$('#go').b.click()"); pg.wait_for_timeout(2500)
    print("l3 step:", pg.evaluate("STEP().title"))
    pg.evaluate("$('#hire').b.click()"); until_explain(pg)
    print("l3 card:", pg.evaluate("STEP().title"), "huddle left:", pg.evaluate("S.huddle.toFixed(1)"))
    print("errors:", errs or "none"); b.close()
