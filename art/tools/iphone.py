"""iPhone check in WebKit: home, lesson intro card, a lesson step with the now-bar and the card."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch()
    for dev in ["iPhone SE", "iPhone 14", "iPhone 15 Pro Max"]:
        d = p.devices[dev]; ctx = b.new_context(**d); pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        n = dev.replace(" ", "")
        pg.goto("file:///work/index.html"); pg.wait_for_timeout(2600); pg.screenshot(path=f"/work/art/explore/ip-{n}-1home.png")
        over = pg.evaluate("document.documentElement.scrollWidth > innerWidth")
        pg.tap("#hstart"); pg.wait_for_timeout(900); pg.screenshot(path=f"/work/art/explore/ip-{n}-2intro.png")
        for _ in range(4):
            btn = pg.locator(".veil:not([hidden]) .bell, .veil:not([hidden]) .btn.gold")
            if not btn.count(): break
            btn.first.tap(); pg.wait_for_timeout(600)
        pg.wait_for_timeout(1500); pg.screenshot(path=f"/work/art/explore/ip-{n}-3watch.png")
        for i in range(40):
            pg.wait_for_timeout(400)
            if pg.evaluate("S.phase") == "explain": break
        pg.wait_for_timeout(700); pg.screenshot(path=f"/work/art/explore/ip-{n}-4card.png")
        bar = pg.evaluate("(() => { const r = $('#nowbar').getBoundingClientRect(); return {top: Math.round(r.top), bottom: Math.round(r.bottom), w: Math.round(r.width), vw: innerWidth, vh: innerHeight, hidden: $('#nowbar').hidden} })()")
        print(dev, "h-scroll:", over, "bar:", bar, "errors:", errs or "none")
        ctx.close()
    b.close()
