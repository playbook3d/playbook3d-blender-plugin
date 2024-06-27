import bpy
import os

# For objects without animations, convert to mesh and apply all transforms
for obj in bpy.data.objects: # loop thru all objects in scene
    if obj.visible_get():
        if obj.animation_data and obj.animation_data.action:
            print("Has animation")
        else: # check if no animations
            if obj.type != 'MESH':
                # Convert object to mesh
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                if bpy.ops.object.convert.poll():
                    bpy.ops.object.convert(target='MESH')
    
            # Apply object transforms
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

            # Print confirmation
            print(f"Converted '{obj.name}' to mesh and applied transforms.")
        
# Bake animations on any objects that are childed to other objects
for obj in bpy.context.scene.objects:
    if obj.visible_get():
        # Check if the object is a child
        if obj.parent:
            # Check if the object is animated
            if obj.animation_data and obj.animation_data.action:
                # Select the child object and bake its animation
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.ops.nla.bake(frame_start=bpy.context.scene.frame_start,
                                 frame_end=bpy.context.scene.frame_end,
                                 step=1, only_selected=True, visual_keying=True, clear_constraints=True)
                print(f"Baked animation for child object '{obj.name}'.")

# Apply all transforms on animated objects that previously had children
for obj in bpy.context.scene.objects:
    if obj.visible_get():
        # Check if the object is a parent
        if obj.children:
            if obj.type != 'MESH':
                # Convert object to mesh
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                if bpy.ops.object.convert.poll():
                    bpy.ops.object.convert(target='MESH')
        
            # Apply object transforms
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

            # Print confirmation
            print(f"Converted '{obj.name}' to mesh and applied transforms.")
     
# Bake animations of animated objects       
for obj in bpy.context.scene.objects:
    if obj.visible_get():
        if obj.animation_data and obj.animation_data.action:
            # Bake its animation
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.nla.bake(frame_start=bpy.context.scene.frame_start,
                            frame_end=bpy.context.scene.frame_end,
                            step=1, only_selected=True, visual_keying=True, clear_constraints=True)
            print(f"Baked animation for object '{obj.name}'.")
            
            # Add the baked animation to an NLA track
            track_name = f"{obj.name}_Track"
            track = obj.animation_data.nla_tracks.new()
            track.name = track_name
            strip = track.strips.new(name=obj.animation_data.action.name,
                        start=bpy.context.scene.frame_start,
                        action=obj.animation_data.action)
            strip.name = obj.animation_data.action.name

            # Print confirmation
            print(f"Add baked animation for '{obj.name}' to NLA strips.")
            
            
# Export
            
file_format = 'FBX'
            
# Get the current Blender file's filepath
blend_filepath = bpy.data.filepath
            
# Extract directory path from Blender file's filepath
blend_dir = os.path.dirname(blend_filepath)
        
# Construct export filepath with the same name but different extension
export_filepath = os.path.join(blend_dir, f"{bpy.path.display_name_from_filepath(blend_filepath)}.{file_format.lower()}")
        
               
bpy.ops.export_scene.fbx(filepath=export_filepath, 
                            check_existing=True, 
                            use_visible=True,
                            object_types={'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'},
                            use_tspace=True,
                            bake_anim=True,
                            bake_anim_use_all_bones=False,
                            bake_anim_use_nla_strips=True,
                            bake_anim_use_all_actions=False,
                            bake_anim_force_startend_keying=True)
                            