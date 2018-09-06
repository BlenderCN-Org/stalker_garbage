import utils, parse_wallmarks

data = utils.read_bin_file('c:\\level.wallmarks')
parse_wallmarks.parse_main(data)