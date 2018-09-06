path = ''
name = 'w_pm'
ext = '.ltx'
file = path + name + ext
syffix = '_new'
new_file = path + name + syffix + ext
f = open(file, 'r')
s = f.read()
f.close()
new = open(new_file, 'w')
tabs = ('\t', ' ')
temp = ''

for i in s:
    if i in tabs:
        pass
    else:
        temp += i

i = 0
temp_2 = ''
while i < len(temp):
    if temp[i] == ';':
        i += 1
        while i < len(temp) and temp[i] != '\n':
            i += 1
    else:
        temp_2 += temp[i]
        i += 1

temp_3 = ''
i = 0
while i < len(temp_2):
    if temp_2[i] == '\n':
        temp_3 += temp_2[i]
        i += 1
        while i < len(temp_2) and temp_2[i] == '\n':
            i += 1
    else:
        temp_3 += temp_2[i]
        i += 1

new.write(temp_3)
new.close()
input()