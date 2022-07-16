import pyautogui
import pyperclip
import time
import webbrowser
from bs4 import BeautifulSoup
import csv
import requests
import zipfile
import pandas as pd
import pandas_gbq
from pandas.io import gbq
from google.cloud import bigquery
import json
import os
from os import path
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from datetime import datetime as dt, timedelta
from unicodedata import normalize
import glob
from datetime import datetime as dt, timedelta


start_date = dt.today()


start_date = start_date.date()


url1 = 'https://app.rdstation.com.br/emails/sent'


chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe --incognito %s'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open_new_tab(url1)
time.sleep(10)
#pyautogui.position() # pega a posição do mouse no momento em pixels
pyautogui.click(x=1269, y=286) #Posição botão exportar
time.sleep(3)
pyautogui.click(x=1294, y=233) #Posição setinha para abrir range de data
time.sleep(3)
pyautogui.click(x=1207, y=324) #Posição ultimos 6 meses
time.sleep(3)
pyautogui.click(x=1284, y=679) #Posição ultimos 6 meses
time.sleep(30)
url2 = 'https://www.gmail.com'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open_new_tab(url2)
time.sleep(10)
pyautogui.click(x=592, y=105) # Clica na caixinha para pesquisar email
time.sleep(5)
pyautogui.write("Estatísticas das campanhas entre 20/10/2021 e 20/04/2022 - www.fideli.com.br")
time.sleep(5)
pyautogui.click(x=900, y=200) # Clica na caixinha para pesquisar email
time.sleep(5)
pyautogui.click(x=-1123, y=-220) # Clica no primeiro email
time.sleep(5)
pyautogui.click(x=773, y=588) # Clica no link para baixar o arquivo
time.sleep(5)
zip = glob.glob(r'C:\Users\funcionario\Downloads\*esta*.zip')[0]
fantasy_zip = zipfile.ZipFile(zip) #descompacta zip
fantasy_zip.extract('estatisticas_das_campanhas_entre_20_10_2021_e_20_04_2022_www_fideli_com_br.csv', r'C:\Users\funcionario\Downloads') #extrai arquivo


fantasy_zip.close()


emailmkt = pd.read_csv(r'C:\Users\funcionario\Downloads\estatisticas_das_campanhas_entre_20_10_2021_e_20_04_2022_www_fideli_com_br.csv',delimiter=',')

df = pd.DataFrame.from_dict(emailmkt)

df.columns = df.columns.str.replace(' ','_')
df.columns = df.columns.str.replace('(','_')
df.columns = df.columns.str.replace(')','_')
df.columns = df.columns.str.replace('/','_')
df.columns = df.columns.str.replace('-','_')

df['data_carga'] = str(start_date)


count = 0
try:
    while(count <= df.columns.size):
        coluna = df.columns[count]
        semacento = normalize('NFKD', coluna).encode('ASCII','ignore').decode('ASCII')
        df= df.rename(columns={ coluna : semacento})
        count = count + 1
except:
    pass

'''
root = path.dirname(path.abspath(__file__))
children = os.listdir(root)
files = [c for c in children if path.isfile(path.join(root, c))]
bl= root+'\\'+files[32]


SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']

SCOPES2 = ['https://www.googleapis.com/auth/bigquery']

SERVICE_ACCOUNT_FILE = bl

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


credentials2 = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES2)


client = bigquery.Client(project='track-field-oficial', credentials=credentials2)


df.to_gbq('TF_CargaDados.fideli',
             'track-field-oficial',
             chunksize=None,
             # I have tried with several chunk sizes, it runs faster when it's one big chunk (at least for me)
             if_exists='append')


#'Estatísticas das campanhas entre 19/10/2021 e 19/04/2022 - www.fideli.com.br' #titulo email

#Point(x=1190, y=678)


#pyautogui.PAUSE = 3.0
#pyautogui.hotkey("ctrl", "t")
#pyautogui.write("https://docs.google.com/spreadsheets/d/12tXR9EHci3BST3iZrFlOxXoBlBliFsqhOaIPxseq-a0/edit?pli=1#gid=19477000")
#pyautogui.press("enter")


'''