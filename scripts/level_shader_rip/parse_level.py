import struct


def parse_textures(d):
    _p = 0
    mtlCnt = struct.unpack('I', d[_p : _p + 4])[0]
    _p += 4
    mtls = d[_p : ].split(b'\x00')
    print('shaders:')
    shdrs = {}
    for n, _ in enumerate(mtls):
        shdr = str(_)[2:-1].split('/')[0]
        shdrs[shdr] = True
    shdrs = list(shdrs.keys())
    shdrs.sort()
    for _ in shdrs:
        print(_)

