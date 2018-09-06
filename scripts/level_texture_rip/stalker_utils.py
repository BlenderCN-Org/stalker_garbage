import struct, os


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


def parse_string(data, position):
    string = ''
    char = struct.unpack('B', data[position : position + 1])[0]
    position += 1
    while char != 0:
        string = string + chr(char)
        char = struct.unpack('B', data[position : position + 1])[0]
        position += 1
    return string, position


def copy_files(path, files, ext, new_path, copy_bump):
    log = open('copy.log', 'w')
    
    list_dir = {}
    for file_name in files:
        list_dir[new_path+file_name.split('\\')[0]] = True
    
    list_dir = list(list_dir.keys())
    list_dir.sort()
    
    if not os.access(new_path, os.F_OK):
        os.makedirs(new_path)
    
    for dir in list_dir:
        try:
            os.mkdir(dir)
        except:
            print('cannot create', dir)
    
    for file_name in files:
        try:
            copy_file(path, file_name, ext, new_path)
            if os.access(path+file_name+'_bump'+ext, os.F_OK) and copy_bump:
                copy_file(path, file_name+'_bump', ext, new_path)
            if os.access(path+file_name+'_bump#'+ext, os.F_OK) and copy_bump:
                copy_file(path, file_name+'_bump#', ext, new_path)
        except:
            print('cannot open', path+file_name+ext, file=log)
    log.close()


def copy_file(path, file_name, ext, new_path):
    file = open(path+file_name+ext, 'rb')
    file_data = file.read()
    file.close()
    new_file = open(new_path+file_name+ext, 'wb')
    new_file.write(file_data)
    new_file.close()

