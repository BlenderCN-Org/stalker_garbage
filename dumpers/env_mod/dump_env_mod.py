import os
from xray_utils import unpack_data as u
from optparse import OptionParser


def parse_environment_modificator(data):    # SoC Format
    (posX, posY, posZ,
    radius,
    power,
    viewDistance,
    fogR, fogG, fogB,
    fogDensity,
    ambR, ambG, ambB,
    skyR, skyG, skyB,
    hemR, hemG, hemB), p = u('19f', data, 0)
    global dump
    dump += '  position      = {:.6}, {:.6}, {:.6}\n'.format(posX, posY, posZ)
    dump += '  radius        = {:.6}\n'.format(radius)
    dump += '  power         = {:.6}\n'.format(power)
    dump += '  view_distance = {:.6}\n'.format(viewDistance)
    dump += '  fog_color     = {:.6}, {:.6}, {:.6}\n'.format(fogR, fogG, fogB)
    dump += '  fog_density   = {:.6}\n'.format(fogDensity)
    dump += '  ambient       = {:.6}, {:.6}, {:.6}\n'.format(ambR, ambG, ambB)
    dump += '  sky_color     = {:.6}, {:.6}, {:.6}\n'.format(skyR, skyG, skyB)
    dump += '  hemi_color    = {:.6}, {:.6}, {:.6}\n\n'.format(hemR, hemG, hemB)


def parse_main(data):
    global dump
    dataSize = len(data)
    envModCount = dataSize // 84
    dump += '[modifers]\n'
    for i in range(envModCount):
        dump += '  modifer_{0:0>2}\n'.format(i)
    dump += '\n'
    p = 0    # position
    while p < dataSize:
        (id, size), p = u('II', data, p)
        dump += '[modifer_{0:0>2}]\n'.format(id)
        parse_environment_modificator(data[p : p + size])
        p += size


dump = ''
parser = OptionParser(usage='Usage: dump_env_mod.py <file> [options]')
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
        data = f.read()
        f.close()
        dump = ''
        parse_main(data)
        if options.save:
            dumpFileName = 'dump_' + argument[0].split('.')[0] + '_env_mod' + '.ltx'
            dumpFile = open(dumpFileName, 'w')
            dumpFile.write(dump)
            dumpFile.close()
            print('\n  dump save in {}\n'.format(dumpFileName))
        else:
            print(dump)
    os.system('pause')

