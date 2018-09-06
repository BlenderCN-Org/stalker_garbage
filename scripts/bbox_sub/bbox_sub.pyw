import os, time
from struct import unpack, pack
from tkinter import *


def bbox_split(d, name):
    p = 0
    subdiv = sc.get()
    data0 = d[p : p + 12]
    p += 12
    minX, minY, minZ, maxX, maxY, maxZ = unpack('6f', d[p : p + 24])
    p += 24
    data1 = d[p : ]
    x = (maxX - minX) / subdiv
    z = (maxZ - minZ) / subdiv
    row = 1
    col = 0
    for i in range(1, subdiv ** 2 + 1):
        if i > subdiv and i % subdiv == 1:
            row += 1
            col -= subdiv - 1
        else:
            col += 1
        bboxNew = (minX + x * (col - 1),
                   minY,
                   minZ + z * (row - 1),
                   minX + x * col,
                   maxY,
                   minZ + z * row)
        f = open(outDir + '\\' + name + '{}{}'.format(row, col), 'wb')
        f.write(data0)
        dataBbox = pack('6f', bboxNew[0], bboxNew[1], bboxNew[2],
                              bboxNew[3], bboxNew[4], bboxNew[5])
        f.write(dataBbox)
        f.write(data1)
        f.close()


def run(event):
    startTime = time.time()
    for file in os.listdir(inDir):
        ext = file.split('.')[-1]
        if ext == 'cform':
            f = open(inDir + '\\' + file, 'rb')
            s = f.read()
            f.close()
            bbox_split(s, file)
    timer.configure(text='Time: {}'.format(time.time() - startTime))


version = (0, 1)
inDir = 'input'
outDir = 'output'
win = Tk()
win['bg'] = '#898989'
win.resizable(height=False, width=False)
win.minsize(width=240, height=120)
win.maxsize(width=240, height=120)
win.title('BBox Subdivider v{}.{}'.format(version[0], version[1]))
x = (win.winfo_screenwidth()) / 2
y = (win.winfo_screenheight()) / 2
win.geometry('+%d+%d' % (x - 120, y - 140))
fr = Frame(win, bg='#898989', width=240, height=320)

sc = Scale(fr,
           orient=HORIZONTAL,
           length=120,
           from_=2,
           to=8,
           tickinterval=1,
           resolution=1,
           label='   Subdivide Count:',
           font=('font', 8, 'bold'),
           activebackground='#aaaaaa',
           background='#898989',
           bd=1,
           highlightbackground='#898989',
           sliderlength=20,
           troughcolor='#aaaaaa')

sc.grid(row = 0, column = 0, padx = 60)
but = Button(fr,
             text='Create',
             width=13,
             height=1,
             bg='#A0A0A0',
             activebackground='#B3B3B3',
             font=('font', 8, 'bold'))
but.bind('<Button-1>', run)
but.grid(row = 1, column = 0, padx = 60)
timer = Label(fr, text='', font=('font', 8, 'bold'), background='#898989')
timer.grid(row=2, column=0, padx=60)
fr.grid(row=0, column=0)
win.mainloop()
