import bpy
from math import pi

from utils.nodes.material import node_material, location, emission, as_surface
from utils.nodes.script import osl_script
from utils.nodes.math import value
from utils.render import render

# set render engine to CYCLES and enable Open Shading Language
scn = bpy.context.scene
scn.render.engine = 'CYCLES'
scn.cycles.shading_system = True

objs = bpy.data.objects
objs.remove(objs["Cube"], do_unlink=True)
objs.remove(objs["Light"], do_unlink=True)
    
bpy.ops.mesh.primitive_plane_add()
plane = bpy.data.objects['Plane']
plane.scale = (4, 4, 1)

# # add material for cube
julia_mat = node_material()

location = location()

(color, ) = osl_script('fractal/julia', location)

strength = value(1)
ems = emission(color, strength)

as_surface(ems)

plane.data.materials.append(julia_mat)

# camera
camera = bpy.data.objects['Camera']
camera.location = (0,0,10)
camera.rotation_euler = (0,0,0)

# render image
bpy.context.scene.camera = camera
bpy.context.scene.frame_end = 200

render('julia', 0.2, True)
        