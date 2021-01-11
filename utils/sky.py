import bpy

def colorSky(color):
    bpy.context.scene.world.use_nodes = True
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = color
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[1].default_value = 1
    