from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(2000, 1122), (2560, 1300), (1600, 900), (1366, 700)]:
        pg = b.new_page(viewport={"width": w, "height": h}); pg.goto("file:///work/index.html"); pg.wait_for_timeout(2600)
        r = pg.evaluate("""() => { const t = document.querySelector('.hero .cta').getBoundingClientRect(), imgs = [...document.querySelectorAll('.hcast img')].map(i => i.getBoundingClientRect());
          const hit = imgs.some(i => i.top < t.bottom && i.right > t.left && i.left < t.right); const ov = imgs.some((a, k) => imgs.some((b2, j) => j > k && a.right > b2.left + 2 && b2.right > a.left + 2));
          return {H: Math.round(imgs[1].height), ctaBottom: Math.round(t.bottom), castTop: Math.round(Math.min(...imgs.map(i => i.top))), hitsCTA: hit, overlap: ov} }""")
        print(w, h, r); pg.screenshot(path=f"/work/art/explore/size-{w}.png"); pg.close()
    b.close()
