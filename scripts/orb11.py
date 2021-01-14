import bpy
from math import pi

from utils.nodes.color import hue_ramp
from utils.nodes.material import emission, as_volume, location, node_material
from utils.nodes.script import osl_script
from utils.nodes.time import time
from utils.nodes.math import polar, multiply_by, fract
from utils.render import render
from utils.sky import colorSky

# set render engine to CYCLES and enable Open Shading Language
scn = bpy.context.scene
scn.render.engine = 'CYCLES'
scn.cycles.shading_system = True
    
cube = bpy.data.objects['Cube']
cube.scale = (5,5,5)

# add material for cube
orbital_mat = node_material()

location = location()
time = time(200, 0.05)

re, im = osl_script('orbital/orb_11', location, time)
r, phi = polar(re, im)
norm_phi = multiply_by(phi, 1 / (2*pi))
hue = fract(norm_phi)
color = hue_ramp(hue)
strength = multiply_by(r, 0.5)
ems = emission(color, strength)

as_volume(ems)

cube.data.materials.append(orbital_mat)

# sky
colorSky((0.01, 0.01, 0.02, 1))

# camera
camera = bpy.data.objects['Camera']
camera.location = (15,0,0)
camera.rotation_euler = (pi/2,0,pi/2)

# render image
bpy.context.scene.camera = camera
bpy.context.scene.frame_end = 200

render('orb11', 0.02, True)
        