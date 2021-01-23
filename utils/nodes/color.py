import bpy

def hue_ramp(fac):
    mat = bpy.context.active_object.active_material
    ramp = mat.node_tree.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.color_mode = 'HSV'
    ramp.color_ramp.hue_interpolation = 'CCW'
    ramp.color_ramp.elements[0].color = [1,0,0,1]
    ramp.color_ramp.elements[1].color = [1,0.001,0,1]
    mat.node_tree.links.new(fac, ramp.inputs["Fac"])
    return ramp.outputs["Color"]

def ramp(fac, arr):
    mat = bpy.context.active_object.active_material
    ramp = mat.node_tree.nodes.new('ShaderNodeValToRGB')
    elem = ramp.color_ramp.elements
    elem.remove(elem[0])
    l = len(arr)
    for i in range(l):
        elem.new(i/l)
        elem[i].color = arr[i]
    # already existing node
    elem[l].color = arr[0]
    mat.node_tree.links.new(fac, ramp.inputs["Fac"])
    return ramp.outputs["Color"]

def icefire(fac):
    return ramp(fac,
        [
            [0.000000, 0.120401, 0.302675, 1],
            [0.000000, 0.216583, 0.524574, 1],
            [0.055247, 0.345025, 0.659500, 1],
            [0.128047, 0.492588, 0.720288, 1],
            [0.188955, 0.641309, 0.792092, 1],
            [0.327673, 0.784935, 0.873434, 1],
            [0.608240, 0.892164, 0.935547, 1],
            [0.881371, 0.912178, 0.818099, 1],
            [0.951407, 0.835621, 0.449279, 1],
            [0.904481, 0.690489, 0.000000, 1],
            [0.854070, 0.510864, 0.000000, 1],
            [0.777093, 0.330180, 0.000882, 1],
            [0.672862, 0.139087, 0.002694, 1],
            [0.508815, 0.000000, 0.000000, 1],
            [0.299417, 0.000366, 0.000548, 1],
            [0.015752, 0.003320, 0.000000, 1],
            [0.000000, 0.000000, 0.000000, 1]
        ]
    )