import bpy

def render(name, prop, image = False):
    bpy.data.scenes['Scene'].render.resolution_x = 1440 * prop
    bpy.data.scenes['Scene'].render.resolution_y = 1080 * prop
    if image:
        bpy.data.scenes['Scene'].render.image_settings.file_format = 'JPEG'
        bpy.data.scenes['Scene'].render.filepath = './output/' + name + '.jpg'
        bpy.ops.render.render(animation=False,write_still=True)
    else:
        bpy.data.scenes['Scene'].render.image_settings.file_format = 'AVI_JPEG'
        bpy.data.scenes['Scene'].render.filepath = './output/' + name + '.avi'
        bpy.ops.render.render(animation=True)