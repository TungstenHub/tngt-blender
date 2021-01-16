def anim(output, v, f): 
    output.default_value = v
    output.keyframe_insert(data_path='default_value', frame=f)