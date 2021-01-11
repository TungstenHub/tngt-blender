import bpy

def time(end, ratio = 1):
    # bpy.ops.action.interpolation_type(type='LINEAR')
    mat = bpy.context.active_object.active_material
    timenode = mat.node_tree.nodes.new('ShaderNodeValue')
    for k in range(end):
        timenode.outputs[0].default_value = k * ratio
        timenode.outputs[0].keyframe_insert(data_path='default_value', frame=k+1)
    return timenode.outputs["Value"]