from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 2000, "height": 1122})
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    vals = pg.evaluate("""async () => { const g = document.querySelector('.glint'), out = [];
      for (let i = 0; i < 70; i++) { out.push(getComputedStyle(g, '::before').transform.split(',')[0].replace('matrix(', '')); await new Promise(r => setTimeout(r, 100)) } return out }""")
    print(vals)
    b.close()
