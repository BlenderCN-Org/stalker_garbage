import xray_utils, time, os
from xray_utils import unpack_data as u


ver = (1, 0, 0)


def parse_0x7777(data):
    p = 0
    dataSize = len(data)
    while p < dataSize:
        (chunkId, chunkCompress, chunkSize), p = u('HHI', data, p)
        if chunkId == 0x0900:
            (version,), p = u('H', data, p)
            dumpFile.write('version      = {}\n'.format(version))
        elif chunkId == 0x0902:
            (fileVersion, unknow,), p = u('II', data, p)
            reference, p = xray_utils.parse_string(data, p)
            dumpFile.write('file_version = {}\n'.format(fileVersion))
            dumpFile.write('reference    = {}\n'.format(reference))
        elif chunkId == 0x0905:
            (flags,), p = u('I', data, p)
            dumpFile.write('flags        = {}\n'.format(flags))
        elif chunkId == 0xf903:
            (posX, pozY, posZ,
             rotX, rotY, rotZ,
             scaleX, scaleY, scaleZ), p = u('9f', data, p)
            dumpFile.write('position     = {0}, {1}, {2}\n'.format(posX, pozY, posZ))
            dumpFile.write('rotation     = {0}, {1}, {2}\n'.format(rotX, rotY, rotZ))
            dumpFile.write('scale        = {0}, {1}, {2}\n'.format(scaleX, scaleY, scaleZ))
        elif chunkId == 0xf906:
            (objectFlags,), p = u('I', data, p)
            objectSelected = bool(objectFlags & 0b1)
            objectVisible = bool(objectFlags & 0b10)
            objectLocked = bool(objectFlags & 0b100)
            objectMotionable = bool(objectFlags & 0b1000)
            dumpFile.write('selected     = {}\n'
                           'visible      = {}\n'
                           'locked       = {}\n'
                           'motionable   = {}\n'.format(
                objectSelected, objectVisible, objectLocked, objectMotionable))
        elif chunkId == 0xf907:
            objectName, p = xray_utils.parse_string(data, p)
            dumpFile.write('name         = {}\n'.format(objectName))
        else:
            xray_utils.un_blk(chunkId)
            p += chunkSize


def parse_object(data):
    p = 0
    dataSize = len(data)
    while p < dataSize:
        (chunkId, chunkCompress, chunkSize), p = u('HHI', data, p)
        if chunkId == 0x7777:
            parse_0x7777(data[p : p + chunkSize])
        p += chunkSize


def parse_objects(data):
    p = 0
    dataSize = len(data)
    while p < dataSize:
        (objectId, objectSize), p = u('II', data, p)
        dumpFile.write('\n[object_{0:0>4}]\n'.format(objectId))
        parse_object(data[p : p + objectSize])
        p += objectSize


def parse_scene(data):
    p = 0
    dataSize = len(data)
    while p < dataSize:
        (chunkId, chunkCompress, chunkSize), p = u('HHI', data, p)
        if chunkId == sceneObjectFmt['TAG']:
            authorName, p = xray_utils.parse_string(data, p)
            createDate, p = xray_utils.parse_date(data, p)
            dumpFile.write('author       = \"{}\"\n'.format(authorName))
            dumpFile.write('create_date  = \"{}\"\n'.format(createDate))
        elif chunkId == sceneObjectFmt['COUNT']:
            (objectCount, ), p = u('I', data, p)
            dumpFile.write('object_count = {}\n'.format(objectCount))
        elif chunkId == sceneObjectFmt['OBJECTS']:
            parse_objects(data[p : p + chunkSize])
            p += chunkSize
        elif chunkId == sceneObjectFmt['VERSION']:
            (version, ), p = u('H', data, p)
            dumpFile.write('\nversion      = {}\n'.format(version))
        elif chunkId == sceneObjectFmt['FLAGS']:
            (flags, ), p = u('I', data, p)
            dumpFile.write('flags        = {}\n'.format(flags))
        elif chunkId == sceneObjectFmt['PARAMS']:
            (minScaleX, minScaleY, minScaleZ,
             maxScaleX, maxScaleY, maxScaleZ,
             minRotX, minRotY, minRotZ,
             maxRotX, maxRotY, maxRotZ,
             snapObj), p = u('13f', data, p)
            dumpFile.write('min_scale    = {0}, {1}, {2}\n'.format(minScaleX, minScaleY, minScaleZ))
            dumpFile.write('max_scale    = {0}, {1}, {2}\n'.format(maxScaleX, maxScaleY, maxScaleZ))
            dumpFile.write('min_rotate   = {0}, {1}, {2}\n'.format(minRotX, minRotY, minRotZ))
            dumpFile.write('max_rotate   = {0}, {1}, {2}\n'.format(maxRotX, maxRotY, maxRotZ))
            dumpFile.write('snap_object  = {0}\n'.format(snapObj))
        else:
            xray_utils.un_blk(chunkId)
            p += chunkSize


def parse_guid(data):
    p = 0
    unknowData, p = u('16B', data, p)


startTime = time.time()
if xray_utils.ver != (1, 0, 0):
    print('! version xray_utils.py = {}.{}{}'.format(xray_utils.ver[0],
                                                     xray_utils.ver[1],
                                                     xray_utils.ver[2]))
    input('Press Enter...')
sceneObjectFmt = {'GUID'    : 0x7000,
                  'SCENE'   : 0x8002,
                  'TAG'     : 0x7777,
                  'COUNT'   : 0x0002,
                  'OBJECTS' : 0x0003,
                  'VERSION' : 0x1001,
                  'PARAMS'  : 0x1002,
                  'FLAGS'   : 0x1003}
fileName = os.path.abspath('.') + '\\' + 'scene_object.part'
data = xray_utils.read_bin_file(fileName)
p = 0
dataSize = len(data)
dumpFile = open('scene_object_dump.ltx', 'w')
while p < dataSize:
    (chunkId, chunkCompress, chunkSize), p = u('HHI', data, p)
    if chunkId == sceneObjectFmt['SCENE']:
        parse_scene(data[p : p + chunkSize])
    elif chunkId == sceneObjectFmt['GUID']:
        parse_guid(data[p : p + chunkSize])
    else:
        xray_utils.un_blk(chunkId)
    p += chunkSize
dumpFile.close()
print('total time: {0:.3}s'.format(time.time() - startTime))
input()

