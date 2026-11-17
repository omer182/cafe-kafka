# Sakuga controls check: home CTA, its impact frame, intro cards, lesson card, panel with the crowd slider, the now-bar.
from playwright.sync_api import sync_playwright
O = "/work/art/explore/sk-"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(2600)
    print("SakugaFX:", pg.evaluate("!!window.SakugaFX && customElements.get('sakuga-button') && customElements.get('sakuga-slider') ? 'ok' : 'missing'"))
    pg.screenshot(path=O + "1home.png")
    pg.locator("#hstart").click(); pg.wait_for_timeout(140); pg.screenshot(path=O + "2impact.png")
    pg.wait_for_timeout(900); pg.screenshot(path=O + "3cast.png")
    pg.locator("#cast").click(); pg.wait_for_timeout(1100); pg.screenshot(path=O + "4story.png")
    pg.locator("#go").click(); pg.wait_for_timeout(1500); pg.screenshot(path=O + "5game.png")
    for i in range(14):
        nb = pg.locator("#nbtn")
        if pg.locator("#lnext").count() and pg.locator("#lnext").is_visible():
            if i < 2: pg.screenshot(path=O + f"6lesson{i}.png")
            pg.locator("#lnext").click(); pg.wait_for_timeout(160)
            if i == 0: pg.screenshot(path=O + "7lnext.png")
        elif nb.count() and nb.is_visible():
            print("nowbar:", nb.inner_text()); nb.click()
        pg.wait_for_timeout(1400)
        t = pg.evaluate("STEP()?.title"); print(i, "step:", t)
        if t and "Falling" in t: break
    r = pg.locator("#rate")
    if r.count():
        bb = r.bounding_box(); print("slider box", bb)
        pg.mouse.move(bb["x"] + 20, bb["y"] + bb["height"] - 20); pg.mouse.down()
        for k in range(8): pg.mouse.move(bb["x"] + 20 + k * bb["width"] / 8, bb["y"] + bb["height"] - 20); pg.wait_for_timeout(16)
        pg.screenshot(path=O + "8slide.png"); pg.mouse.up(); pg.wait_for_timeout(60); pg.screenshot(path=O + "9release.png")
        print("rate now:", pg.evaluate("S.rate"))
    print("errors:", errs or "none"); b.close()
