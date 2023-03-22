import bpy
from math import pi

bpy.ops.preferences.addon_enable(module="add_mesh_extra_objects")
from mathutils import Color 

# delete all previous objects and meshes

def reset_blend():

    for collection in bpy.data.collections:
        for obj in collection.objects:
            collection.objects.unlink(obj)

    for bpy_data_iter in (
            bpy.data.objects,
            bpy.data.meshes,
            bpy.data.lights,
            bpy.data.cameras,
            bpy.data.materials,
            bpy.data.textures,
            bpy.data.particles,
            ):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)

reset_blend()

# cursor to center
bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    
# add surface
# bpy.ops.mesh.primitive_xyz_function_surface(x_eq="cos(u)*sin(v)",
#                                             y_eq="sin(u)*sin(v)",
#                                             z_eq="cos(v)+log(tan(v/2)+0.01)+0.2*u", 
#                                             range_u_min=0, 
#                                             range_u_max=4*pi,
#                                             range_u_step=256, 
#                                             wrap_u = False,
#                                             range_v_min=0.1, 
#                                             range_v_max=2,
#                                             range_v_step=128, 
#                                             wrap_v = False)
bpy.ops.mesh.primitive_gem_add()
bpy.context.object.name = 'surface'
surface = bpy.data.objects['surface']

# add material for surface
bpy.ops.material.new()
surf_mat = bpy.data.materials['Material']
# surf_mat.diffuse_color = Color([x/255 for x in (255,143,0)])
# surf_mat.diffuse_intensity = 1
surf_mat.specular_intensity = 1
# surf_mat.specular_hardness = 30
# surf_mat.raytrace_mirror.use = True
# surf_mat.raytrace_mirror.reflect_factor = 0.3
# surface.data.materials.append(surf_mat)

# add lamps
for i in [-10, 10]:
    for j in [-10, 10]:
        for k in [-10, 10]:
            bpy.ops.object.light_add(type='POINT', location=(i,j,k))

for light in bpy.data.lights:
    light.energy = 2.0

# add camera
bpy.ops.object.camera_add(location=(15,0,0), rotation=(pi/2,0,pi/2))
bpy.context.object.name = 'camera'
camera = bpy.data.objects['camera']

# add empty to control camera position
bpy.ops.object.empty_add(type='PLAIN_AXES')
bpy.context.object.name = 'empty'
empty = bpy.data.objects['empty']

# parent the camera to the empty
camera.parent = empty

# rotate empty
empty.rotation_euler = (0,0,0)
empty.keyframe_insert(data_path='rotation_euler', frame=11)
empty.rotation_euler = (0,0,2*pi)
empty.keyframe_insert(data_path='rotation_euler', frame=261)

# add sky 
# def add_sky():
#     # bpy.context.scene.world.use_sky_blend = True
#     # bpy.context.scene.world.use_sky_real = True
#     # bpy.context.scene.world.zenith_color = (0.00, 0.00, 0.00)
#     # bpy.context.scene.world.horizon_color = (0.01, 0.01, 0.02)

# add_sky()

# render image
bpy.context.scene.camera = camera
bpy.context.scene.frame_end = 271
bpy.data.scenes['Scene'].render.resolution_x = 3840
bpy.data.scenes['Scene'].render.resolution_y = 2160

mode = 'video'

if mode == 'image':
    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.data.scenes['Scene'].render.filepath = '/tmp/dini.jpg'
    bpy.ops.render.render(animation=False,write_still=True)
elif mode == 'video':
    bpy.context.scene.render.image_settings.file_format = 'AVI_JPEG'
    bpy.data.scenes['Scene'].render.filepath = '/tmp/dini.avi'
    bpy.ops.render.render(animation=True)




