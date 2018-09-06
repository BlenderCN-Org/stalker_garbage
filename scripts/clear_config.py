import os


def clear_config(fileName):
    inputFile = open(fileName, 'r')
    inputConfig = inputFile.read()
    inputFile.close()
    outputFile = open('output\\' + fileName, 'w')
    configs = []
    
    for line in inputConfig.split('\n'):
        newLine = ''
        for char in line:
            if char == ';' or char == '/':
                break
            elif char == ' ' or char == '\t':
                continue
            else:
                if char == ',':
                    char = ', '
                newLine += char
        if len(newLine) != 0:
            if newLine[0] == '[':
                configs.append((newLine, True))
            elif newLine.startswith('#include') == True:
                configs.append((newLine, True))
            else:
                values = newLine.split('=')
                configs.append((values[0], values[1]))
    
    maxLenValue = 0
    for value in configs:
        if value[0][0] != '[':
            lenValue = len(value[0])
            if lenValue > maxLenValue:
                maxLenValue = lenValue
    
    for line in configs:
        if line[0][0] == '[':
            outputFile.write(line[0] + '\n')
        elif line[0].startswith('#include'):
            outputFile.write(line[0][:8] + ' ' + line[0][8:] + '\n')
        else:
            var = line[0] + (maxLenValue - len(line[0])) * ' ' + ' = ' + line[1] + '\n'
            outputFile.write(var)
    outputFile.close()


if not os.access('output\\', os.F_OK):
    os.makedirs('output\\')

for file in os.listdir('.'):
    if file.split('.')[-1] == 'ltx':
        clear_config(file)
os.system("PAUSE")

