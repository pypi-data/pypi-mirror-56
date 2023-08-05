from tkinter import *


row = 0
col = 0
__root = Tk()
__root.overrideredirect(True)


e = Entry(__root,  font=(None, 48))

e.config(width=15)
e.grid(row=row, column=col, padx=0, pady=0)
__root.geometry('+%d+%d' % (100, 100))
while True:
    __root.update_idletasks()
    pass
    __root.update()
