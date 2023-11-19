from tkinter import *
from tkinter import filedialog, simpledialog
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter.ttk import *
import re

root = Tk()
root.title('Text Editor')

# scrollable text
textPad = ScrolledText(root, width=100, height=50)
filename = ''
current_content = ""

# functions
def newFile():
    global filename, current_content
    if len(textPad.get('1.0', END + '-1c')) > 0:
        if messagebox.askyesno("SAVE", "Do you want to save?"):
            saveFile()
        else:
            textPad.delete(0.0, END)
    root.title("TEXT EDITOR")
    current_content = ""

def saveFile():
    global current_content
    f = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if f is not None:
        data = textPad.get('1.0', END)
        try:
            f.write(data)
            current_content = data
        except:
            messagebox.showerror(title="Oops!!", message="Unable to save file!")

def saveAs():
    global current_content
    f = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    t = textPad.get(0.0, END)
    try:
        f.write(t.rstrip())
        current_content = t
    except:
        messagebox.showerror(title="Oops!!", message="Unable to save file!")

def openFile():
    global current_content
    f = filedialog.askopenfile(parent=root, mode='r')
    t = f.read()
    textPad.delete(0.0, END)
    textPad.insert(0.0, t)
    current_content = t

def about_command():
    label = messagebox.showinfo("About", "Just Another TextPad \n No rights left to reserve")

def handle_click(event):
    textPad.tag_config('Found', background='white', foreground='grey')

def find_pattern():
    textPad.tag_remove("Found", '1.0', END)
    find = simpledialog.askstring("Find....", "Enter text:")
    if find:
        idx = '1.0'
        while 1:
            idx = textPad.search(find, idx, nocase=1, stopindex=END)
            if not idx:
                break
            lastidx = '%s+%dc' % (idx, len(find))
            textPad.tag_add('Found', idx, lastidx)
            idx = lastidx
    textPad.tag_config('Found', foreground='white', background='black')
    textPad.bind("<1>", handle_click)

def copy_text():
    textPad.clipboard_clear()
    textPad.clipboard_append(textPad.selection_get())

def cut_text():
    copy_text()
    textPad.delete(SEL_FIRST, SEL_LAST)

def paste_text():
    textPad.insert(INSERT, textPad.clipboard_get())

def printme():
    label = messagebox.showinfo("Text", "Welcome to the text editor")

def exit_command():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# creating menu
menuM = Menu(root)
root.configure(menu=menuM)

fileM = Menu(menuM)
menuM.add_cascade(label='File', menu=fileM)
fileM.add_command(label='New', command=newFile)
fileM.add_command(label='Open', command=openFile)
fileM.add_command(label='Save', command=saveFile)
fileM.add_command(label='Save As...', command=saveAs)
fileM.add_separator()
fileM.add_command(label='Exit', command=exit_command)

editM = Menu(menuM)
menuM.add_cascade(label='Edit', menu=editM)
editM.add_command(label='Cut', command=cut_text)
editM.add_command(label='Copy', command=copy_text)
editM.add_command(label='Paste', command=paste_text)

viewM = Menu(menuM)
menuM.add_cascade(label='View', menu=viewM)
viewM.add_command(label='Text', command=printme)

aboutM = Menu(menuM)
menuM.add_cascade(label='About', menu=aboutM)
aboutM.add_command(label='About', command=about_command)

findM = Menu(menuM)
menuM.add_cascade(label='Find', menu=findM)
findM.add_command(label='Find', command=find_pattern)

textPad.pack()

root.mainloop()
