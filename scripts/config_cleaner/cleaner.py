f = open('w_abakan.ltx', 'r')
for i in f.readlines():
    centres = []
    try:
        centres.append(i.index('='))
    except:
        centres.append(0)
center = (max(centres))
new = open('1.ltx', 'w')
f.close()
f = open('w_abakan.ltx', 'r')
for i in f.readlines():
    line = ''
    for j in i:
        if j == ';':
            break
        else:
            if j != ' ' and j != '\n' and j != '\t':
                if j == '=':
                    line += (center - len(line)) * ' '
                    line += j + ' '
                else:
                    line += j
    if len(line) and len(i):
        new.write(line + '\n')
new.close()
f.close()
input()