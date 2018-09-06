import xray_utils
from xray_utils import unpack_data as u


def parse_header(s):
    print('LEVEL format version:', u('H', s, 0)[0])


s = xray_utils.read_bin_file('level')
p = 0
while p < len(s):
    (id, cmpr, sz), p = u('HHI', s, p)
    if id == 0x1:
        parse_header(s[p : p + sz])
    p += sz
input()