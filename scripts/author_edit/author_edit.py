from struct import *
from tkinter import *
import os

def edit_author(event):
    for i in os.listdir():
        ext = os.path.splitext(i)[1]
        if ext == '.object':
            save_authors(i)


def return_time(s):
    p = 0
    ch = unpack('s', s[p : p + 1])[0]
    p += 1
    author = ''
    while ch != b'\x00':
        author += str(ch)[2:-1]
        ch = unpack('s', s[p : p + 1])[0]
        p += 1
    date_1 = s[p : p + 4]
    p += 4
    ch = unpack('s', s[p : p + 1])[0]
    p += 1
    modifer = ''
    while ch != b'\x00':
        modifer += str(ch)[2:-1]
        ch = unpack('s', s[p : p + 1])[0]
        p += 1
    date_2 = s[p : p + 4]
    return  date_1, date_2


def save_authors(path):
    
    f = open(path, 'rb')
    s = f.read()
    file_size = len(s) - 8
    f.close()
    
    p = 8
    while p < len(s):
        block_id = unpack('i', s[p : p + 4])[0]
        p += 4
        block_size = unpack('i', s[p : p + 4])[0]
        p += 4
    
        if block_id == 0x922:
    
            data = s[p : p + block_size]
            new_author = b'\\\\COMP\\Pavel_Blend'
            new_modifer = b'Python 3.3.5.'
            
            date_1, date_2 = return_time(data)
            
            new_block = new_author+b'\x00'+date_1+new_modifer+b'\x00'+date_2
            new_size = len(new_author) + 4 + len(new_modifer) + 4 + 2
            
            new_file_size = file_size - block_size + new_size
            
            new_file = s[0 : 4]
            new_file += pack('i', new_file_size)
            new_file += s[8 : p - 4]
            new_file += pack('i', new_size)
            new_file += new_block
            
            save_f = open('new.object', 'wb')
            save_f.write(new_file)
            save_f.close()
    
        p += block_size

root_width = 300
root_height = root_width // 3
root = Tk()
root.minsize(width=root_width, height=root_height)
root.maxsize(width=300, height=150)
root.resizable(width=False, height=False)
x = (root.winfo_screenwidth()) / 2
y = (root.winfo_screenheight()) / 2
root.geometry('+%d+%d' % (x - (root_width/2), y - (root_height/2) - 40))
root.title('Edit Author')

lab1 = Label(root, text='Author Name:')
lab1.pack()

ent1 = Entry(root, width=32)
ent1.pack()

lab2 = Label(root, text='Edit Name:')
lab2.pack()

ent2 = Entry(root, width=32)
ent2.pack()

but = Button(root, text='Save')
but.bind('<Button-1>', edit_author)
but.pack()

root.mainloop()