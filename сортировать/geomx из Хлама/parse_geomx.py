import xray_utils
from xray_utils import unpack_data as u


def parse_0x9(d):
    p = 0
    unk, p = u('iiiiIffffff', d, p)
    print(unk)


def parse_0xa(d):
    pass


d = xray_utils.read_bin_file('level.geomx')
dataSize = len(d)
p = 0
while p < dataSize:
    (id, cmpr, sz), p = u('HHI', d, p)
    if id == 0x1:
        fmtVer, p = u('BBBB', d, p)
    elif id == 0x9:
        parse_0x9(d[p : p + sz])
        p += sz
    elif id == 0xa:
        parse_0xa(d[p : p + sz])
        p += sz
    elif id == 0xb:
        (unk, ), p = u('I', d, p)
input()

