import bpy


oldPath = 'E:\\X-Ray SDK\\level_editor\\gamedata\\textures\\'
newPath = 'E:\\STALKER Game\\CS\\gamedata_unpack\\textures\\'
for i in bpy.data.images:
    i.filepath = newPath + i.filepath[len(oldPath) : ]

