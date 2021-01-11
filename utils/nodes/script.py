import os

import bpy

def osl_script(path, *args):
    mat = bpy.context.active_object.active_material
    sc = mat.node_tree.nodes.new('ShaderNodeScript')
    sc.mode = 'EXTERNAL'
    sc.filepath = os.path.abspath('./utils/shaders/' + path + '.osl')
    for i in range(len(args)):
        mat.node_tree.links.new(args[i], sc.inputs[i])
    return tuple(sc.outputs)