import bpy

from utils.nodes.script import osl_script

def polar(x,y):
    return osl_script('math/polar', x, y)

# node output - scalar
def multiply_by(a,b): 
    mat = bpy.context.active_object.active_material
    mult = mat.node_tree.nodes.new('ShaderNodeMath')
    mult.operation = 'MULTIPLY'
    mult.inputs[1].default_value = b
    mat.node_tree.links.new(a, mult.inputs[0])
    return mult.outputs["Value"]

def fract(a): 
    mat = bpy.context.active_object.active_material
    fract = mat.node_tree.nodes.new('ShaderNodeMath')
    fract.operation = 'FRACT'
    mat.node_tree.links.new(a, fract.inputs["Value"])
    return fract.outputs["Value"]