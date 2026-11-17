# Diner mood marks: let lag build in lesson 2, puff every mark in a row, shoot the dining room.
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1480, "height": 1000}, device_scale_factor=2); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///work/index.html"); pg.wait_for_timeout(1500)
    pg.evaluate("enter(1)"); pg.wait_for_timeout(400); pg.evaluate("castShown=true; renderVeil()"); pg.wait_for_timeout(300)
    pg.evaluate("$('#go').b.click()"); pg.wait_for_timeout(1500)
    pg.evaluate("S.rate=3; LV().steps[0].until=()=>false"); pg.wait_for_timeout(9000)
    pg.evaluate("['🙂','😐','😠','😋','😤','👋','🤨','😡'].forEach((e,i)=>S.parts.push({x:120+i*80,y:160,vx:0,vy:0,life:30,max:30,text:e}))")
    pg.wait_for_timeout(400)
    r = pg.evaluate("(()=>{const r=cv.getBoundingClientRect();return [r.left,r.top,r.width]})()")
    pg.screenshot(path="/work/art/explore/marks.png", clip={"x": r[0], "y": r[1], "width": r[2], "height": 300})
    pg.wait_for_timeout(8000)
    pg.screenshot(path="/work/art/explore/marks2.png", clip={"x": r[0], "y": r[1], "width": r[2], "height": 300})
    print("errors:", errs or "none"); b.close()
