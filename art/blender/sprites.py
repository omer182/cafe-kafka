"""Café Kafka sprite renderer.

Builds every sprite procedurally (no hand modelling) and renders each one to a
transparent PNG with Cycles on the CPU. Run it with:

  docker run --rm -v "$PWD/art":/work cafe-blender:4.2.3 --python /work/blender/sprites.py -- [names...]

The PNGs land in art/sprites/. With no names, every sprite is rendered.
"""
import math
import sys
import os
import bpy
import bmesh
from mathutils import Vector

OUT = "/work/sprites"
SIZE = 256          # pixels per sprite
SAMPLES = 48

# ---------- palette (from the page's CSS) ----------
PAPER = "#F6F2EA"; INK = "#1D1B18"; BRASS = "#D9A441"; TOMATO = "#E4573D"
HERB = "#7FB069"; BLUE = "#5B8DB8"; LILAC = "#C9A0DC"; NEON = "#FF5E3A"
SKIN = ["#F2C9A5", "#E0A97E", "#B97A50", "#7A4B2E"]
TEAM = [TOMATO, BLUE, HERB, LILAC, BRASS, "#4FB6A8"]


def hexc(h, a=1.0):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    return (*lin, a)


_mats = {}


def mat(color, rough=0.45, metal=0.0, sss=0.0, emit=0.0, coat=0.25):
    key = (color, rough, metal, sss, emit, coat)
    if key in _mats:
        return _mats[key]
    m = bpy.data.materials.new(f"m{len(_mats)}")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexc(color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.3
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (0.4, 0.2, 0.1)
        b.inputs["Subsurface Scale"].default_value = 0.05
    if emit:
        b.inputs["Emission Color"].default_value = hexc(color)
        b.inputs["Emission Strength"].default_value = emit
    _mats[key] = m
    return m


# ---------- primitive helpers ----------
COLL = None


def _finish(o, m, smooth=True, bevel=0.0, subd=0):
    for c in o.users_collection:
        c.objects.unlink(o)
    COLL.objects.link(o)
    o.data.materials.append(m)
    if smooth:
        for p in o.data.polygons:
            p.use_smooth = True
    if bevel:
        mod = o.modifiers.new("bev", "BEVEL"); mod.width = bevel; mod.segments = 3
    if subd:
        mod = o.modifiers.new("sub", "SUBSURF"); mod.levels = subd; mod.render_levels = subd
    return o


def ball(loc, r, m, scale=(1, 1, 1), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=r, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = scale
    return _finish(o, m)


def cyl(loc, r, depth, m, scale=(1, 1, 1), rot=(0, 0, 0), bevel=0.02, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = scale
    return _finish(o, m, bevel=bevel)


def box(loc, size, m, rot=(0, 0, 0), bevel=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = size
    return _finish(o, m, smooth=False, bevel=bevel)


def ring(loc, R, r, m, scale=(1, 1, 1), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot,
                                     major_segments=48, minor_segments=16)
    o = bpy.context.object; o.scale = scale
    return _finish(o, m)


def cone(loc, r1, r2, depth, m, rot=(0, 0, 0), bevel=0.01):
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    return _finish(bpy.context.object, m, bevel=bevel)


def wedge(loc, R, angle, z0, z1, m, bevel=0.02):
    """A cake-slice prism: pie wedge of radius R and opening `angle`, from z0 to z1."""
    me = bpy.data.meshes.new("wedge"); bm = bmesh.new()
    n = 16
    pts = [(0, 0)] + [(R * math.cos(-angle / 2 + angle * i / n), R * math.sin(-angle / 2 + angle * i / n)) for i in range(n + 1)]
    bot = [bm.verts.new((x, y, z0)) for x, y in pts]
    top = [bm.verts.new((x, y, z1)) for x, y in pts]
    bm.faces.new(bot[::-1]); bm.faces.new(top)
    k = len(pts)
    for i in range(k):
        j = (i + 1) % k
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("wedge", me); o.location = loc
    COLL.objects.link(o)
    o.data.materials.append(m)
    mod = o.modifiers.new("bev", "BEVEL"); mod.width = bevel; mod.segments = 3; mod.limit_method = "ANGLE"
    return o


# ---------- characters: chunky vinyl toys ----------
def eyes(z, skin_r, spread=0.11, y=None):
    y = -skin_r * 0.93 if y is None else y
    black = mat(INK, rough=0.15, coat=1)
    for s in (-1, 1):
        ball((s * spread, y, z), 0.05, black, scale=(1, 0.7, 1.3))
        ball((s * spread + 0.014, y - 0.035, z + 0.025), 0.014, mat("#FFFFFF", emit=2))   # catch-light


def smile(z, skin_r):
    ring((0, -skin_r * 0.95, z), 0.05, 0.012, mat("#7A3B2E", rough=0.5), scale=(1, 0.5, 0.6), rot=(math.pi / 2, 0, 0))


def cheeks(z, skin_r):
    for s in (-1, 1):
        ball((s * 0.2, -skin_r * 0.86, z), 0.05, mat("#F28C8C", rough=0.7), scale=(1, 0.4, 0.7))


def figure(body_col, skin, head_z=1.2, body_scale=(1, 0.85, 1.05)):
    """Pear-shaped body, big round head, stubby hands and feet. Returns head radius."""
    body = mat(body_col, rough=0.55)
    ball((0, 0, 0.55), 0.48, body, scale=body_scale)
    skin_m = mat(skin, rough=0.5, sss=0.3)
    hr = 0.4
    ball((0, 0, head_z), hr, skin_m)
    for s in (-1, 1):
        ball((s * 0.5, -0.05, 0.6), 0.12, skin_m)                      # hands
        ball((s * 0.2, -0.08, 0.06), 0.14, mat(INK, rough=0.35), scale=(1, 1.3, 0.55))  # shoes
    eyes(head_z + 0.03, hr)
    cheeks(head_z - 0.08, hr)
    smile(head_z - 0.13, hr)
    return hr


def chef(name, skin, scarf):
    hr = figure(PAPER, skin)
    white = mat("#FFFFFF", rough=0.6)
    for s in (-1, 1):                                                   # double-breasted buttons
        for z in (0.45, 0.7):
            ball((s * 0.12, -0.42, z), 0.035, mat(INK, rough=0.3))
    ring((0, -0.02, 0.93), 0.27, 0.07, mat(scarf, rough=0.5), scale=(1, 0.9, 1))   # neckerchief
    ball((0, -0.3, 0.88), 0.09, mat(scarf, rough=0.5), scale=(1, 0.6, 1.2))         # knot
    cyl((0, 0, 1.55), 0.33, 0.28, white, bevel=0.03)                               # toque band
    for x, y, z in [(0, 0, 1.82), (-0.2, 0.05, 1.76), (0.2, 0.05, 1.76), (0, 0.16, 1.78), (0, -0.14, 1.76)]:
        ball((x, y, z), 0.24, white)                                                # puffy top


def waiter(skin):
    figure("#23272B", skin)
    ball((0, -0.36, 0.62), 0.26, mat("#FFFFFF", rough=0.5), scale=(0.75, 0.35, 1.2))  # shirt front
    bow = mat(TOMATO, rough=0.4)
    for s in (-1, 1):
        cone((s * 0.08, -0.47, 0.9), 0.07, 0.0, 0.14, bow, rot=(0, s * math.pi / 2, 0))
    ball((0, -0.47, 0.9), 0.035, bow)
    hair = mat("#2A1E17", rough=0.35, coat=0.8)
    ball((0, 0.03, 1.27), 0.42, hair, scale=(1.03, 1.03, 0.78))                     # slicked hair
    ball((-0.1, -0.22, 1.5), 0.2, hair, scale=(1.6, 1, 0.55), rot=(0, -0.25, 0))    # side-part quiff
    # tray with a cloche held high on the right
    X = 0.82
    ball((0.56, -0.05, 0.85), 0.12, mat(skin, sss=0.3))                             # raised hand
    cyl((X, -0.05, 0.95), 0.3, 0.04, mat(BRASS, rough=0.25, metal=1), bevel=0.01)   # tray
    ball((X, -0.05, 0.97), 0.22, mat("#D8DDE1", rough=0.15, metal=1), scale=(1, 1, 0.8))  # cloche
    ball((X, -0.05, 1.16), 0.04, mat(BRASS, rough=0.25, metal=1))


def diner(skin, sweater, hair_col, style):
    figure(sweater, skin)
    hair = mat(hair_col, rough=0.6)
    if style == "bun":
        ball((0, 0.06, 1.3), 0.41, hair, scale=(1.03, 1.02, 0.7))
        ball((0, 0.12, 1.62), 0.17, hair)
    elif style == "beard":
        ball((0, 0.06, 1.33), 0.41, hair, scale=(1.03, 1.02, 0.6))
        ball((0, -0.25, 1.0), 0.27, hair, scale=(1.1, 0.7, 0.8))
    elif style == "granny":
        ball((0, 0.06, 1.32), 0.42, mat("#E7E4E0", rough=0.7), scale=(1.05, 1.03, 0.68))
        for s in (-1, 1):
            ring((s * 0.13, -0.38, 1.22), 0.07, 0.012, mat(BRASS, metal=1, rough=0.2), rot=(math.pi / 2, 0, 0))
    else:
        ball((0, 0.06, 1.3), 0.42, hair, scale=(1.05, 1.03, 0.66))
        ball((0.25, -0.15, 1.42), 0.17, hair)


# ---------- food ----------
def plate():
    cyl((0, 0, 0.02), 0.95, 0.06, mat("#FFFFFF", rough=0.25, coat=0.6), bevel=0.03)
    ring((0, 0, 0.06), 0.82, 0.03, mat(BRASS, rough=0.3, metal=1))


def pizza():
    plate()
    cyl((0, 0, 0.1), 0.78, 0.07, mat("#E9B36A", rough=0.7), bevel=0.04)
    ring((0, 0, 0.13), 0.74, 0.07, mat("#D9954A", rough=0.7))
    cyl((0, 0, 0.14), 0.68, 0.03, mat("#C8432E", rough=0.5), bevel=0.01)
    cyl((0, 0, 0.16), 0.62, 0.03, mat("#FFD15C", rough=0.4), bevel=0.02)
    for a, r in [(0.3, 0.35), (1.6, 0.42), (2.8, 0.3), (4.1, 0.45), (5.3, 0.33), (0, 0)]:
        cyl((r * math.cos(a), r * math.sin(a), 0.19), 0.11, 0.025, mat("#9E1F1A", rough=0.35), bevel=0.01)
    for a, r in [(0.9, 0.5), (2.2, 0.15), (3.5, 0.52), (4.7, 0.2), (5.9, 0.55)]:
        ball((r * math.cos(a), r * math.sin(a), 0.19), 0.045, mat("#3F7D3A", rough=0.5), scale=(1.6, 1, 0.4))


def burger():
    plate()
    bun = mat("#D98B3A", rough=0.4, coat=0.6)
    cyl((0, 0, 0.17), 0.58, 0.16, bun, bevel=0.06)
    cyl((0, 0, 0.32), 0.6, 0.14, mat("#5A3221", rough=0.75), bevel=0.05)               # patty
    box((0, 0, 0.41), (1.05, 1.05, 0.03), mat("#F4B83A", rough=0.35), rot=(0, 0, math.pi / 4), bevel=0.01)
    ring((0, 0, 0.45), 0.54, 0.06, mat(HERB, rough=0.5), scale=(1, 1, 0.5))           # lettuce
    cyl((0, 0, 0.49), 0.5, 0.05, mat(TOMATO, rough=0.35), bevel=0.02)                  # tomato
    top = ball((0, 0, 0.5), 0.6, bun, scale=(1, 1, 0.62))
    for a, r in [(0.4, 0.3), (1.3, 0.42), (2.1, 0.2), (2.9, 0.38), (3.8, 0.28), (4.6, 0.43), (5.5, 0.25), (0, 0.05)]:
        z = 0.5 + 0.6 * 0.62 * math.sqrt(max(0, 1 - (r / 0.6) ** 2)) + 0.01
        ball((r * math.cos(a), r * math.sin(a), z), 0.035, mat("#FFF3D6", rough=0.5), scale=(1.6, 1, 0.6), rot=(0, 0, a))


def cake():
    plate()
    sponge = mat("#F1D3A1", rough=0.8); cream = mat("#FFF7EE", rough=0.5); jam = mat("#C9364A", rough=0.4)
    ang = math.radians(55)
    rot = -math.pi / 2 - 0.35
    for z0, z1, m in [(0.08, 0.36, sponge), (0.36, 0.42, jam), (0.42, 0.7, sponge), (0.7, 0.82, cream)]:
        w = wedge((0, 0.35, 0), 0.95, ang, z0, z1, m)
        w.rotation_euler = (0, 0, rot)
    ball((-0.12, -0.25, 0.92), 0.09, jam)                                               # cherry
    cyl((-0.1, -0.25, 1.03), 0.008, 0.12, mat("#3F7D3A"), bevel=0, rot=(0.3, 0, 0))


SPRITES = {
    "chef-1": lambda: chef("Marco", SKIN[0], TEAM[0]),
    "chef-2": lambda: chef("Yuki", SKIN[1], TEAM[1]),
    "chef-3": lambda: chef("Kofi", SKIN[3], TEAM[2]),
    "waiter": lambda: waiter(SKIN[1]),
    "diner-1": lambda: diner(SKIN[0], TOMATO, "#B5482A", "plain"),
    "diner-2": lambda: diner(SKIN[0], LILAC, "#E7E4E0", "granny"),
    "pizza": pizza,
    "burger": burger,
    "cake": cake,
}
FOOD = {"pizza", "burger", "cake"}


# ---------- scene ----------
def setup():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.render.film_transparent = True
    sc.render.resolution_x = sc.render.resolution_y = SIZE
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = hexc("#2A2420")
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.35

    def area(name, loc, energy, color, size):
        d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.color = hexc(color)[:3]; d.size = size
        o = bpy.data.objects.new(name, d); o.location = loc
        sc.collection.objects.link(o)
        t = o.constraints.new("TRACK_TO"); t.target = target; t.track_axis = "TRACK_NEGATIVE_Z"; t.up_axis = "UP_Y"

    global target
    target = bpy.data.objects.new("target", None); sc.collection.objects.link(target)
    area("key", (-3, -4, 5), 650, "#FFF1DE", 3)                # warm key, front-left
    area("fill", (4, -2, 2), 160, "#BFD4FF", 4)                # cool fill
    area("rim", (1.5, 4, 3), 1200, NEON, 2)                    # neon rim from behind
    cam_d = bpy.data.cameras.new("cam"); cam_d.type = "ORTHO"
    cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
    t = cam.constraints.new("TRACK_TO"); t.target = target; t.track_axis = "TRACK_NEGATIVE_Z"; t.up_axis = "UP_Y"
    return sc, cam


def render(name, sc, cam):
    global COLL
    COLL = bpy.data.collections.new(name); sc.collection.children.link(COLL)
    SPRITES[name]()
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in COLL.objects for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    mid = (lo + hi) / 2
    target.location = mid
    elev = math.radians(42 if name in FOOD else 14)        # food seen from above, people nearly face-on
    azim = math.radians(-18)
    d = 12
    cam.location = mid + Vector((d * math.cos(elev) * math.sin(azim), -d * math.cos(elev) * math.cos(azim), d * math.sin(elev)))
    span = max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z)
    cam.data.ortho_scale = span * 1.12
    sc.render.filepath = f"{OUT}/{name}.png"
    bpy.ops.render.render(write_still=True)
    for o in list(COLL.objects):
        bpy.data.objects.remove(o)
    bpy.data.collections.remove(COLL)


def main():
    names = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    names = names or list(SPRITES)
    os.makedirs(OUT, exist_ok=True)
    sc, cam = setup()
    for n in names:
        render(n, sc, cam)
        print("rendered", n, flush=True)


main()
