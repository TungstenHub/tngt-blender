import bpy

from utils.nodes.script import osl_script

def polar(x,y):
    return osl_script('math/polar', x, y)

# node output - scalar
def summ_by(a,b): 
    mat = bpy.context.active_object.active_material
    summ = mat.node_tree.nodes.new('ShaderNodeMath')
    summ.operation = 'ADD'
    summ.inputs[1].default_value = b
    mat.node_tree.links.new(a, summ.inputs[0])
    return summ.outputs["Value"]

# node output - node output
def summ(a,b): 
    mat = bpy.context.active_object.active_material
    summ = mat.node_tree.nodes.new('ShaderNodeMath')
    summ.operation = 'ADD'
    mat.node_tree.links.new(a, summ.inputs[0])
    mat.node_tree.links.new(b, summ.inputs[1])
    return summ.outputs["Value"]

# node output - scalar
def multiply_by(a,b): 
    mat = bpy.context.active_object.active_material
    mult = mat.node_tree.nodes.new('ShaderNodeMath')
    mult.operation = 'MULTIPLY'
    mult.inputs[1].default_value = b
    mat.node_tree.links.new(a, mult.inputs[0])
    return mult.outputs["Value"]

# node output - node output
def multiply(a,b): 
    mat = bpy.context.active_object.active_material
    mult = mat.node_tree.nodes.new('ShaderNodeMath')
    mult.operation = 'MULTIPLY'
    mat.node_tree.links.new(a, mult.inputs[0])
    mat.node_tree.links.new(b, mult.inputs[1])
    return mult.outputs["Value"]

def fract(a): 
    mat = bpy.context.active_object.active_material
    fract = mat.node_tree.nodes.new('ShaderNodeMath')
    fract.operation = 'FRACT'
    mat.node_tree.links.new(a, fract.inputs["Value"])
    return fract.outputs["Value"]

def value(v):
    mat = bpy.context.active_object.active_material
    timenode = mat.node_tree.nodes.new('ShaderNodeValue')
    timenode.outputs["Value"].default_value = v
    return timenode.outputs["Value"]