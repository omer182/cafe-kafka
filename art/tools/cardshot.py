# Lesson 1 end: the "whole loop" card's two buttons, then the lesson-complete card (no scrollbars), desktop and iPhone.
from playwright.sync_api import sync_playwright
def run(pg, tag):
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    pg.evaluate("enter(0)"); pg.wait_for_timeout(400); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
    pg.evaluate("$('#go').b.click()"); pg.wait_for_timeout(3000)
    for i in range(40):
        if pg.evaluate("STEP()?.title") == "The whole loop": break
        pg.evaluate("S.phase='explain'; nextStep()"); pg.wait_for_timeout(200)
    pg.evaluate("S.served = 99; S.stats && (S.stats.served = 99)"); pg.wait_for_timeout(2500)
    pg.evaluate("if (S.phase !== 'explain') { S.phase='wait'; S.time+=5 }"); pg.wait_for_timeout(2500)
    el = pg.locator("#lesson")
    print(tag, "phase", pg.evaluate("S.phase"), "lesson visible", el.is_visible())
    if el.is_visible(): el.screenshot(path=f"/work/art/explore/cs-{tag}-loop.png")
    pg.evaluate("S.phase='explain'; nextStep()"); pg.wait_for_timeout(1200)
    c = pg.locator("#win .card")
    print(tag, "win scroll w/h vs client:", pg.evaluate("(()=>{const c=document.querySelector('#win .card');return [c.scrollWidth,c.clientWidth,c.scrollHeight,c.clientHeight]})()"))
    pg.screenshot(path=f"/work/art/explore/cs-{tag}-win.png")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}); run(pg, "desk"); b.close()
    w = p.webkit.launch(); ctx = w.new_context(**p.devices["iPhone 14"]); run(ctx.new_page(), "ip"); w.close()
