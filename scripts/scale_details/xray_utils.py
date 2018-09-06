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

