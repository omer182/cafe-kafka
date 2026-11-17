# Smoke test the live site: loads, Sakuga components defined, lesson 1 reaches its first card, no errors or 4xx.
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("response", lambda r: errs.append(f"{r.status} {r.url}") if r.status >= 400 else None)
    pg.goto("https://kafka.omersher.com/"); pg.wait_for_timeout(3000)
    pg.evaluate("enter(0)"); pg.wait_for_timeout(500); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
    pg.evaluate("$('#go').b.click()"); pg.wait_for_timeout(9000)
    print("defined:", pg.evaluate("!!customElements.get('sakuga-button')"), "phase:", pg.evaluate("S.phase"), "step:", pg.evaluate("STEP().title"))
    print("errors:", errs or "none"); b.close()
