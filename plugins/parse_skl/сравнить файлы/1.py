f1 = open('old.skl', 'rb')
f2 = open('new.skl', 'rb')
d1 = f1.read()
d2 = f2.read()
if len(d1) == len(d2):
    p = 0
    fileSize = len(d1)
    while p < fileSize:
        if d1[p] != d2[p]:
            print(p)
        p += 1
else:
    print('len1 != len2')
f1.close()
f2.close()
input()

# name + 15
#           type Fx     0x0/0x1
#           stop at end 0x0/0x2
#           no mix      0x0/0x4
#           sync part   0x0/0x8
# + 1 bone part ID (0xff - all bones)
# + 1 start bone ID (0xff - None)
# name + 17 speed
# accure speed + 4
# falloff + 4
# power + 4
# 
