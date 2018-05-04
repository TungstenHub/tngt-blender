import bpy
from math import pi

bpy.ops.wm.addon_enable(module="add_mesh_extra_objects")
from mathutils import Color 

# delete all previous objects and meshes

def reset_blend():

    for scene in bpy.data.scenes:
        for obj in scene.objects:
            scene.objects.unlink(obj)

    for bpy_data_iter in (
            bpy.data.objects,
            bpy.data.meshes,
            bpy.data.lamps,
            bpy.data.cameras,
            bpy.data.materials,
            bpy.data.textures,
            bpy.data.particles,
            bpy.data.node_groups,
            ):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data, do_unlink=True)

reset_blend()

# set render engine to CYCLES and enable Open Shading Language
scn = bpy.context.scene
scn.render.engine = 'CYCLES'
bpy.context.scene.cycles.shading_system = True

# cursor to center
bpy.context.scene.cursor_location = (0.0, 0.0, 0.0)
    
# add cube
bpy.ops.mesh.primitive_cube_add()
bpy.context.object.name = 'cube'
cube = bpy.data.objects['cube']
cube.scale=(1,1,1)

# add material for cube
bpy.ops.material.new()
orbital_mat = bpy.data.materials['Material']
orbital_mat.use_nodes = True
nodes = orbital_mat.node_tree.nodes
links = orbital_mat.node_tree.links

material_output = nodes['Material Output']

nodes.remove(nodes['Diffuse BSDF'])

bpy.ops.text.new()
formula = bpy.data.texts['Text']
formula.name = 'formula.osl'
s = '''
shader Orbital(
    float Time = 0.0,
    vector Position = vector(0, 0, 0),
    output float Hue = 0.5,
    output float Density = 0.5)
{
    float scale = 0.3;
    float x = Position[0]/scale;
    float y = Position[1]/scale;
    float z = Position[2]/scale;
    float r = sqrt(x*x + y*y + z*z);
    float wx = exp(-r)*cos(-2*Time)*z/r;
    float wy = exp(-r)*sin(-2*Time)*z/r;
    Hue = atan2(-wy,-wx)/6.28+0.5;
    Density = (wx*wx+wy*wy)*3.5;
}
'''
formula.write(s)

script = nodes.new('ShaderNodeScript')
script.mode = 'INTERNAL'
script.script = formula
script.update()

location = nodes.new('ShaderNodeNewGeometry')

emission = nodes.new('ShaderNodeEmission')

time = nodes.new('ShaderNodeValue')
for k in range(200):
    time.outputs[0].default_value = k/10
    time.outputs[0].keyframe_insert(data_path='default_value', frame=k+1)

c_ramp = nodes.new('ShaderNodeValToRGB')
c_ramp.color_ramp.color_mode = 'HSV'
c_ramp.color_ramp.hue_interpolation = 'CCW'
c_ramp.color_ramp.elements[0].color= [1,0,0,1]
c_ramp.color_ramp.elements[1].color= [1,0.001,0,1]

links.new(time.outputs["Value"], script.inputs["Time"])
links.new(location.outputs["Position"], script.inputs["Position"])
links.new(script.outputs["Hue"], c_ramp.inputs["Fac"])
links.new(c_ramp.outputs["Color"], emission.inputs["Color"])
links.new(script.outputs["Density"], emission.inputs["Strength"])
links.new(emission.outputs["Emission"], material_output.inputs["Volume"])

cube.data.materials.append(orbital_mat)

# add camera
bpy.ops.object.camera_add(location=(3,0,0), rotation=(pi/2,0,pi/2))
bpy.context.object.name = 'camera'
camera = bpy.data.objects['camera']

# add sky 
def add_sky():
    bpy.context.scene.world.use_sky_blend = True
    bpy.context.scene.world.use_sky_real = True
    bpy.context.scene.world.zenith_color = (0.00, 0.00, 0.00)
    bpy.context.scene.world.horizon_color = (0.01, 0.01, 0.02)

add_sky()

# render image
bpy.context.scene.camera = camera
bpy.context.scene.frame_end = 200
bpy.data.scenes['Scene'].render.resolution_x = 1960
bpy.data.scenes['Scene'].render.resolution_y = 1080

mode = 'video'

if mode == 'image':
    bpy.data.scenes['Scene'].render.image_settings.file_format = 'JPEG'
    bpy.data.scenes['Scene'].render.filepath = '/tmp/orb01.jpg'
    bpy.ops.render.render(animation=False,write_still=True)
elif mode == 'video':
    bpy.data.scenes['Scene'].render.image_settings.file_format = 'AVI_JPEG'
    bpy.data.scenes['Scene'].render.filepath = '/tmp/orb01.avi'
    bpy.ops.render.render(animation=True)
        