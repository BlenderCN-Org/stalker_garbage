import xray_utils
from xray_utils import unpack_data as u
import struct


def parse_main(d):
    scale = 2.0
    newMesh = b''
    shader, _p = xray_utils.parse_string(d, 0)
    image, _p = xray_utils.parse_string(d, _p)
    newMesh += d[0 : _p + 4]
    (flgs, minS, maxS, vCnt, iCnt), _p = u('IffII', d, _p)
    newMinSize = struct.pack('f', minS * scale)
    newMaxSize = struct.pack('f', maxS * scale)
    newMesh += newMinSize + newMaxSize + d[_p - 8 : ]
    verts, uvs, faces = [], [], []
    for _ in range(vCnt):
        (X, Y, Z, U, V), _p = u('5f', d, _p)
        verts.append((X, Z, Y))
        uvs.append((U, 1 - V))
    for _ in range(iCnt // 3):
        (v1, v2, v3), _p = u('3H', d, _p)
        faces.append((v1, v3, v2))
    meshData = {'verts' : verts}
    meshData['faces'] = faces
    meshData['uvs'] = uvs
    meshData['images'] = image
    return newMesh

