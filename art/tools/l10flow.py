# Lessons 10 (retention) and 11 (replication): play every step, screenshot each card.
import sys
from playwright.sync_api import sync_playwright
XR = len(sys.argv) > 1 and sys.argv[1] == "xray"
def until_explain(pg, n=240):
    for i in range(n):
        if pg.evaluate("S.phase") == "explain": return True
        pg.wait_for_timeout(250)
    print("  !! timed out on", pg.evaluate("STEP().title")); return False
def card(pg, name):
    ok = until_explain(pg); pg.wait_for_timeout(1000)
    print(f"  card {pg.evaluate('S.si+1')}: {pg.evaluate('STEP().title')}")
    pg.screenshot(path=f"/work/art/explore/{name}.png")
    pg.evaluate("$('#lesson').style.visibility='hidden'"); pg.locator('#cv').screenshot(path=f"/work/art/explore/{name}-cv.png"); pg.evaluate("$('#lesson').style.visibility=''")
    pg.evaluate("nextStep()"); pg.wait_for_timeout(2600)
    pg.locator('#cv').screenshot(path=f"/work/art/explore/{name}-play.png")
    return ok
def start(pg, lvl):
    pg.evaluate(f"enter({lvl})"); pg.wait_for_timeout(400); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
    pg.evaluate("$('#go').b.click(); S.speed=1"); pg.wait_for_timeout(500)
def click(pg, sel):
    pg.evaluate(f"(() => {{ const t = $('{sel}'); t.b ? t.b.click() : t.click() }})()")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1480, "height": 1000}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    pg.evaluate(f"save.xray={'true' if XR else 'false'}; setCode(false)")
    s = "x" if XR else ""
    print("lesson 10 retention")
    start(pg, 9)
    card(pg, f"r1{s}")
    click(pg, "#aud"); card(pg, f"r2{s}")
    click(pg, "#aud"); card(pg, f"r3{s}")
    click(pg, "#aud"); card(pg, f"r4{s}")
    print("   missed:", pg.evaluate("S.flags.missed"), "binned:", pg.evaluate("S.stats.binned"), "lost:", pg.evaluate("S.stats.lost"))
    pg.evaluate("[...document.querySelectorAll('#ret button')].find(b => b.dataset.v === 'long').click()"); card(pg, f"r5{s}")
    pg.wait_for_timeout(1500); print("   won:", pg.evaluate("S.won")); pg.screenshot(path=f"/work/art/explore/rwin{s}.png")
    print("lesson 11 replication")
    start(pg, 10)
    card(pg, f"p1{s}")
    card(pg, f"p2{s}")
    click(pg, "#fall"); card(pg, f"p3{s}")
    print("   lost:", pg.evaluate("S.stats.lost"), "lead:", pg.evaluate("S.rep.lead"))
    pg.evaluate("[...document.querySelectorAll('#acks button')].find(b => b.dataset.v === 'all').click()"); card(pg, f"p4{s}")
    click(pg, "#fall"); card(pg, f"p5{s}")
    print("   lost:", pg.evaluate("S.stats.lost"), "retried ticket:", pg.evaluate("S.flags.retried && S.flags.retried.off"))
    card(pg, f"p6{s}")
    pg.wait_for_timeout(1500); print("   won:", pg.evaluate("S.won")); pg.screenshot(path=f"/work/art/explore/pwin{s}.png")
    print("errors:", errs or "none"); b.close()
