from tkinter import *
from tkinter.filedialog import askdirectory

janela = Tk()

#Escolhendo diretorio para salvar
campo_pasta = Entry(janela, width=50, state="disabled")
campo_pasta.place(x=160,y=8)
pasta=askdirectory

def escolher_pasta():
    campo_pasta.config(state="normal")
    global pasta
    pasta = askdirectory()
    campo_pasta.delete(0, END)
    campo_pasta.insert(END, pasta)
    campo_pasta.config(state="disabled")

botao_caminho = Button(janela, text="Escolha a pasta: ", width=15, background="lightblue", command=escolher_pasta)
botao_caminho.place(x=25,y=4)