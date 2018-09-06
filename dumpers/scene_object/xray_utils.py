import struct, os, time


def unpack_data(fmt, data, offs):
    size = struct.calcsize(fmt)
    return struct.unpack(fmt, data[offs : offs + size]), offs + size


def read_bin_file(file_name, file_ext='', file_path=''):
    if len(file_path) != 0:
        if file_path[-1] != '\\':
            file_path = file_path + '\\'
    if len(file_ext) != 0:
        if file_ext[0] != '.':
            file_ext = '.' + file_ext
        _absolute_path = file_path + file_name + file_ext
    else:
        _absolute_path = file_path + file_name
    try:
        _file = open(_absolute_path, 'rb')
        file_data = _file.read()
        _file.close()
    except:
        print(' ! CANNOT OPEN FILE: {}'.format(_absolute_path))
        file_data = b''
    return file_data


def parse_string(data, offs):
    string = ''
    _char = struct.unpack('B', data[offs : offs + 1])[0]
    offs += 1
    while _char != 0:
        string = string + chr(_char)
        _char = struct.unpack('B', data[offs : offs + 1])[0]
        offs += 1
    return string, offs


def parse_date(data, offs):
    (date, ), offs = unpack_data('I', data, offs)
    return time.ctime(date), offs


def un_ver(fmt, fmtVer):
    print(' ! UNSUPPORTED {0} FORMAT VERSION ({1})'.format(fmt, fmtVer))


def un_blk(id):
    print(' ! UNKNOW BLOCK ({0})'.format(hex(id)))


def generate_face(vertex_count):
    faces = []
    for index in range(0, vertex_count, 3):
        faces.append((index, index + 2, index + 1))
    return faces


def print_bytes(data, column_count=16):
    _data_bytes = struct.unpack('%dB' % len(data), data)
    _column = 1
    if column_count < 1 or column_count > 16:
        column_count = 16
    for _byte in _data_bytes:
        if _column % column_count != 0:
            print('{0: ^4}'.format(hex(_byte)), end=' ')
            _column += 1
        else:
            print(hex(_byte))
            _column += 1
    print()
    return 'FINISHED'



def get_module_version():
    print('ver. {}.{}{}'.format(ver[0], ver[1], ver[2]))
    input()


ver = (1, 0, 0)
if __name__ == '__main__':
    get_module_version()

