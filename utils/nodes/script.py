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

def inn_script(s, *args):
    mat = bpy.context.active_object.active_material
    sc = mat.node_tree.nodes.new('ShaderNodeScript')
    sc.mode = 'INTERNAL'
    bpy.ops.text.new()
    formula = bpy.data.texts.new(name = 'formula.osl')
    formula.write(s)
    sc.script = formula
    sc.update()
    print(list(sc.inputs))
    for i in range(len(args)):
        mat.node_tree.links.new(args[i], sc.inputs[i])
    return tuple(sc.outputs)