from struct import *
import parse_visual, parse_geom, import_mesh

f = open('c:\\level', 'rb')
s = f.read()
f.close()

p = 0
################################################################################
while p < len(s):
    block_id = unpack('i', s[p : p + 4])[0]
    p += 4
    
    block_size = unpack('i', s[p : p + 4])[0]
    p += 4
    
    if block_id == 3:
        visuals = parse_visual.parse(s[p : p + block_size])
    p += block_size

################################################################################
f = open('c:\\level.geom', 'rb')
s = f.read()
f.close()
vertices_buffer, indices_buffer = parse_geom.parse_geom(s)

for visual in visuals:
    if visual != None:
        v_set = visual[0]
        v_base = visual[1]
        v_count = visual[2]
        vert_list = vertices_buffer[v_set][v_base : v_base + v_count]
        
        i_set = visual[3]
        i_base = visual[4]
        i_count = visual[5]
        index_list = indices_buffer[i_set][i_base : v_base + i_count]
        
        print(vert_list)
        
        # import_mesh.crete_mesh('geom_name', vert_list, index_list)

