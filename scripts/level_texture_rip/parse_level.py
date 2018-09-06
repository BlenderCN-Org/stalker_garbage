import struct, stalker_utils


def parse_textures(data, data_size):
    position = 0
    texture_count = struct.unpack('I', data[position : position + 4])[0]
    position += 4
    image_list = {}
    materials = data[position : ].split(b'\x00')
    for material in materials:
        try:
            images = material.split(b'/')[1]
            image = str(images.split(b',')[0])[2:-1]
            image_list[image] = True
        except:
            pass
    image_list = list(image_list.keys())
    image_list.sort()
    return image_list