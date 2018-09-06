import struct, time


def print_bytes(byte_data, column_count = 8, save = False):
    stime = time.time()
    hex_data = list(map(hex, struct.unpack('%db' % len(byte_data), byte_data)))
    column = 0
    text = ''
    for hex_number in hex_data:
        column += 1
        if column % column_count == 0:
            print('{0:<5}'.format(hex_number), end='\n')
        else:
            print('{0:<5}  '.format(hex_number), end='')
    ftime = time.time()
    print('\ntotal time: {}s'.format(ftime-stime))


if __name__ == '__main__':
    file = open('1.object', 'rb')
    s = file.read()
    file.close()
    print_bytes(s)
    input()