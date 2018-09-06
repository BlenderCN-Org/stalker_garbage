f1 = open('old_file.bin', 'rb')
s1 = f1.read()
f1.close()

f2 = open('new_file.bin', 'rb')
s2 = f2.read()
f2.close()

if len(s1) != len(s2):
    print('lengths files not equial')
else:
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            print(i, hex(i))
input()

