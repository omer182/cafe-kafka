# Lesson 2 panel: hire button and the crowd slider (drag fast, let go), then iPhone (WebKit) home and in-game.
from playwright.sync_api import sync_playwright
O = "/work/art/explore/sk-"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    pg.evaluate("enter(1)"); pg.wait_for_timeout(600)
    pg.evaluate("$('#go')?.b?.click()"); pg.wait_for_timeout(800)
    pg.evaluate("S.flags.gate=0; for (let i=0;i<40 && STEP() && !/Falling/.test(STEP().title);i++) nextStep()"); pg.wait_for_timeout(1500)
    print("step:", pg.evaluate("STEP()?.title"), "rate:", pg.evaluate("S.rate"))
    pg.screenshot(path=O + "a-panel.png", clip={"x": 0, "y": 60, "width": 720, "height": 840})
    r = pg.locator("#rate"); bb = r.bounding_box(); print("slider", bb)
    y = bb["y"] + bb["height"] - 22
    pg.mouse.move(bb["x"] + 14, y); pg.mouse.down()
    for k in range(10): pg.mouse.move(bb["x"] + 14 + k * (bb["width"] - 20) / 9, y); pg.wait_for_timeout(16)
    pg.screenshot(path=O + "b-drag.png", clip={"x": 0, "y": 60, "width": 720, "height": 840})
    pg.mouse.up(); pg.wait_for_timeout(80); pg.screenshot(path=O + "c-release.png", clip={"x": 0, "y": 60, "width": 720, "height": 840})
    print("rate after:", pg.evaluate("S.rate"), pg.evaluate("$('#rateV').textContent"))
    print("errors:", errs or "none"); b.close()
    w = p.webkit.launch(); ctx = w.new_context(**p.devices["iPhone 14"]); pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(2600); pg.screenshot(path=O + "d-ip-home.png", full_page=True)
    pg.locator("#hstart").tap(); pg.wait_for_timeout(150); pg.screenshot(path=O + "e-ip-tap.png")
    pg.wait_for_timeout(900); pg.locator("#cast").tap(); pg.wait_for_timeout(900); pg.locator("#go").tap(); pg.wait_for_timeout(5000)
    pg.screenshot(path=O + "f-ip-game.png")
    print("ip scrollW:", pg.evaluate("document.documentElement.scrollWidth"), "errors:", errs or "none"); w.close()
