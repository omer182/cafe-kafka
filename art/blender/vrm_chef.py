"""Turn a VRoid / VRM character into a Café Kafka chef and render cel-shaded sprites.

  docker run --rm -v "$PWD/art":/work cafe-blender:4.2.3-vrm --python /work/blender/vrm_chef.py -- \
      /work/vrm/pixiv-sample.vrm yuki '#E4573D'

Args: <vrm file> <name> <neckerchief colour>. Writes art/sprites/<name>.png (full body)
and art/sprites/<name>-portrait.png (bust).
"""
import math
import sys
import bpy
import bmesh
from mathutils import Vector, Matrix

args = sys.argv[sys.argv.index("--") + 1:]
VRM, NAME, SCARF = args[0], args[1], args[2]
OUT = "/work/sprites"


def hexc(h):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb) + (1.0,)


# ---------- scene + import ----------
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
bpy.ops.import_scene.vrm(filepath=VRM)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = bpy.data.objects["Body"]
hb = arm.data.vrm_addon_extension.vrm1.humanoid.human_bones
B = lambda k: getattr(hb, k).node.bone_name
sc = bpy.context.scene
dg = lambda: bpy.context.evaluated_depsgraph_get()


# ---------- cel material + outline for the props ----------
def toon(color, shade, name):
    """Two-tone cel shading: diffuse -> Shader to RGB -> hard ramp -> emission."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; n = nt.nodes; L = nt.links
    for x in list(n):
        n.remove(x)
    out = n.new("ShaderNodeOutputMaterial")
    dif = n.new("ShaderNodeBsdfDiffuse"); dif.inputs["Color"].default_value = (1, 1, 1, 1)
    s2r = n.new("ShaderNodeShaderToRGB")
    ramp = n.new("ShaderNodeValToRGB"); ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].color = hexc(shade)
    ramp.color_ramp.elements[1].position = 0.5
    ramp.color_ramp.elements[1].color = hexc(color)
    em = n.new("ShaderNodeEmission")
    L.new(dif.outputs[0], s2r.inputs[0]); L.new(s2r.outputs["Color"], ramp.inputs[0])
    L.new(ramp.outputs[0], em.inputs[0]); L.new(em.outputs[0], out.inputs[0])
    return m


OUTLINE = bpy.data.materials.new("prop-outline"); OUTLINE.use_nodes = True
_n = OUTLINE.node_tree.nodes; _n.remove(_n["Principled BSDF"])
_e = _n.new("ShaderNodeEmission"); _e.inputs[0].default_value = hexc("#3B2A2A")
OUTLINE.node_tree.links.new(_e.outputs[0], _n["Material Output"].inputs[0])
OUTLINE.use_backface_culling = True


def finish(o, m, outline=0.006, smooth=True):
    o.data.materials.append(m); o.data.materials.append(OUTLINE)
    if smooth:
        for p in o.data.polygons:
            p.use_smooth = True
    if outline:                                  # inverted-hull outline, the classic anime trick
        s = o.modifiers.new("outline", "SOLIDIFY"); s.thickness = outline; s.offset = 1
        s.use_flip_normals = True; s.material_offset = 1
    return o


def parent_to_bone(o, bone):
    mw = o.matrix_world.copy()
    o.parent = arm; o.parent_type = "BONE"; o.parent_bone = bone
    bpy.context.view_layer.update()
    o.matrix_world = mw


def prim(kind, **kw):
    getattr(bpy.ops.mesh, f"primitive_{kind}_add")(**kw)
    return bpy.context.object


# ---------- measure the body in rest pose ----------
bpy.context.view_layer.update()
ev = body.evaluated_get(dg()); me = ev.to_mesh()
verts = [body.matrix_world @ v.co for v in me.vertices]
ev.to_mesh_clear()


def front_y(z, half_w):
    ys = [v.y for v in verts if abs(v.z - z) < 0.015 and abs(v.x) < half_w]
    return min(ys) if ys else None


hair = bpy.data.objects["Hair"]
hair_top = max((hair.matrix_world @ Vector(c)).z for c in hair.bound_box)
head_bone = arm.data.bones[B("head")]
head_c = arm.matrix_world @ head_bone.head_local

WHITE = toon("#FFFFFF", "#D9DCE6", "toque")
NAVY = toon("#2C3550", "#1B2135", "apron")
RED = toon(SCARF, "#9E2A22", "scarf")
STEEL = toon("#4A4F57", "#25282D", "pan")
BRASS = toon("#E3B04B", "#A77A28", "brass")
NOODLE = toon("#F2C46B", "#C98E3A", "noodle")
GREEN = toon("#7FB069", "#4F7F3D", "veg")

# ---------- apron: follows the torso front, bib + skirt ----------
rows = [(1.27, 0.085), (1.16, 0.10), (1.04, 0.15), (0.98, 0.17), (0.9, 0.175), (0.8, 0.18), (0.7, 0.185), (0.62, 0.185)]
bm = bmesh.new(); grid = []
for z, w in rows:
    y = front_y(z, max(w, 0.16)) or front_y(z, 0.2)
    y = (y if y is not None else -0.12) - 0.03
    row = []
    for i in range(7):
        x = -w + 2 * w * i / 6
        row.append(bm.verts.new((x, y + abs(x / w) ** 2 * 0.05, z)))   # wrap slightly around the sides
    grid.append(row)
for r in range(len(grid) - 1):
    for i in range(6):
        bm.faces.new((grid[r][i], grid[r][i + 1], grid[r + 1][i + 1], grid[r + 1][i]))
apron_me = bpy.data.meshes.new("apron"); bm.to_mesh(apron_me); bm.free()
apron = bpy.data.objects.new("apron", apron_me); sc.collection.objects.link(apron)
sol = apron.modifiers.new("thick", "SOLIDIFY"); sol.thickness = 0.008
finish(apron, NAVY, outline=0.004)
parent_to_bone(apron, B("hips"))

# ---------- neckerchief ----------
neck = arm.matrix_world @ arm.data.bones[B("neck")].head_local
scarf = prim("torus", major_radius=0.055, minor_radius=0.014, location=(neck.x, neck.y - 0.005, neck.z - 0.01))
scarf.scale = (1.05, 1.0, 0.8)
finish(scarf, RED, outline=0.003)
knot = prim("cone", radius1=0.03, radius2=0.0, depth=0.06, location=(neck.x, neck.y - 0.06, neck.z - 0.04), rotation=(math.pi, 0, 0))
finish(knot, RED, outline=0.003)
for o in (scarf, knot):
    parent_to_bone(o, B("neck"))

# ---------- toque on top of the hair ----------
hat_parts = []
band = prim("cylinder", vertices=48, radius=0.105, depth=0.07, location=(head_c.x, head_c.y + 0.01, hair_top - 0.035))
band.rotation_euler = (math.radians(-8), 0, 0)
hat_parts.append(finish(band, WHITE, outline=0.004))
for dx, dy, dz, r in [(0, 0, 0.09, 0.105), (-0.07, 0.01, 0.07, 0.075), (0.07, 0.01, 0.07, 0.075), (0, 0.06, 0.075, 0.08), (0, -0.05, 0.07, 0.075)]:
    p = prim("uv_sphere", segments=32, ring_count=16, radius=r, location=(head_c.x + dx, head_c.y + 0.01 + dy, hair_top - 0.035 + dz))
    hat_parts.append(finish(p, WHITE, outline=0.004))
for p in hat_parts:
    parent_to_bone(p, B("head"))

# ---------- pose: from T-pose to holding a pan and a ladle ----------
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")


def aim(key, direction):
    """Rotate a pose bone so it points along `direction` (armature space)."""
    pb = arm.pose.bones[B(key)]
    bpy.context.view_layer.update()
    head = pb.head.copy()
    cur = (pb.tail - pb.head).normalized()
    q = cur.rotation_difference(Vector(direction).normalized())
    pb.matrix = Matrix.Translation(head) @ q.to_matrix().to_4x4() @ Matrix.Translation(-head) @ pb.matrix
    bpy.context.view_layer.update()


# The character faces -Y. Her right side is -X.
aim("right_upper_arm", (-0.28, -0.32, -1))      # pan arm: elbow tucked, forearm out front
aim("right_lower_arm", (-0.1, -1, 0.05))
aim("left_upper_arm", (0.3, -0.15, -1))         # ladle arm: forearm raised
aim("left_lower_arm", (0.05, -0.75, 0.9))
aim("head", (0.08, -0.12, 1))                   # slight head tilt


def curl(side, amount):
    """Bend every finger joint toward the palm."""
    for f in ("index", "middle", "ring", "little"):
        for j in ("proximal", "intermediate", "distal"):
            try:
                pb = arm.pose.bones[B(f"{side}_{f}_{j}")]
            except Exception:
                continue
            pb.rotation_mode = "XYZ"
            pb.rotation_euler = (0, 0, math.radians(amount if side == "left" else -amount))
    for j, a in (("proximal", 25), ("distal", 30)):
        try:
            pb = arm.pose.bones[B(f"{side}_thumb_{j}")]
            pb.rotation_mode = "XYZ"; pb.rotation_euler = (0, math.radians(a if side == "left" else -a), 0)
        except Exception:
            pass


curl("left", 75)
curl("right", 75)
bpy.ops.object.mode_set(mode="OBJECT")

# happy face from the model's own expressions
try:
    ex = arm.data.vrm_addon_extension.vrm1.expressions.preset
    ex.happy.preview = 0.4
except Exception as e:
    print("no expression preview:", e)

bpy.context.view_layer.update()
rh = arm.matrix_world @ arm.pose.bones[B("right_hand")].tail
lhb = arm.pose.bones[B("left_hand")]
lh = arm.matrix_world @ (lhb.head * 0.35 + lhb.tail * 0.65)

# ---------- props in the hands ----------
pan = prim("cylinder", vertices=48, radius=0.12, depth=0.035, location=(rh.x - 0.02, rh.y - 0.19, rh.z + 0.005))
finish(pan, STEEL, outline=0.004)
handle = prim("cylinder", vertices=16, radius=0.012, depth=0.16, location=(rh.x - 0.01, rh.y - 0.05, rh.z + 0.005), rotation=(math.pi / 2, 0, 0))
finish(handle, STEEL, outline=0.003)
for i, (dx, dy, r) in enumerate([(0, 0, 0.07), (-0.04, 0.03, 0.05), (0.045, -0.02, 0.05), (0.02, 0.05, 0.04)]):
    nd = prim("uv_sphere", segments=24, ring_count=12, radius=r, location=(rh.x - 0.02 + dx, rh.y - 0.19 + dy, rh.z + 0.04))
    nd.scale = (1, 1, 0.45)
    finish(nd, NOODLE if i else NOODLE, outline=0.003)
for dx, dy in [(-0.05, -0.04), (0.03, 0.04), (0.06, -0.05)]:
    v = prim("uv_sphere", segments=16, ring_count=8, radius=0.018, location=(rh.x - 0.02 + dx, rh.y - 0.19 + dy, rh.z + 0.065))
    finish(v, GREEN, outline=0.002)
lad_stick = prim("cylinder", vertices=16, radius=0.007, depth=0.26, location=(lh.x, lh.y - 0.015, lh.z + 0.08))
finish(lad_stick, BRASS, outline=0.003)
lad_cup = prim("uv_sphere", segments=24, ring_count=12, radius=0.03, location=(lh.x, lh.y - 0.015, lh.z + 0.215))
finish(lad_cup, BRASS, outline=0.003)

# ---------- light, camera, render ----------
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sc.collection.objects.link(sun)
sun.data.energy = 3.0; sun.rotation_euler = (math.radians(50), math.radians(-20), math.radians(-35))
sc.world = sc.world or bpy.data.worlds.new("w")
sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.6, 0.6, 0.62, 1)
sc.render.engine = "BLENDER_EEVEE_NEXT"
sc.render.film_transparent = True
sc.view_settings.view_transform = "Standard"
sc.render.image_settings.color_mode = "RGBA"

cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = "ORTHO"


def shoot(path, center, scale, res, az=-22, el=6):
    a, e = math.radians(az), math.radians(el)
    d = 6
    cam.location = Vector(center) + Vector((d * math.cos(e) * math.sin(a), -d * math.cos(e) * math.cos(a), d * math.sin(e)))
    cam.rotation_euler = (Vector(center) - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.ortho_scale = scale
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("rendered", path, flush=True)


top = hair_top + 0.2
shoot(f"{OUT}/{NAME}.png", (0, 0, top / 2), top * 1.06, (512, 512))
shoot(f"{OUT}/{NAME}-portrait.png", (head_c.x, head_c.y, head_c.z + 0.02), 0.62, (768, 768), az=-18, el=3)
