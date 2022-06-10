from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd

janela = Tk()
janela.title("Tratamento dos dados de ASO")
janela.geometry("500x300")


listaClientes = ["BanQi", "Privalia"]

lb_clientes = Label(janela, text="Selecione o cliente:")
lb_clientes.pack()

cb_clientes = ttk.Combobox(janela, values=listaClientes)
cb_clientes.set("BanQi")
cb_clientes.pack()

banqi = cb_clientes.set("BanQi")
privalia = cb_clientes.set("Privalia")


lb_periodo = Label(janela, text="Selecione o período dos dados:")
lb_periodo.pack()



lb_inicio = Label(janela, text="Início: ")
lb_inicio.pack()
dataInicial = Entry(janela, width=10)
dataInicial.pack()



lb_final = Label(janela, text="Final: ")
lb_final.pack()
dataFinal = Entry(janela, width=10)
dataFinal.pack()

      #  "2022-06-07":"2022-05-08"
    
def tratar_banqi():
    arquivoPasta = filedialog.askopenfile()
    arquivo = pd.read_csv(arquivoPasta, encoding = "UTF-8", sep = ",")
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
    base.to_csv("C:/Users/User/Documents/git-e-github/Meus arquivos/apis/robo/nova_base.csv", encoding="UTF-8")

def tratar_privalia():
    arquivoPasta = filedialog.askopenfile()
    arquivo = pd.read_csv(arquivoPasta, encoding = "UTF-8", sep = ",")
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
    base.to_csv("C:/Users/User/Documents/git-e-github/Meus arquivos/apis/robo/nova_base.csv")

def tratar_dados():
    cliente = cb_clientes.get()
    if cliente == "BanQi":
        tratar_banqi()
    elif cliente == "Privalia":
        tratar_privalia()


botao = Button(janela, text="Go!", width=5, height=1, background="lightblue", command=tratar_dados)
botao.pack()


janela.mainloop()