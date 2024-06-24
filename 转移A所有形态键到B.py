import bpy

def copy_all_shape_keys():
    if len(bpy.context.selected_objects) == 2:
        source = bpy.context.selected_objects[1]
        dest = bpy.context.active_object
        for v in bpy.context.selected_objects:
            if v is not dest:
                source = v
                break
        
        print("Source: ", source.name)
        print("Destination: ", dest.name)
        
        if source.data.shape_keys is None:
            print("Source object has no shape keys!") 
        else:
            for idx in range(1, len(source.data.shape_keys.key_blocks)):
                source.active_shape_key_index = idx
                print("Copying Shape Key - ", source.active_shape_key.name)
                bpy.ops.object.shape_key_transfer()

print("Start")
copy_all_shape_keys()
print("End") 