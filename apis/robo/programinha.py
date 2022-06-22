#Importando bibliotecas de autenticação do Google
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#Outras importações
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import pandas as pd
from codecs import open as codeopen

#API Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main(data):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId='1A5kQ_wqY_Tml_Utsz2QiRZkKhWQyiNnc_vcFWUcJdE0',
                                    range='android keywords ranking!B:E').execute()
    values = result.get('values', [])
    teste = pd.DataFrame(values)
    local = str((teste.iloc[-1].name+2))

    result = sheet.values().update(spreadsheetId='1A5kQ_wqY_Tml_Utsz2QiRZkKhWQyiNnc_vcFWUcJdE0',
                                range='android keywords ranking!B'+local, valueInputOption='USER_ENTERED',
                                body={'values': data}).execute()

#Interface
janela = Tk()
janela.title("Tratamento dos dados de ASO")
janela.geometry("500x300")

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
    #Recebendo as datas
    retornoDataFinal=dataFinal.get()
    retornoDataInicial=dataInicial.get()
    diaInicial=retornoDataInicial[0:2]
    mesI=retornoDataInicial[3:5]
    anoI=retornoDataInicial[6:10]
    diaFinal=retornoDataFinal[0:2]
    mesF=retornoDataFinal[3:5]
    anoF=retornoDataFinal[6:10]
    dataInicialTratada=f"{anoI}-{mesI}-{diaInicial}"
    dataFinalTratada=f"{anoF}-{mesF}-{diaFinal}"

    #Seleção das colunas
    arquivoPasta = next(wrap_text_file())
    arquivo = pd.read_csv(arquivoPasta, sep = ",")
    datas = arquivo.T[dataFinalTratada:dataInicialTratada].fillna('')
    termos = arquivo["Term"].fillna('')
    posicoes = arquivo.T[dataFinalTratada:dataInicialTratada].fillna('').values

    #Seleção dos dados de datas
    datas.reset_index(inplace=True)
    datas = datas["index"]

    #Definição das colunas
    colunaTermos = column = termos
    colunaDatas = column = datas

    #Tratamento dos dados
    dados = []
    chave = []

    for i in posicoes:
        for y in i:
            if type(y) == str:
                chave.append(y)
            else:
                chave.append('%.0f'%y)
    i = 0
    j = 0

    #Adicionando novos dados
    for data in datas:
        for termo in termos:      
            dados.append((str(termo),str(chave[i]),str(data)))
            j = j + 1
            i = i + 1
        j=0

    #Criação do arquivo final
    base = pd.DataFrame(dados, columns = ["termos", "posição","datas"])
    base.sort_values(by=['datas'], inplace=True)
    print(base)
    base_new = base.values.tolist()
    main(base_new)

def tratar_privalia():
    #Recebendo as datas
    retornoDataFinal=dataFinal.get()
    retornoDataInicial=dataInicial.get()
    diaInicial=retornoDataInicial[0:2]
    mesI=retornoDataInicial[3:5]
    anoI=retornoDataInicial[6:10]
    diaFinal=retornoDataFinal[0:2]
    mesF=retornoDataFinal[3:5]
    anoF=retornoDataFinal[6:10]
    dataInicialTratada=f"{anoI}-{mesI}-{diaInicial}"
    dataFinalTratada=f"{anoF}-{mesF}-{diaFinal}"

    #Seleção das colunas
    arquivoPasta = next(wrap_text_file())
    arquivo = pd.read_csv(arquivoPasta, sep = ",")
    datas = arquivo.T[dataFinalTratada:dataInicialTratada].fillna('')
    termos = arquivo["Term"].fillna('')
    appId = arquivo["App ID"].fillna('').values
    posicoes = arquivo.T[dataFinalTratada:dataInicialTratada].fillna('').values

    #Seleção dos dados de datas
    datas.reset_index(inplace=True)
    datas = datas["index"]

    #Definição das colunas
    colunaTermos = column = termos
    colunaAppID = column = appId
    colunaDatas = column = datas

    #Tratamento dos dados
    dados = []
    chave = []

    for i in posicoes:
        for y in i:
            if type(y) == str:
                chave.append(y)
            else:
                chave.append('%.0f'%y)
    i = 0
    j = 0

    #Adicionando novos dados
    for data in datas:
        for termo in termos:      
            dados.append((str(termo),str(appId[j]),str(chave[i]),str(data)))
            j = j + 1
            i = i + 1
        j=0

    #Criação do arquivo final
    base = pd.DataFrame(dados, columns = ["termos", "id", "posição","datas"])
    base.sort_values(by=['datas'], inplace=True)
    base_new = base.values.tolist()
    main(base_new)

def tratar_dados():
    cliente = cb_clientes.get()
    if cliente == "BanQi":
        tratar_banqi()
    elif cliente == "Privalia":
        tratar_privalia()

botao = Button(janela, text="Go!", width=5, height=1, background="pink", command=tratar_dados)
botao.place(x=230,y=200)

janela.mainloop()