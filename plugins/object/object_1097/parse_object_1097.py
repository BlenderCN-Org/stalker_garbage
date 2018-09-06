import xray_utils
from xray_utils import unpack_data as u


def parse_mesh(d):
    meshSize = len(d)
    p = 0
    while p < meshSize:
        (id, cmpr, sz), p = u('HHI', d, p)
        if id == 0x1000:
            meshVer, p = u('H', d, p)
        elif id == 0x1001:
            meshName, p = u('%ds' % sz, d, p)
        elif id == 0x1002:
            flags, p = u('B', d, p)
        elif id == 0x1003:
            unknow, p = u('B', d, p)
        elif id == 0x1004:
            bbox, p = u('6f', d, p)
        elif id == 0x1005:
            (vCnt,), p = u('I', d, p)
            for i in range(vCnt):
                (X, Y, Z), p = u('3f', d, p)
            for i in range(vCnt):
                unknow, p = u('7B', d, p)
        elif id == 0x1006:
            tCnt = sz // 12
            for i in range(tCnt):
                (v1, v2, v3), p = u('3I', d, p)
                print(v1, v2, v3)
            p += 4
        elif id == 0x1010:
            unknow, p = u('IHH', d, p)
        else:
            p += sz
            print(hex(id), sz)


d = xray_utils.read_bin_file('Bush6_hang.object')
(id, cmpr, sz), p = u('HHI', d, 0)
fileSize = len(d)
while p < fileSize:
    (id, cmpr, sz), p = u('HHI', d, p)
    if id == 0x0900:    # format version
        (fmtVer,), p = u('H', d, p)
    elif id == 0x0903:
        objectType, p = u('B', d, p)
    elif id == 0x0904:    # transformations
        (pX, pY, pZ, rX, rY, rZ, sX, sY, sZ), p = u('9f', d, p)
    elif id == 0x0905:
        (materialId,), p = u('I', d, p)
        materialName, p = xray_utils.parse_string(d, p)
        shader, p = xray_utils.parse_string(d, p)
        unknow, p = u('BBHHHB', d, p)
        texture, p = xray_utils.parse_string(d, p)
        uvSlotName, p = xray_utils.parse_string(d, p)
    elif id == 0x0910:
        while p < sz:
            (meshId, meshSize), p = u('II', d, p)
            parse_mesh(d[p : p + meshSize])
            p += meshSize
    elif id == 0x0911:
        (unknow1, unknow2), p = u('fI', d, p)
    elif id == 0x0912:
        unknow, p = u('B', d, p)
    elif id == 0x0913:
        unknow, p = u('I', d, p)
    elif id == 0x0914:
        unknow, p = u('I', d, p)
    elif id == 0x0916:
        unknow, p = u('I', d, p)
    elif id == 0xf900:
        unknow, p = u('4B', d, p)
        name, p = xray_utils.parse_string(d, p)
    elif id == 0xf901:
        unknow, p = u('4B', d, p)
    elif id == 0xf902:
        unknow, p = u('2B', d, p)
    else:
        p += sz
        print(hex(id), sz)
input()

