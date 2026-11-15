import bpy, addon_utils
print("addons:", [m for m in bpy.context.preferences.addons.keys() if 'vrm' in m.lower()])
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
r = bpy.ops.import_scene.vrm(filepath="/work/vrm/pixiv-sample.vrm")
print("import:", r)
for o in bpy.data.objects: print("OBJ", o.type, o.name, [round(v,2) for v in o.dimensions])
arm = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
print("BONES", len(arm.data.bones), [b.name for b in arm.data.bones][:60])
for m in bpy.data.materials: print("MAT", m.name)
hb = arm.data.vrm_addon_extension.vrm1.humanoid.human_bones
for k in ["head","neck","left_upper_arm","left_lower_arm","left_hand","right_upper_arm","right_lower_arm","right_hand","spine","chest","hips"]:
    print("HB", k, getattr(hb, k).node.bone_name)
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE_NEXT'
sc.render.resolution_x = sc.render.resolution_y = 256; sc.render.film_transparent = True
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0, -3, 1.0); cam.rotation_euler = (1.5708, 0, 0)
sc.render.filepath = "/work/vrm/probe.png"
bpy.ops.render.render(write_still=True); print("EEVEE OK")
