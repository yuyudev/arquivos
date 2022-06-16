from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilename
import pandas as pd
from codecs import open as codeopen

#Interface
janela = Tk()
janela.title("Tratamento dos dados de ASO")
janela.geometry("500x300")

#Escolhendo diretorio para salvar
campo_pasta = Entry(janela, width=50, state="disabled")
campo_pasta.place(x=160,y=8)
pasta=askdirectory
def escolher_pasta():

    campo_pasta.config(state="normal")
    global pasta
    pasta = askdirectory()
    campo_pasta.insert(END, pasta)
    campo_pasta.config(state="disabled")

botao_caminho = Button(janela, text="Escolha a pasta: ", width=15, background="lightblue", command=escolher_pasta)
botao_caminho.place(x=25,y=4)

#ComboBox clientes
lb_clientes = Label(janela, text="Selecione o cliente:")
lb_clientes.place(x=200,y=70)
listaClientes = ["BanQi", "Privalia"]
cb_clientes = ttk.Combobox(janela, values=listaClientes)
cb_clientes.set("BanQi")
cb_clientes.place(x=180,y=90)

#Definindo datas
lb_periodo = Label(janela, text="Selecione o período dos dados:")
lb_periodo.place(x=170,y=125)
lb_inicio = Label(janela, text="Início: ")
lb_inicio.place(x=180,y=150)
dataInicial = Entry(janela, width=10)
dataInicial.place(x=180,y=170)
lb_final = Label(janela, text="Final: ")
lb_final.place(x=270,y=150)
dataFinal = Entry(janela, width=10)
dataFinal.place(x=270,y=170)

#Funções de tratamento
def wrap_text_file():    
    file = codeopen(
        askopenfilename(filetypes=[('CSV Files', '*.csv')]), 
        encoding='utf-8')
    yield file
    file.close()

def tratar_banqi():
    arquivoPasta = next(wrap_text_file())
    arquivo = pd.read_csv(arquivoPasta, sep = ",")
    datas = arquivo.T[str(dataFinal.get()):str(dataInicial.get())]
    termos = arquivo["Term"]
    posicoes = arquivo.T[str(dataFinal.get()):str(dataInicial.get())]
    x = posicoes.to_numpy()

    #seleção dos dados de datas

    datas.reset_index(inplace=True)
    datas = datas["index"]

    colunaTermos = column = termos
    colunaDatas = column = datas


    #tratamento dos dados

    dados = []
    chave = []

    for i in x:
        for y in i:
            chave.append(y)
    i = 0
    j = 0

    for data in datas:
        for termo in termos:      
            dados.append((data,termo,chave[i]))
            i = i + 1
        

    base = pd.DataFrame(dados, columns = ["datas", "termos", "posição"])
    base.to_csv(pasta+"/nova_base.csv")

def tratar_privalia():
    arquivoPasta = next(wrap_text_file())
    arquivo = pd.read_csv(arquivoPasta, encoding = "utf8", sep = ",")
    datas = arquivo.T[str(dataFinal.get()):str(dataInicial.get())]
    termos = arquivo["Term"]
    appId = arquivo["App ID"].values
    posicoes = arquivo.T[str(dataFinal.get()):str(dataInicial.get())]
    x = posicoes.to_numpy()

    #seleção dos dados de datas

    datas.reset_index(inplace=True)
    datas = datas["index"]

    colunaTermos = column = termos
    colunaAppID = column = appId
    colunaDatas = column = datas

    #tratamento dos dados

    dados = []
    chave = []

    for i in x:
        for y in i:
            chave.append(y)
    i = 0
    j = 0

    for data in datas:
        for termo in termos:      
            dados.append((data,termo,appId[j],chave[i]))
            j = j + 1
            i = i + 1
        j=0

    base = pd.DataFrame(dados, columns = ["datas", "termos", "id", "posição"])
    base.to_csv(pasta+"/nova_base.csv")

def tratar_dados():
    cliente = cb_clientes.get()
    if cliente == "BanQi":
        tratar_banqi()
    elif cliente == "Privalia":
        tratar_privalia()

botao = Button(janela, text="Go!", width=5, height=1, background="pink", command=tratar_dados)
botao.place(x=230,y=200)

janela.mainloop()