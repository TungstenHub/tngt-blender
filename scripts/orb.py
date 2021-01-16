import bpy
from math import pi

from utils.nodes.color import hue_ramp
from utils.nodes.material import emission, as_volume, location, node_material
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
camera.location = (0,12.5,0)
camera.rotation_euler = (pi/2,0,pi)

# render image
bpy.context.scene.camera = camera
bpy.context.scene.frame_end = 200

render('orb', 0.2, False)
        