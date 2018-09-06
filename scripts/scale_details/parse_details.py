from xray_utils import unpack_data as u
import parse_dm


def parse_main(d):
    _p, _fileSz = 0, len(d)
    newDet = open('level.details.new', 'wb')
    while _p < _fileSz:
        (_id, _cmpr, _sz), _p = u('HHI', d, _p)
        if _id == 0x1:
            newData = parse_meshes(d[_p : _p + _sz])
            newDet.write(d[_p - 8 : _p])
            newDet.write(newData)
        else:
            newDet.write(d[_p - 8 : _p + _sz])
        _p += _sz
    newDet.close()


def parse_meshes(d):
    _p, _blkSz = 0, len(d)
    newData = b''
    while _p < _blkSz:
        newData += d[_p : _p + 8]
        (_id, _cmpr, _sz), _p = u('HHI', d, _p)
        newMesh = parse_dm.parse_main(d[_p : _p + _sz])
        newData += newMesh
        _p += _sz
    return newData

