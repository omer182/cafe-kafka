from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch()
    for dev in ["iPhone SE", "iPhone 14", "iPhone 15 Pro Max"]:
        ctx = b.new_context(**p.devices[dev]); pg = ctx.new_page(); pg.goto("file:///work/index.html"); pg.wait_for_timeout(2600)
        n = dev.replace(" ", ""); pg.screenshot(path=f"/work/art/explore/ip-{n}-1home.png", full_page=True)
        print(dev, "h-scroll:", pg.evaluate("document.documentElement.scrollWidth > innerWidth"), "page h:", pg.evaluate("document.documentElement.scrollHeight"), "vh:", pg.evaluate("innerHeight"))
        ctx.close()
    b.close()
