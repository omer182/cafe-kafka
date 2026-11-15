"""Café Kafka chef from a VRoid / VRM model: bob haircut, chef whites, pleated toque,
crossed arms. Renders a cel-shaded portrait, a full-body sprite and a cut-in bust.

  docker run --rm -v "$PWD/art":/work cafe-blender:4.2.3-vrm --python /work/blender/chef_hero.py -- \
      /work/vrm/pixiv-sample.vrm yuki '#E4573D' '#17161C'

Args: <vrm> <name> <team colour> <hair colour>
"""
import math
import sys
import bpy
import bmesh
from mathutils import Vector, Matrix

args = sys.argv[sys.argv.index("--") + 1:]
VRM, NAME, TEAM, HAIR = args[0], args[1], args[2], args[3]
OUT = "/work/sprites"


def lin(h):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb)


for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
bpy.ops.import_scene.vrm(filepath=VRM)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
hb = arm.data.vrm_addon_extension.vrm1.humanoid.human_bones
B = lambda k: getattr(hb, k).node.bone_name
sc = bpy.context.scene
body, hair = bpy.data.objects["Body"], bpy.data.objects["Hair"]
head_c = arm.data.bones[B("head")].head_local.copy()

# ---------------- hair: short black bob ----------------
CUT = head_c.z - 0.07          # just under the jaw


def cut_below(obj, z, only_mat=None):
    bm = bmesh.new(); bm.from_mesh(obj.data)
    idx = {m.name: i for i, m in enumerate(obj.data.materials)}
    kill = [f for f in bm.faces
            if (only_mat is None or f.material_index == idx[only_mat])
            and min((obj.matrix_world @ v.co).z for v in f.verts) < z]
    bmesh.ops.delete(bm, geom=kill, context="FACES")
    bm.to_mesh(obj.data); bm.free()


cut_below(hair, CUT)
cut_below(body, CUT + 0.02, "HairBack_00_HAIR")
for mn in ("Hair_00_HAIR", "HairBack_00_HAIR"):
    m = bpy.data.materials[mn].vrm_addon_extension.mtoon1
    m.pbr_metallic_roughness.base_color_factor = (*lin(HAIR), 1)
    m.extensions.vrmc_materials_mtoon.shade_color_factor = tuple(c * 0.55 for c in lin(HAIR))
    m.extensions.vrmc_materials_mtoon.parametric_rim_color_factor = lin("#3A4E7A")   # blue-black sheen

# warm amber eyes like the reference
try:
    e = bpy.data.materials["EyeIris_00_EYE"].vrm_addon_extension.mtoon1
    e.pbr_metallic_roughness.base_color_factor = (*lin("#E8B04A"), 1)
except Exception as ex:
    print("eye tint skipped", ex)

# ---------------- materials for the outfit ----------------
CLOTH = bpy.data.materials["Tops_01_CLOTH"]          # the model's own white cel cloth


def toon(color, shade, name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    n = m.node_tree.nodes; L = m.node_tree.links
    for x in list(n):
        n.remove(x)
    out = n.new("ShaderNodeOutputMaterial"); dif = n.new("ShaderNodeBsdfDiffuse")
    s2r = n.new("ShaderNodeShaderToRGB"); ramp = n.new("ShaderNodeValToRGB"); em = n.new("ShaderNodeEmission")
    ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].color = (*lin(shade), 1)
    ramp.color_ramp.elements[1].position = 0.45
    ramp.color_ramp.elements[1].color = (*lin(color), 1)
    L.new(dif.outputs[0], s2r.inputs[0]); L.new(s2r.outputs["Color"], ramp.inputs[0])
    L.new(ramp.outputs[0], em.inputs[0]); L.new(em.outputs[0], out.inputs[0])
    return m


WHITE = toon("#FFFFFF", "#C9CEDC", "whites")
BUTTON = toon("#9AA3AE", "#5C636C", "buttons")
TEAMM = toon(TEAM, "#8E2A22", "team")
OUTLINE = bpy.data.materials.new("ink"); OUTLINE.use_nodes = True
_n = OUTLINE.node_tree.nodes; _n.remove(_n["Principled BSDF"])
_e = _n.new("ShaderNodeEmission"); _e.inputs[0].default_value = (*lin("#2E2226"), 1)
OUTLINE.node_tree.links.new(_e.outputs[0], _n["Material Output"].inputs[0])
OUTLINE.use_backface_culling = True


def finish(o, m, outline=0.004):
    o.data.materials.append(m); o.data.materials.append(OUTLINE)
    for p in o.data.polygons:
        p.use_smooth = True
    if outline:
        s = o.modifiers.new("ink", "SOLIDIFY"); s.thickness = outline; s.offset = 1
        s.use_flip_normals = True; s.material_offset = 1
    return o


def attach(o, bone):
    bpy.context.view_layer.update()            # make matrix_world reflect location/rotation first
    mw = o.matrix_world.copy()
    o.parent = arm; o.parent_type = "BONE"; o.parent_bone = B(bone)
    bpy.context.view_layer.update(); o.matrix_world = mw


def lathe(name, profile, pleats=0, amp=0.0, segs=96):
    """Revolve (z, r) around Z. Optional pleats ripple the radius."""
    bm = bmesh.new(); rings = []
    for z, r in profile:
        ring = []
        for i in range(segs):
            a = 2 * math.pi * i / segs
            rr = r * (1 + (amp * math.cos(pleats * a) if pleats and r > 0.02 else 0))
            ring.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), z)))
        rings.append(ring)
    for r0, r1 in zip(rings, rings[1:]):
        for i in range(segs):
            j = (i + 1) % segs
            bm.faces.new((r0[i], r0[j], r1[j], r1[i]))
    bm.faces.new(rings[0][::-1])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    return o


def tube(name, p0, p1, r0, r1, m, outline=0.004):
    """Tapered sleeve from p0 to p1 (world)."""
    p0, p1 = Vector(p0), Vector(p1)
    o = lathe(name, [(0, r0), (1, r1)], segs=40)
    o.data.polygons[-1].use_smooth = True
    d = p1 - p0
    o.matrix_world = Matrix.Translation(p0) @ d.to_track_quat("Z", "Y").to_matrix().to_4x4() @ Matrix.Diagonal((1, 1, d.length, 1))
    return finish(o, m, outline)


def ball(name, p, r, m, outline=0.003):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=r, location=p)
    o = bpy.context.object; o.name = name
    return finish(o, m, outline)


# ---------------- body front profile (rest pose) for buttons + apron ----------------
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
ev = body.evaluated_get(dg); me = ev.to_mesh()
verts = [body.matrix_world @ v.co for v in me.vertices]
ev.to_mesh_clear()


def front_y(z, half_w=0.0, band=0.0, x=0.0):
    """Where the body surface is, looking from the front at (x, z)."""
    ok, loc, *_ = body.ray_cast(Vector((x, -2, z)), Vector((0, 1, 0)))
    return loc.y if ok else None


hair_top = max((hair.matrix_world @ Vector(c)).z for c in hair.bound_box)

# pleated toque
toque = lathe("toque", [(0, 0.101), (0.045, 0.102), (0.07, 0.108), (0.11, 0.126), (0.15, 0.146), (0.19, 0.16),
                        (0.22, 0.162), (0.245, 0.152), (0.265, 0.126), (0.278, 0.09), (0.285, 0.05), (0.2875, 0.02)],
              pleats=12, amp=0.07)
toque.location = (head_c.x, head_c.y + 0.012, hair_top - 0.085)
toque.rotation_euler = (math.radians(-10), math.radians(4), 0)
toque.scale = (0.86, 0.86, 0.78)
finish(toque, WHITE, 0.005)
band = lathe("band", [(0, 0.106), (0.05, 0.106)], segs=64)
band.location = toque.location; band.rotation_euler = toque.rotation_euler; band.scale = (0.86, 0.86, 0.8)
finish(band, WHITE, 0.004)
for o in (toque, band):
    attach(o, "head")

# stand collar + double-breasted buttons + team-colour piping on the collar
neck = arm.data.bones[B("neck")].head_local
collar = lathe("collar", [(0, 0.074), (0.05, 0.064)], segs=64)
collar.location = (neck.x, neck.y - 0.012, neck.z - 0.04)
collar.rotation_euler = (math.radians(-12), 0, 0)
finish(collar, WHITE, 0.003); attach(collar, "upper_chest")
pipe = lathe("pipe", [(0, 0.0655), (0.007, 0.0645)], segs=64)
pipe.location = (neck.x, neck.y - 0.012 - 0.01, neck.z + 0.006)
pipe.rotation_euler = (math.radians(-12), 0, 0)
finish(pipe, TEAMM, 0.002); attach(pipe, "upper_chest")
for z in (1.235, 1.17):
    for s in (-1, 1):
        fy = front_y(z, x=s * 0.05)
        b = ball(f"btn{z}{s}", (s * 0.05, (fy if fy is not None else -0.1) - 0.003, z), 0.011, BUTTON, 0.002)
        attach(b, "upper_chest")

# long white waist apron with a team-colour waistband
rows = [(0.99, 0.19), (0.9, 0.2), (0.8, 0.205), (0.7, 0.21), (0.6, 0.215), (0.5, 0.22), (0.42, 0.225)]
bm = bmesh.new(); grid = []
for z, w in rows:
    row, prev = [], None
    for i in range(17):
        xx = -w + 2 * w * i / 16
        fy = front_y(z, x=xx * 0.85)
        fy = fy if fy is not None else (prev if prev is not None else -0.08)
        prev = fy
        depth = (0.99 - z) / 0.57                                  # 0 at the waist, 1 at the hem
        fold = 0.016 * depth * math.sin(xx * 24 + 0.6)
        row.append(bm.verts.new((xx, min(fy, -0.06) - 0.035 - 0.03 * depth + fold + (abs(xx) / w) ** 3 * 0.09, z)))
    grid.append(row)
for r in range(len(grid) - 1):
    for i in range(16):
        bm.faces.new((grid[r][i], grid[r][i + 1], grid[r + 1][i + 1], grid[r + 1][i]))
ame = bpy.data.meshes.new("apron"); bm.to_mesh(ame); bm.free()
apron = bpy.data.objects.new("apron", ame); sc.collection.objects.link(apron)
apron.modifiers.new("t", "SOLIDIFY").thickness = 0.006
finish(apron, WHITE, 0.004); attach(apron, "hips")
wb = lathe("waistband", [(0, 0.165), (0.03, 0.163)], segs=64)
wb.location = (0, -0.02, 0.975); wb.scale = (1.05, 0.78, 1)
finish(wb, TEAMM, 0.003); attach(wb, "hips")

# ---------------- pose: arms crossed, slight head tilt ----------------
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")


def aim(key, d):
    pb = arm.pose.bones[B(key)]
    bpy.context.view_layer.update()
    h = pb.head.copy()
    q = (pb.tail - pb.head).normalized().rotation_difference(Vector(d).normalized())
    pb.matrix = Matrix.Translation(h) @ q.to_matrix().to_4x4() @ Matrix.Translation(-h) @ pb.matrix
    bpy.context.view_layer.update()


# She faces -Y; her right side is -X.
aim("right_upper_arm", (-0.16, -0.5, -1))
aim("right_lower_arm", (1, -0.28, 0.28))
aim("left_upper_arm", (0.16, -0.62, -1))
aim("left_lower_arm", (-1, -0.55, 0.36))
aim("right_hand", (0.6, 0.2, 0.2))
aim("left_hand", (-0.6, 0.3, -0.1))
aim("head", (0.1, -0.08, 1))
for side in ("left", "right"):
    for f in ("index", "middle", "ring", "little"):
        for j in ("proximal", "intermediate", "distal"):
            try:
                pb = arm.pose.bones[B(f"{side}_{f}_{j}")]
                pb.rotation_mode = "XYZ"; pb.rotation_euler = (0, 0, math.radians(35 if side == "left" else -35))
            except Exception:
                pass
bpy.ops.object.mode_set(mode="OBJECT")
ex = arm.data.vrm_addon_extension.vrm1.expressions.preset
ex.happy.preview = 0.22
ex.relaxed.preview = 0.15
bpy.context.view_layer.update()

# ---------------- long sleeves + trousers follow the posed bones ----------------
P = lambda k, end="head": arm.matrix_world @ getattr(arm.pose.bones[B(k)], end)
for s in ("left", "right"):
    sh, el, wr = P(f"{s}_upper_arm"), P(f"{s}_lower_arm"), P(f"{s}_hand")
    attach(tube(f"{s}-upper", sh, el, 0.058, 0.046, WHITE), f"{s}_upper_arm")
    attach(ball(f"{s}-elbow", el, 0.046, WHITE), f"{s}_lower_arm")
    attach(tube(f"{s}-lower", el, wr, 0.046, 0.042, WHITE), f"{s}_lower_arm")
    cuff = wr + (wr - el).normalized() * -0.012
    attach(tube(f"{s}-cuff", cuff, wr + (wr - el).normalized() * 0.006, 0.045, 0.045, WHITE), f"{s}_lower_arm")
    hip, knee, ank = P(f"{s}_upper_leg"), P(f"{s}_lower_leg"), P(f"{s}_foot")
    attach(tube(f"{s}-thigh", hip + Vector((0, 0, 0.05)), knee, 0.092, 0.066, WHITE), f"{s}_upper_leg")
    attach(tube(f"{s}-shin", knee, ank + Vector((0, 0, 0.02)), 0.066, 0.056, WHITE), f"{s}_lower_leg")

# ---------------- light + cameras ----------------
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sc.collection.objects.link(sun)
sun.data.energy = 3.0
sun.rotation_euler = Vector((-0.7, -1.0, 1.2)).to_track_quat("Z", "Y").to_euler()   # light from her right-front, above
sc.world = sc.world or bpy.data.worlds.new("w"); sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.42, 0.43, 0.48, 1)
sc.render.engine = "BLENDER_EEVEE_NEXT"; sc.render.film_transparent = True
sc.view_settings.view_transform = "Standard"; sc.render.image_settings.color_mode = "RGBA"
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = "ORTHO"


def shoot(path, center, scale, res, az=-20, el=4):
    a, e = math.radians(az), math.radians(el)
    cam.location = Vector(center) + 6 * Vector((math.cos(e) * math.sin(a), -math.cos(e) * math.cos(a), math.sin(e)))
    cam.rotation_euler = (Vector(center) - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.ortho_scale = scale
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("rendered", path, flush=True)


only = args[4:] or ["portrait", "full", "bust"]
if "debug" in only:
    bpy.context.view_layer.update()
    for n in ("toque", "band", "collar", "apron", "waistband", "btn1.235-1"):
        o = bpy.data.objects.get(n)
        if o is None: print("DBG", n, "MISSING"); continue
        ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
        print("DBG", n, "hide", o.hide_render, "z", round(min(w.z for w in ws), 3), round(max(w.z for w in ws), 3),
              "y", round(min(w.y for w in ws), 3), "x", round(min(w.x for w in ws), 3), round(max(w.x for w in ws), 3), "mats", [m.name for m in o.data.materials])
    print("DBG hair_top", round(hair_top, 3), "CUT", round(CUT, 3))
top = hair_top + 0.22
if "portrait" in only:   # thigh-up, like the reference
    shoot(f"{OUT}/{NAME}-hero.png", (0, 0, (top + 0.6) / 2), (top - 0.6) * 1.05, (600, 900))
if "full" in only:
    shoot(f"{OUT}/{NAME}.png", (0, 0, top / 2), top * 1.04, (512, 512))
if "bust" in only:       # for the manga cut-in panel
    shoot(f"{OUT}/{NAME}-bust.png", (head_c.x, head_c.y, head_c.z - 0.05), 0.75, (768, 768), az=-16, el=3)
