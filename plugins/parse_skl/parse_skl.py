import xray_utils
from xray_utils import unpack_data as u


def parse_main(d):
    (motionCnt, ), p = u('I', d, 0)
    motionName, p = xray_utils.parse_string(d, p)
    (startFrame, endFrame), p = u('II', d, p)
    (fps, ), p = u('f', d, p)
    (ver, ), p = u('H', d, p)
    (flags, ), p = u('B', d, p)
    typeFx = flags & 0x1
    stopAtEnd = flags & 0x2
    noMix = flags & 0x4
    syncPart = flags & 0x8
    (bonePart, ), p = u('B', d, p)
    (boneStart, ), p = u('B', d, p)
    (speed, accrue, falloff, power, boneCnt), p = u('ffffH', d, p)
    for i in range(boneCnt):
        boneName, p = xray_utils.parse_string(d, p)
        (flags, ), p = u('B', d, p)
        for i in range(6):
            behaviours, p = u('BB', d, p)
            (keys, ), p = u('H', d, p)
            for j in range(keys):
                (value, time, shape), p = u('ffB', d, p)
                print(value, time * fps)


d = xray_utils.read_bin_file('1.skl')
parse_main(d)
input()

