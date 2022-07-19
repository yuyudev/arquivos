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
import numpy as np
import pandas as pd
from codecs import ignore_errors, open as codeopen

#Interface
janela = Tk()
janela.title("Tratamento dos dados de ASO")
janela.geometry("500x300")

#Menus
nb=ttk.Notebook(janela)
nb.place(x=0,y=0,width=500,height=300)

#Aba Posicionamento do APP
def pagina_posicionamento_app():
    #ComboBox clientes
    posicionamento_app=Frame(nb)
    nb.add(posicionamento_app,text='Posicionamento do APP')
    lb_clientes = Label(posicionamento_app, text="Selecione o cliente:")
    lb_clientes.pack()
    listaClientes = ["BanQi", "Privalia"]
    cb_clientes = ttk.Combobox(posicionamento_app, values=listaClientes)
    cb_clientes.set("BanQi")
    cb_clientes.pack()

    lb_os = Label(posicionamento_app, text="Selecione o Sistema Operacional:")
    lb_os.pack()
    listaos = ["Android", "Apple"]
    cb_os = ttk.Combobox(posicionamento_app, values=listaos)
    cb_os.set("Android")
    cb_os.pack()

    #API Google Sheets - Preenchimento
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def google_sheets(data):
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
        sistema_operacional=cb_os.get()
        cliente=cb_clientes.get()
        if cliente == 'Privalia':
            sheet_privalia = service.spreadsheets()
            if sistema_operacional == 'Android':
                result_privalia = sheet_privalia.values().get(spreadsheetId='1A5kQ_wqY_Tml_Utsz2QiRZkKhWQyiNnc_vcFWUcJdE0',
                range='android keywords ranking!B:E').execute()
                values_privalia = result_privalia.get('values', [])
                df = pd.DataFrame(values_privalia)
                local_privalia = str((df.iloc[-1].name+2))
                result_privalia = sheet_privalia.values().update(spreadsheetId='1A5kQ_wqY_Tml_Utsz2QiRZkKhWQyiNnc_vcFWUcJdE0',
                range='android keywords ranking!B'+local_privalia, valueInputOption='USER_ENTERED',
                body={'values': data}).execute()
            elif sistema_operacional == 'Apple':
                result_privalia = sheet_privalia.values().get(spreadsheetId='1A5kQ_wqY_Tml_Utsz2QiRZkKhWQyiNnc_vcFWUcJdE0',
                range='iOS keywords ranking vs!B:E').execute()
                values_privalia = result_privalia.get('values', [])
                df = pd.DataFrame(values_privalia)
                local_privalia = str((df.iloc[-1].name+2))
                result_privalia = sheet_privalia.values().update(spreadsheetId='1A5kQ_wqY_Tml_Utsz2QiRZkKhWQyiNnc_vcFWUcJdE0',
                range='iOS keywords ranking vs!B'+local_privalia, valueInputOption='USER_ENTERED',
                body={'values': data}).execute()

        elif cliente == 'BanQi':
            sheet_banqi = service.spreadsheets()
            if sistema_operacional == 'Android':
                result_banqi = sheet_banqi.values().get(spreadsheetId='1VcEG2qxqmFnERd1VE_N_OH1J3em9nDXgrr1HVcp1xcw',
                range='kw android semana!A:C').execute()
                values_banqi = result_banqi.get('values', [])
                df = pd.DataFrame(values_banqi)
                local_banqi = str((df.iloc[-1].name+2))
                result_banqi = sheet_banqi.values().update(spreadsheetId='1VcEG2qxqmFnERd1VE_N_OH1J3em9nDXgrr1HVcp1xcw',
                range='kw android semana!A'+local_banqi, valueInputOption='USER_ENTERED',
                body={'values': data}).execute()
            elif sistema_operacional == 'Apple':
                result_banqi = sheet_banqi.values().get(spreadsheetId='1VcEG2qxqmFnERd1VE_N_OH1J3em9nDXgrr1HVcp1xcw',
                range='kw ios semana!A:C').execute()
                values_banqi = result_banqi.get('values', [])
                df = pd.DataFrame(values_banqi)
                local_banqi = str((df.iloc[-1].name+2))
                result_banqi = sheet_banqi.values().update(spreadsheetId='1VcEG2qxqmFnERd1VE_N_OH1J3em9nDXgrr1HVcp1xcw',
                range='kw ios semana!A'+local_banqi, valueInputOption='USER_ENTERED',
                body={'values': data}).execute()            

    #Definindo datas
    lb_periodo = Label(posicionamento_app, text="Selecione o período dos dados:")
    lb_periodo.pack()
    lb_inicio = Label(posicionamento_app, text="Início: ")
    lb_inicio.pack()
    dataInicial = Entry(posicionamento_app, width=10)
    dataInicial.pack()
    lb_final = Label(posicionamento_app, text="Final: ")
    lb_final.pack()
    dataFinal = Entry(posicionamento_app, width=10)
    dataFinal.pack()

    #Funções de tratamento
    def wrap_text_file():    
        file = codeopen(
            askopenfilename(filetypes=[('CSV Files', '*.csv')]), 
            encoding='utf-16')
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

        #Lendo o arquivo
        arquivo_pasta = next(wrap_text_file())
        arquivo = pd.read_csv(arquivo_pasta, sep = "	")
        
        #Coluna datas
        datas = arquivo.T[dataFinalTratada:dataInicialTratada].fillna('')
        
        #Coluna termos
        termos = arquivo["Term"].fillna('')
        
        #Coluna posicoes
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
        for lista_posicoes in posicoes:
            for posicao in lista_posicoes:
                if type(posicao) == str:
                    chave.append(posicao)
                else:
                    chave.append('%.0f'%posicao)

        #Adicionando novos dados
        i = 0
        j = 0
        for data in datas:
            for termo in termos:      
                dados.append((str(termo),str(data),str(chave[i])))
                j = j + 1
                i = i + 1
            j=0

        #Criação do arquivo final
        base = pd.DataFrame(dados, columns = ["termos","datas", "posição"])
        base.sort_values(by=["datas"], inplace=True)
        base_new = base.values.tolist()
        google_sheets(base_new)

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

        #Lendo o arquivo
        arquivo_pasta = next(wrap_text_file())
        arquivo = pd.read_csv(arquivo_pasta, sep='	')

        #Coluna datas
        datas = arquivo.T[dataFinalTratada:dataInicialTratada].fillna('')
        
        #Coluna termos
        termos = arquivo["Term"].fillna('')

        #Coluna App ID
        sistema_operacional = cb_os.get()
        if sistema_operacional == 'Android':
            appId = arquivo['App ID'].fillna('').values
        elif sistema_operacional == 'Apple':
            appId = arquivo['App ID'].fillna('0').astype('int').replace(0,'').values

        #Coluna posicoes
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
        for lista_posicoes in posicoes:
            for posicao in lista_posicoes:
                if type(posicao) == str:
                    chave.append(posicao)
                else:
                    chave.append('%.0f'%posicao)

        #Adicionando novos dados
        i = 0
        j = 0
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
        google_sheets(base_new)

    def tratar_dados():
        cliente = cb_clientes.get()
        if cliente == "BanQi":
            tratar_banqi()
        elif cliente == "Privalia":
            tratar_privalia()

    botao = Button(posicionamento_app, text="Go!", width=5, height=1, background="pink", command=tratar_dados)
    botao.pack()
pagina_posicionamento_app()

#Aba Categoria
def pagina_categoria():
    categoria=Frame(nb)
    nb.add(categoria,text='Categoria')

    #ComboBox clientes
    lb_clientes = Label(categoria, text="Selecione o cliente:")
    lb_clientes.pack()
    listaClientes = ["BanQi", "Privalia"]
    cb_clientes = ttk.Combobox(categoria, values=listaClientes)
    cb_clientes.set("BanQi")
    cb_clientes.pack()

    #API Google Sheets - Preenchimento
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def google_sheets(data):
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
        cliente=cb_clientes.get()
    
        if cliente == 'Privalia':
            sheet_privalia = service.spreadsheets()
            result_privalia = sheet_privalia.values().get(spreadsheetId='1A5kQ_wqY_Tml_Utsz2QiRZkKhWQyiNnc_vcFWUcJdE0',
                                range='categoria!A:F').execute()
            values_privalia = result_privalia.get('values', [])

            df = pd.DataFrame(values_privalia)
            local_privalia = str((df.iloc[-1].name+2))
            result_privalia = sheet_privalia.values().update(spreadsheetId='1A5kQ_wqY_Tml_Utsz2QiRZkKhWQyiNnc_vcFWUcJdE0',
                                range='categoria!A'+local_privalia, valueInputOption='USER_ENTERED',
                                body={'values': data}).execute()
            
        elif cliente == 'BanQi':
            sheet_banqi = service.spreadsheets()
            result_banqi = sheet_banqi.values().get(spreadsheetId='1VcEG2qxqmFnERd1VE_N_OH1J3em9nDXgrr1HVcp1xcw',
                                range='categoria!J:O').execute()
            values_privalia = result_banqi.get('values', [])

            df = pd.DataFrame(values_privalia)
            local_privalia = str((df.iloc[-1].name+2))
            result_banqi = sheet_banqi.values().update(spreadsheetId='1VcEG2qxqmFnERd1VE_N_OH1J3em9nDXgrr1HVcp1xcw',
                                range='categoria!J'+local_privalia, valueInputOption='USER_ENTERED',
                                body={'values': data}).execute()

    #Funções de tratamento
    def wrap_text_file():    
        file = codeopen(
            askopenfilename(filetypes=[('CSV Files', '*.csv')]), 
            encoding='utf-16')
        yield file
        file.close()

    def tratar_banqi():
        #Arquivo Android 
        arquivo_pasta_android = next(wrap_text_file())
        arquivo_android = pd.read_csv(arquivo_pasta_android, encoding='utf-16', sep='\t')
        arquivo_android.reset_index(inplace=True)
        arquivo_android.rename(columns={'level_0': 'App ID',
                        'level_1': 'App Name',
                        'level_2': 'Country',
                        'level_3': 'Date',
                        'level_4': 'Posição',
                        'Sensor Tower Category Ranking Report': 'Updated'}, inplace=True)

        arquivo_android.drop([0, 1], inplace=True)
        arquivo_android.reset_index(drop=True, inplace=True)
        arquivo_android.fillna('', inplace=True)
       
        #Arquivo Apple
        arquivo_pasta_apple = next(wrap_text_file())
        arquivo_apple = pd.read_csv(arquivo_pasta_apple, encoding='utf-16', sep='\t')
        arquivo_apple.reset_index(inplace=True)
        arquivo_apple.rename(columns={'level_0': 'App ID',
                        'level_1': 'App Name',
                        'level_2': 'Country',
                        'level_3': 'Date',
                        'level_4': 'Posição',
                        'Sensor Tower Category Ranking Report': 'Updated'}, inplace=True)

        arquivo_apple.drop([0, 1], inplace=True)
        arquivo_apple.reset_index(drop=True, inplace=True)
        arquivo_apple.fillna('', inplace=True)
        arquivo_apple
        
        #Arquivo Final
        arquivo_final=pd.concat([arquivo_android,arquivo_apple])
        arquivo_final.reset_index(drop=True,inplace=True)
        arquivo_final.sort_values(by=['Date'], inplace=True)
        base_new=arquivo_final.values.tolist()
        google_sheets(base_new)

    def tratar_privalia():
        #Arquivo Android 
        arquivo_pasta_android = next(wrap_text_file())
        arquivo_android = pd.read_csv(arquivo_pasta_android, encoding='utf-16', sep='\t')
        arquivo_android.reset_index(inplace=True)
        arquivo_android.rename(columns={'level_0': 'App ID',
                        'level_1': 'App Name',
                        'level_2': 'Country',
                        'level_3': 'Date',
                        'level_4': 'Posição',
                        'Sensor Tower Category Ranking Report': 'Updated'}, inplace=True)

        arquivo_android.drop([0, 1], inplace=True)
        arquivo_android.reset_index(drop=True, inplace=True)
        arquivo_android.fillna('', inplace=True)
       
        #Arquivo Apple
        arquivo_pasta_apple = next(wrap_text_file())
        arquivo_apple = pd.read_csv(arquivo_pasta_apple, encoding='utf-16', sep='\t')
        arquivo_apple.reset_index(inplace=True)
        arquivo_apple.rename(columns={'level_0': 'App ID',
                        'level_1': 'App Name',
                        'level_2': 'Country',
                        'level_3': 'Date',
                        'level_4': 'Posição',
                        'Sensor Tower Category Ranking Report': 'Updated'}, inplace=True)

        arquivo_apple.drop([0, 1], inplace=True)
        arquivo_apple.reset_index(drop=True, inplace=True)
        arquivo_apple.fillna('', inplace=True)
        arquivo_apple
        
        #Arquivo Final
        arquivo_final=pd.concat([arquivo_android,arquivo_apple])
        arquivo_final.reset_index(drop=True,inplace=True)
        arquivo_final.sort_values(by=['Date'], inplace=True)
        base_new=arquivo_final.values.tolist()
        google_sheets(base_new)

    def tratar_dados():
        cliente = cb_clientes.get()
        if cliente == "BanQi":
            tratar_banqi()
        elif cliente == "Privalia":
            tratar_privalia()

    botao = Button(categoria, text="Go!", width=5, height=1, background="pink", command=tratar_dados)
    botao.pack()
pagina_categoria()

#Aba Rating
def pagina_rating():
    rating=Frame(nb)
    nb.add(rating,text='Rating')

    #ComboBox clientes
    lb_clientes = Label(rating, text="Selecione o cliente:")
    lb_clientes.pack()
    listaClientes = ["BanQi", "Privalia"]
    cb_clientes = ttk.Combobox(rating, values=listaClientes)
    cb_clientes.set("BanQi")
    cb_clientes.pack()

    #API Google Sheets - Preenchimento
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def google_sheets(data):
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
        cliente=cb_clientes.get()
    
        if cliente == 'Privalia':
            sheet_privalia = service.spreadsheets()
            result_privalia = sheet_privalia.values().get(spreadsheetId='1A5kQ_wqY_Tml_Utsz2QiRZkKhWQyiNnc_vcFWUcJdE0',
                                range='rating android play!A:F').execute()
            values_privalia = result_privalia.get('values', [])

            df = pd.DataFrame(values_privalia)
            local_privalia = str((df.iloc[-1].name+2))
            result_privalia = sheet_privalia.values().update(spreadsheetId='1A5kQ_wqY_Tml_Utsz2QiRZkKhWQyiNnc_vcFWUcJdE0',
                                range='rating android play!A'+local_privalia, valueInputOption='USER_ENTERED',
                                body={'values': data}).execute()
            
        elif cliente == 'BanQi':
            sheet_banqi = service.spreadsheets()
            result_banqi = sheet_banqi.values().get(spreadsheetId='1VcEG2qxqmFnERd1VE_N_OH1J3em9nDXgrr1HVcp1xcw',
                                range='categoria!J:O').execute()
            values_privalia = result_banqi.get('values', [])

            df = pd.DataFrame(values_privalia)
            local_privalia = str((df.iloc[-1].name+2))
            result_banqi = sheet_banqi.values().update(spreadsheetId='1VcEG2qxqmFnERd1VE_N_OH1J3em9nDXgrr1HVcp1xcw',
                                range='categoria!J'+local_privalia, valueInputOption='USER_ENTERED',
                                body={'values': data}).execute()

    #Funções de tratamento
    def wrap_text_file():    
        file = codeopen(
            askopenfilename(filetypes=[('CSV Files', '*.csv')]), 
            encoding='utf-8')
        yield file
        file.close()

    def tratar():
        arquivo_pasta = next(wrap_text_file())
        arquivo=pd.read_csv(arquivo_pasta, sep=',')

        #Formatando datas
        datas=[]
        i=0
        for data in arquivo['Data']:
            
            if int(arquivo['Data'][i][0:2]) < 10:
                dia=arquivo['Data'][i][0:1]
                mes=arquivo['Data'][i][5:9]
                ano=arquivo['Data'][i][13:18]
                if mes == 'jan.':
                    mes='01'
                elif mes == 'fev.':
                    mes='02'
                elif mes == 'mar.':
                    mes='03'
                elif mes == 'abr.':
                    mes='04'
                elif mes == 'mai.':
                    mes='05'
                elif mes == 'jun.':
                    mes='06'
                elif mes == 'jul.':
                    mes='07'
                elif mes == 'ago.':
                    mes='08'
                elif mes == 'set.':
                    mes='09'
                elif mes == 'out.':
                    mes='10'        
                elif mes == 'nov.':
                    mes='11'
                elif mes == 'dez.':
                    mes='12'
            else:
                dia=arquivo['Data'][i][0:2]
                mes=arquivo['Data'][i][6:10]
                ano=arquivo['Data'][i][14:18]
                if mes == 'jan.':
                    mes='01'
                elif mes == 'fev.':
                    mes='02'
                elif mes == 'mar.':
                    mes='03'
                elif mes == 'abr.':
                    mes='04'
                elif mes == 'mai.':
                    mes='05'
                elif mes == 'jun.':
                    mes='06'
                elif mes == 'jul.':
                    mes='07'
                elif mes == 'ago.':
                    mes='08'
                elif mes == 'set.':
                    mes='09'
                elif mes == 'out.':
                    mes='10'        
                elif mes == 'nov.':
                    mes='11'
                elif mes == 'dez.':
                    mes='12'
            datas.append(f'{dia}/{mes}/{ano}')
            i+=1
        arquivo['Data']=datas
        arquivo.drop(columns=['Observações'], inplace=True)
        
        #Arquivo Final
        base_new=arquivo.values.tolist()
        google_sheets(base_new)

    botao = Button(rating, text='Go!', width=5, height=1, background='red', command=tratar)
    botao.pack()
pagina_rating()

janela.mainloop()