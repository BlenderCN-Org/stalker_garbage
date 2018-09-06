import stalker_utils, parse_level

d = stalker_utils.file_read('level')
dSz = len(d)
_p = 0
while _p < dSz:
    id, sz, blckDt, _p = stalker_utils.block_read(d, _p)
    if id == 0x0002:
        parse_level.parse_textures(blckDt)
input()