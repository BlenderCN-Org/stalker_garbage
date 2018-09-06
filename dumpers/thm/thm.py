from struct import unpack as u


def parse_main(s):
    p = 0
    while p < len(s):
        id, cmpr, sz = u('HHI', s[p : p + 8])
        p += 8
        if id == 0x810:
            pass
        print(hex(id), sz)
        p += sz


f = open('$shadertest.thm', 'rb')
s = f.read()
f.close()
parse_main(s)
input()