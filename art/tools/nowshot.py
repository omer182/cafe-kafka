"""Lesson 2: check locking + the now-bar across watch / read / do steps."""
from playwright.sync_api import sync_playwright
def state(pg):
    return pg.evaluate("""() => ({phase: S.phase, step: STEP().title, bar: $('#nowbar').hidden ? null : $('#nowbar').innerText.replace(/\\s+/g,' '),
      locked: [...document.querySelectorAll('#ctls .locked')].map(e => e.id || e.className).join(','),
      hire: $('#hire') ? getComputedStyle($('#hire')).pointerEvents : '-'})""")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(700)
    pg.click("#hstart"); pg.wait_for_timeout(500)
    pg.evaluate("load(1)"); pg.wait_for_timeout(500)
    print("veil:", state(pg))
    pg.screenshot(path="/work/art/explore/now-0-veil.png")
    for _ in range(4):
        btn = pg.locator(".veil:not([hidden]) .bell, .veil:not([hidden]) .btn.gold")
        if not btn.count(): break
        btn.first.click(); pg.wait_for_timeout(500)
    shots = {}
    for i in range(160):
        st = state(pg)
        k = ("read" if st["phase"] == "explain" else ("do-btn" if "Hire" in (st["bar"] or "") else ("do" if "YOUR TURN" in (st["bar"] or "") else "watch")))
        if k not in shots:
            shots[k] = st; print(k, ":", st); pg.screenshot(path=f"/work/art/explore/now-{k}.png")
        if k == "do-btn":
            n0 = pg.evaluate("S.chefs.length"); pg.click("#nbtn"); pg.wait_for_timeout(900)
            print("hired via bar:", n0, "->", pg.evaluate("S.chefs.length")); break
        if k == "read": pg.click("#nbtn")
        elif "Crowd" in (st["bar"] or ""): pg.evaluate("S.rate = st0 = +$('#rate').max; $('#rate').value = S.rate".replace("st0 = ", ""))
        pg.wait_for_timeout(400)
    print("errors:", errs or "none")
    b.close()
