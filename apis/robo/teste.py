from tkinter import *
from tkinter import ttk, Entry
from tkinter.filedialog import askdirectory

app = Tk()
app.geometry("500x500")

caminho=Entry(app, width=15)
caminho.pack()

def pasta():
    path = askdirectory()
    print(path)

botao = Button(app, background="pink", command=pasta)
botao.pack()

app.mainloop()