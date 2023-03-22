import bpy

def emission(color, strength):
    mat = bpy.context.active_object.active_material
    em = mat.node_tree.nodes.new('ShaderNodeEmission')
    mat.node_tree.links.new(color, em.inputs["Color"])
    mat.node_tree.links.new(strength, em.inputs["Strength"])
    return em.outputs["Emission"]

#constant values
def plain_emission(color, strength):
    mat = bpy.context.active_object.active_material
    em = mat.node_tree.nodes.new('ShaderNodeEmission')
    em.inputs["Color"].default_value = color
    em.inputs["Strength"].default_value = strength
    return em.outputs["Emission"]

def as_surface(shading):
    mat = bpy.context.active_object.active_material
    material_output = mat.node_tree.nodes['Material Output']
    mat.node_tree.links.new(shading, material_output.inputs["Surface"])

def as_volume(shading):
    mat = bpy.context.active_object.active_material
    material_output = mat.node_tree.nodes['Material Output']
    mat.node_tree.links.new(shading, material_output.inputs["Volume"])

def location():
    mat = bpy.context.active_object.active_material
    loc = mat.node_tree.nodes.new('ShaderNodeNewGeometry')
    return loc.outputs["Position"]

def node_material():
    mat = bpy.data.materials.new(name="Material")
    mat.use_nodes = True
    mat.node_tree.nodes.remove(mat.node_tree.nodes['Principled BSDF'])
    bpy.context.active_object.active_material = mat
    return mat