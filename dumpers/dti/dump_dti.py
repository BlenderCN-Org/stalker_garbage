import os, xray_utils    # use xray_utils ver 1.01
from xray_utils import unpack_data as u
from optparse import OptionParser


class DtiFormat:
    class Chunks:
        class Objects:    # DETMGR_CHUNK_OBJECTS
            class Object:
                class Version:   # DETOBJ_CHUNK_VERSION
                    id = 0x1000
                    cur_ver = 0x0001    # DETOBJ_VERSION = 0x0001
                class Reference:    # DETOBJ_CHUNK_REFERENCE
                    id = 0x0101
                class ScaleLimits:    # DETOBJ_CHUNK_SCALE_LIMITS
                    id = 0x0102
                class DensityFactor:    # DETOBJ_CHUNK_DENSITY_FACTOR
                    id = 0x0103
                class Flags:    # DETOBJ_CHUNK_FLAGS
                    id = 0x0104
            id = 0x1
        class ColorIndex:    # DETMGR_CHUNK_COLOR_INDEX
            id = 0x1003


def parse_detail_flags(d):
    global dump
    (noWaving, ), p = u('I', d, 0)
    dump += '  no waving = {}\n'.format(str(bool(noWaving)).lower())


def parse_detail_density_factor(d):
    global dump
    (density, ), p = u('f', d, 0)
    dump += '  density   = {}\n'.format(round(density, 2))


def parse_detail_scale_limits(d):
    global dump
    (minScale, maxScale, ), p = u('ff', d, 0)
    dump += '  min scale = {}\n'.format(round(minScale, 2))
    dump += '  max scale = {}\n'.format(round(maxScale, 2))


def parse_detail_reference(d):
    global dump
    referenceName, p = xray_utils.parse_string(d, 0)
    dump += '  reference = "{}"\n'.format(referenceName)


def parse_detail_version(d):
    global dump
    (version, ), p = u('I', d, 0)
    dump += '  version   = {}\n'.format(version)


def parse_detail_object(d):
    global dump
    p = 0
    dataSize = len(d)
    while p < dataSize:
        (id, cmprs, sz), p = u('HHI', d, p)
        cd = d[p : p + sz]
        if id == DtiFormat.Chunks.Objects.Object.Version.id:
            parse_detail_version(cd)
        elif id == DtiFormat.Chunks.Objects.Object.Reference.id:
            parse_detail_reference(cd)
        elif id == DtiFormat.Chunks.Objects.Object.ScaleLimits.id:
            parse_detail_scale_limits(cd)
        elif id == DtiFormat.Chunks.Objects.Object.DensityFactor.id:
            parse_detail_density_factor(cd)
        elif id == DtiFormat.Chunks.Objects.Object.Flags.id:
            parse_detail_flags(cd)
        else:
            print('! unknow block {}'.format(hex(id)))
        p += sz
    dump += '\n'


def parse_detail_objects(d):
    global dump
    dump += '; objects\n\n'
    p = 0
    dataSize = len(d)
    objectCount = 0
    while p < dataSize:
        (detId, detSize), p = u('II', d, p)
        dump += '[object_{0:0>2}]\n'.format(detId)
        objectCount += 1
        parse_detail_object(d[p : p + detSize])
        p += detSize
    return objectCount


def parse_color(d):
    global dump
    dump += '; colors\n\n'
    (colorCount, ), p = u('B', d, 0)
    for colorID in range(colorCount):
        dump += '[color_{0:0>2}]\n'.format(colorID)
        (B, G, R, unknow, referenceCount), p = u('5B', d, p)
        dump += '  rgb        = {0}, {1}, {2}\n'.format(R, G, B)
        refList = []
        for i in range(referenceCount):
            reference, p = xray_utils.parse_string(d, p)
            refList.append(reference)
        dump += '  references = '
        refListSize = len(refList)
        for n, ref in enumerate(refList):
            if n != refListSize - 1:
                dump += '"{0}", '.format(ref)
            else:
                dump += '"{0}"\n\n'.format(ref)
    return colorCount


def parse_main(d):
    p = 0
    dataSize = len(d)
    while p < dataSize:
        (id, cmprs, size), p = u('HHI', d, p)
        cd = d[p : p + size]
        if id == DtiFormat.Chunks.Objects.id:
            objectCount = parse_detail_objects(cd)
        elif id == DtiFormat.Chunks.ColorIndex.id:
            colorCount = parse_color(cd)
        else:
            xray_utils.un_blk(id)
        p += size
    return objectCount, colorCount


version = (0, 0, 2)    # version of dump_dti.py
parser = OptionParser(usage='Usage: dump_dti.py <file> [options]')
parser.add_option("-s",
                  "--save",
                  action='store_true',
                  default=False,
                  help='save dump in file')
(options, argument) = parser.parse_args()
if not argument:
    parser.print_help()
    print()
    os.system('pause')
else:
    if not os.access(argument[0], os.F_OK):
        print('\n  file "{0}" not found!\n'.format(argument[0]))
    else:
        f = open(argument[0], mode='rb')
        s = f.read()
        f.close()
        dump = ''
        objectCount, colorCount = parse_main(s)
        objectsSection = '[objects]\n'
        for ob in range(objectCount):
            objectsSection += '  object_{0:0>2}\n'.format(ob)
        objectsSection += '\n'
        colorsSection = '[colors]\n'
        for ob in range(colorCount):
            colorsSection += '  color_{0:0>2}\n'.format(ob)
        colorsSection += '\n'
        if options.save:
            dumpFileName = 'dump_' + argument[0].split('.')[0] + '.ltx'
            dumpFile = open(dumpFileName, 'w')
            dumpFile.write(objectsSection + colorsSection + dump)
            dumpFile.close()
            print('\n  dump save in {}\n'.format(dumpFileName))
        else:
            print(dump)
    os.system('pause')

