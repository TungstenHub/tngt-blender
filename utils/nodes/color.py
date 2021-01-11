import bpy

def hue_ramp(fac):
    mat = bpy.context.active_object.active_material
    ramp = mat.node_tree.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.color_mode = 'HSV'
    ramp.color_ramp.hue_interpolation = 'CCW'
    ramp.color_ramp.elements[0].color= [1,0,0,1]
    ramp.color_ramp.elements[1].color= [1,0.001,0,1]
    mat.node_tree.links.new(fac, ramp.inputs["Fac"])
    return ramp.outputs["Color"]