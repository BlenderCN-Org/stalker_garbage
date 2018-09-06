import struct


def file_read(path):
    file = open(path, 'rb')
    data = file.read()
    file.close()
    return data


def block_read(data, position):
    block_id, hz, block_size = struct.unpack('HHI', data[position : position + 8])
    position += 8
    block_data = data[position : position + block_size]
    position += block_size
    return block_id, block_size, block_data, position


def print_bytes(data):
    data_bytes = struct.unpack('%dB' % len(data), data)
    column = 1
    column_count = 8
    for byte in data_bytes:
        if column % column_count != 0:
            print('{0: ^5}'.format(hex(byte)), end = ' ')
            column += 1
        else:
            print(hex(byte))
            column += 1
    print()

