import xray_utils, parse_object


d = xray_utils.read_bin_file('0.object')
parse_object.parse_main(d)
input()