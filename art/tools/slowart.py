# Slow art: a local server makes every chibi sprite take 3 s. Hire a chef right away: no emoji stand-in may appear.
import threading, time, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
class H(SimpleHTTPRequestHandler):
    def do_GET(self):
        if "/chibi-" in self.path: time.sleep(3)
        super().do_GET()
    def log_message(self, *a): pass
srv = ThreadingHTTPServer(("127.0.0.1", 8765), functools.partial(H, directory="/work")); threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("http://127.0.0.1:8765/index.html", wait_until="domcontentloaded"); pg.wait_for_timeout(600)
    pg.evaluate("enter(1)"); pg.wait_for_timeout(200); pg.evaluate("castShown=true; renderVeil(); $('#go').b.click()"); pg.wait_for_timeout(200)
    pg.evaluate("S.started=true; hire()"); pg.wait_for_timeout(500)
    print("still loading [Yuki, Marco]:", pg.evaluate("[loading('Yuki'), loading('Marco')]"), "chefs:", pg.evaluate("S.chefs.map(c=>c.n)"))
    pg.screenshot(path="/work/art/explore/slow-1.png", clip={"x": 360, "y": 60, "width": 1080, "height": 840})
    pg.wait_for_timeout(3500); pg.screenshot(path="/work/art/explore/slow-2.png", clip={"x": 360, "y": 60, "width": 1080, "height": 840})
    print("errors:", errs or "none"); b.close()
