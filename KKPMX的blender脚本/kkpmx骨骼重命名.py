#blender 3.5验证通过
#截至目前2025.11.30，KKPMX最新版导出已经不需要用这个脚本了。配合最新MMDTOOL直接就能导入动画文件
import bpy

def rename_bone(old_bone_name, new_bone_name):
    # Get the active armature object
    armature = bpy.context.object
    if armature is None or armature.type != 'ARMATURE':
        raise ValueError("No armature is currently selected")

    # Enter Edit Mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')

    # Get the edit bones
    edit_bones = armature.data.edit_bones

    # Find the bone to rename
    bone = edit_bones.get(old_bone_name)
    if bone is None:
        raise ValueError(f"Bone '{old_bone_name}' not found in the selected armature")

    # Rename the bone
    bone.name = new_bone_name

    # Return to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    print(f"Bone '{old_bone_name}' successfully renamed to '{new_bone_name}'")

#example
old_bone_name = 'cf_n_height'
new_bone_name = '全ての親'
rename_bone(old_bone_name, new_bone_name)
#direct rename
rename_bone('cf_j_hips', 'センター')
rename_bone('cf_j_spine01', '上半身')
rename_bone('cf_j_spine02', '上半身２')
rename_bone('cf_j_spine03', '上半身３')
rename_bone('cf_j_neck', '首')
rename_bone('cf_j_head','頭')
#rename_bone('Eyesx','両目')
#rename_bone('cf_J_hitomi_tx_L','左目')
#rename_bone('cf_J_hitomi_tx_R','右目')
rename_bone('cf_j_waist01','下半身')
rename_bone('cf_j_waist02','下半身２')
rename_bone('cf_j_shoulder_L','左肩')
rename_bone('cf_j_shoulder_R','右肩')
rename_bone('cf_j_arm00_L','左腕')
rename_bone('cf_j_arm00_R','右腕')
rename_bone('cf_j_forearm01_L','左ひじ')
rename_bone('cf_j_forearm01_R','右ひじ')
rename_bone('cf_j_hand_L','左手首')
rename_bone('cf_j_hand_R','右手首')
rename_bone('cf_j_thumb02_L','左親指１')
rename_bone('cf_j_thumb03_L','左親指２')
rename_bone('cf_j_thumb01_L','左親指０')
rename_bone('cf_j_thumb02_R','右親指１')
rename_bone('cf_j_thumb03_R','右親指２')
rename_bone('cf_j_thumb01_R','右親指０')
rename_bone('cf_j_index01_L','左人指１')
rename_bone('cf_j_index02_L','左人指２')
rename_bone('cf_j_index03_L','左人指３')
rename_bone('cf_j_index01_R','右人指１')
rename_bone('cf_j_index02_R','右人指２')
rename_bone('cf_j_index03_R','右人指３')
rename_bone('cf_j_middle01_L','左中指１')
rename_bone('cf_j_middle02_L','左中指２')
rename_bone('cf_j_middle03_L','左中指３')
rename_bone('cf_j_middle01_R','右中指１')
rename_bone('cf_j_middle02_R','右中指２')
rename_bone('cf_j_middle03_R','右中指３')
rename_bone('cf_j_ring01_L','左薬指１')
rename_bone('cf_j_ring02_L','左薬指２')
rename_bone('cf_j_ring03_L','左薬指３')
rename_bone('cf_j_ring01_R','右薬指１')
rename_bone('cf_j_ring02_R','右薬指２')
rename_bone('cf_j_ring03_R','右薬指３')
rename_bone('cf_j_little01_L','左小指１')
rename_bone('cf_j_little02_L','左小指２')
rename_bone('cf_j_little03_L','左小指３')
rename_bone('cf_j_little01_R','右小指１')
rename_bone('cf_j_little02_R','右小指２')
rename_bone('cf_j_little03_R','右小指３')
rename_bone('cf_j_thigh00_L','左足')
rename_bone('cf_j_thigh00_R','右足')
rename_bone('cf_j_leg01_L','左ひざ')
rename_bone('cf_j_leg01_R','右ひざ')
rename_bone('cf_j_leg03_L','左足首')
rename_bone('cf_j_leg03_R','右足首')
rename_bone('cf_j_toes_L','左つま先')
rename_bone('cf_j_toes_R','右つま先')
