import bpy
from math import pi

from utils.nodes.color import hue_ramp
from utils.nodes.material import emission, as_volume, location, node_material, plain_emission, as_surface
from utils.nodes.script import osl_script, inn_script
from utils.nodes.time import time
from utils.nodes.math import polar, multiply_by, multiply, fract, value
from utils.nodes.anim import anim
from utils.render import render
from utils.sky import colorSky

# set render engine to CYCLES and enable Open Shading Language
scn = bpy.context.scene
scn.render.engine = 'CYCLES'
scn.cycles.shading_system = True
    
cube = bpy.data.objects['Cube']
cube.scale = (4, 4, 4)

# add material for cube
orbital_mat = node_material()

location = location()
time = time(200, 0.05)

n = value(3)
l = value(2)
m = value(1)
re, im = osl_script('orbital/orb', n, l, m, location, time)
r, phi = polar(re, im)
norm_phi = multiply_by(phi, 1 / (2*pi))
hue = fract(norm_phi)
color = hue_ramp(hue)

s = '''
shader ylayer(
    float ythr = 0.0,
    float scale = 1,
    vector Position = vector(0, 0, 0),
    output float yfac = 0.5)
{
    float y = Position[1] / scale;
    if ( y < ythr - 0.1 ){ yfac = 2; }
    if ( ythr - 0.1 <= y && y < ythr + 0.1 ){ yfac = 10; }
    if ( y > ythr + 0.1 ){ yfac = 0.0; }
}
'''

ythr = value(-1.2)
yscale = value(4)
(yfac, ) = inn_script(s, ythr, yscale, location)

strength = multiply(r, yfac)
ems = emission(color, strength)

as_volume(ems)

cube.data.materials.append(orbital_mat)

bpy.context.scene.cursor.location = (0.0, -4.0, 0.0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

bpy.ops.object.empty_add(type='PLAIN_AXES')
bpy.context.object.name = 'y_empty'
y_empty = bpy.data.objects['y_empty']

d = cube.driver_add( 'scale', 1 ).driver
v = d.variables.new()
v.name                 = 'pos'
v.targets[0].id        = y_empty
v.targets[0].data_path = 'location.y'

d.expression = 'pos + 4'

bpy.context.view_layer.objects.active = cube
print(bpy.context.active_object)

bpy.ops.object.duplicate()
wcube = bpy.context.object
bpy.ops.object.modifier_add(type='WIREFRAME')
bpy.context.object.modifiers["Wireframe"].thickness = 0.02

wireframe_mat = node_material()
ems = plain_emission((1,1,1,1), 20)
as_volume(ems)

wcube.data.materials.append(wireframe_mat)

# animation

anim(ythr, -1.2,  0)
anim(ythr, -1.2, 10)
anim(ythr,  1.2, 60)
anim(ythr,  1.2, 120)
anim(ythr, -1.2, 180)
anim(ythr, -1.2, 200)

# sky
colorSky((0.01, 0.01, 0.02, 1))

# camera
camera = bpy.data.objects['Camera']
camera.location = (0,30,0)
camera.rotation_euler = (pi/2,0,pi)

# add empty to control camera position
bpy.ops.object.empty_add(type='PLAIN_AXES')
bpy.context.object.name = 'c_empty'
c_empty = bpy.data.objects['c_empty']

# parent the camera to the empty
camera.parent = c_empty

# rotate empty
c_empty.rotation_euler = (0,0,-pi/8)
# empty.keyframe_insert(data_path='rotation_euler', frame=11)
# empty.rotation_euler = (0,0,2*pi)
# empty.keyframe_insert(data_path='rotation_euler', frame=261)

# render image
bpy.context.scene.camera = camera
bpy.context.scene.frame_end = 200

render('orb', 0.02, True)
        