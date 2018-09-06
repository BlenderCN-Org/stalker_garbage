HEADER        = (1, 'HEADER')
TEXTURE       = (2, 'TEXTURE')
VERTICES      = (3, 'VERTICES')
INDICES       = (4, 'INDICES')
P_MAP         = (5, 'P_MAP')
SWIDATA       = (6, 'SWIDATA')
VCONTAINER    = (7, 'VCONTAINER')
ICONTAINER    = (8, 'ICONTAINER')
CHILDREN      = (9, 'CHILDREN')
CHILDREN_L    = (10, 'CHILDREN_L')
LODDEF2       = (11, 'LODDEF2')
TREEDEF2      = (12, 'TREEDEF2')
S_BONE_NAMES  = (13, 'S_BONE_NAMES')
S_MOTIONS     = (14, 'S_MOTIONS')
S_SMPARAMS    = (15, 'S_SMPARAMS')
S_IKDATA      = (16, 'S_IKDATA')
S_USERDATA    = (17, 'S_USERDATA')
S_DESC        = (18, 'S_DESC')
S_MOTION_REFS = (19, 'S_MOTION_REFS')
SWICONTAINER  = (20, 'SWICONTAINER')
GCONTAINER    = (21, 'GCONTAINER')
FASTPATH      = (22, 'FASTPATH')
S_LODS        = (23, 'S_LODS')

mesh_type_names = {0  : 'MT_NORMAL',
                   1  : 'MT_HIERRARHY',
                   2  : 'MT_PROGRESSIVE',
                   3  : 'MT_SKELETON_ANIM',
                   4  : 'MT_SKELETON_GEOMDEF_PM',
                   5  : 'MT_SKELETON_GEOMDEF_ST',
                   6  : 'MT_LOD',
                   7  : 'MT_TREE_ST',
                   8  : 'MT_PARTICLE_EFFECT',
                   9  : 'MT_PARTICLE_GROUP',
                   10 : 'MT_SKELETON_RIGID',
                   11 : 'MT_TREE_PM'}


vertex_format = {'1L'	: 0x12071980,
                 '2L'	: 0x240e3300,
                 'NL'	: 0x36154c80,
                 'OLD'	: 0x00000112}