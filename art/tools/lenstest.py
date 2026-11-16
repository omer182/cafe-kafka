"""Fresh visitor: no code/X-ray at the start of lesson 1; they get introduced at the end; keep/hide choice."""
from playwright.sync_api import sync_playwright
def hdr(pg): return pg.evaluate("({xray: getComputedStyle($('#xray')).display, code: getComputedStyle($('#codebtn')).display, panel: $('#split').classList.contains('coded'), xon: save.xray, step: STEP()?.title, phase: S.phase, bar: $('#nowbar').hidden ? null : $('#nowbar').innerText.replace(/\\s+/g,' ')})")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    pg.click("#hstart"); pg.wait_for_timeout(500)
    for _ in range(4):
        btn = pg.locator(".veil:not([hidden]) .bell, .veil:not([hidden]) .btn.gold")
        if not btn.count(): break
        btn.first.click(); pg.wait_for_timeout(500)
    print("start  :", hdr(pg)); pg.screenshot(path="/work/art/explore/lens-0.png")
    pg.evaluate("S.si = LV().steps.findIndex(s => s.title === 'X-ray on'); $('#lesson').hidden = true; startStep()"); pg.wait_for_timeout(1200)
    print("xray   :", hdr(pg)); pg.screenshot(path="/work/art/explore/lens-1.png")
    pg.click("#nbtn"); pg.wait_for_timeout(1500); print("xray ok:", hdr(pg)); pg.click("#nbtn"); pg.wait_for_timeout(1200)
    print("code   :", hdr(pg)); pg.screenshot(path="/work/art/explore/lens-2.png")
    pg.click("#nbtn"); pg.wait_for_timeout(1500); pg.click("#nbtn"); pg.wait_for_timeout(500)
    for i in range(60):
        pg.wait_for_timeout(400)
        if pg.evaluate("S.phase") == "explain": break
    print("loop   :", hdr(pg)); pg.screenshot(path="/work/art/explore/lens-3.png")
    pg.click("#lhide"); pg.wait_for_timeout(800); print("hidden :", hdr(pg), "won:", pg.evaluate("S.won"))
    pg.evaluate("load(1)"); pg.wait_for_timeout(500); print("lesson2:", {k: v for k, v in hdr(pg).items() if k in ('xray','code')})
    print("errors:", errs or "none"); b.close()
