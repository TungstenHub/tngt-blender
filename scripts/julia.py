import bpy
from math import pi

from utils.nodes.material import node_material, location, emission, as_surface
from utils.nodes.script import osl_script, inn_script
from utils.nodes.color import icefire
from utils.nodes.math import value, fract, multiply_by, summ_by
from utils.nodes.anim import anim
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

shader = 'basic'
params_dict = {
    'basic': {
        'bailout': 2**2,
        'max_iter': 2**6,
        'color_factor': 0.1,
        'color_offset': 0.1
    },
    'norm': {
        'bailout': 2**8,
        'max_iter': 2**6,
        'color_factor': 0.1,
        'color_offset': -0.09
    },
    'smooth': {
        'bailout': 2**8,
        'max_iter': 2**6,
        'color_factor': -0.1,
        'color_offset': 0.4
    }
}
params = params_dict[shader]

# # add material for cube
julia_mat = node_material()

location = location()

alpha = value(0)

s1 = '''
shader Cardioid(
    float a = 0.0,
    output float x = 0.0,
    output float y = 0.0)
{
    x = 0.25 + cos(a) * (1.0 - cos(a)) / 2;
    y = sin(a) * (1.0 - cos(a)) / 2;
}
'''

seed_x, seed_y = inn_script(s1, alpha)

bailout = value(params['bailout'])
max_iter = value(params['max_iter'])

inside, out = osl_script('fractal/julia_' + shader, location, seed_x, seed_y, bailout, max_iter)

fac = fract(summ_by(multiply_by(out,params['color_factor']),params['color_offset']))

out_color = icefire(fac)

s2 = '''
shader Color(
    float inside = 0,
    color out = color(0),
    output color c = color(0))
{
    if (inside) { c = color(0); }
    else        { c = out; }
}
'''

(color, ) = inn_script(s2, inside, out_color)

strength = value(1)
ems = emission(color, strength)

as_surface(ems)

plane.data.materials.append(julia_mat)

# animation

anim(alpha, 0, 0)
anim(alpha, 2*pi, 100)

# camera
camera = bpy.data.objects['Camera']
camera.location = (0,0,10.1)
camera.rotation_euler = (0,0,0)

# render image
bpy.context.scene.camera = camera
bpy.context.scene.frame_end = 100

render('julia_' + shader, 0.6, True)
        