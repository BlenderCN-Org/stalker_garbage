import xray_utils, parse_details


data = xray_utils.read_bin_file('level.details')
parse_details.parse_main(data)
input()