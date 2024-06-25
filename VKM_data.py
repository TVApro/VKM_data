import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import openpyxl
import numpy as np

BUKVY = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
df_global = pd.DataFrame({'Номер ВКМ':[], 'Типовой':[], 'Культура':[], 'Температура':[], 'Доп. условия':[], 'Выделен из':[], 'Среда культивирования':[]})

for bukva in BUKVY:
    url = 'https://vkm.ru/rus/catalog/bacte/'+bukva+'.htm'
    page1 = requests.get(url)
    soup1 = BeautifulSoup(page1.text, 'lxml')
    links1 = soup1.findAll("a")
    for link in links1:
        page2 = requests.get("https://vkm.ru/rus/catalog/bacte/"+link["href"])
        soup2 = BeautifulSoup(page2.text, 'lxml')
        tables = soup2.findAll("table")
        for table in tables:
            df_simple = pd.DataFrame(columns=['First', 'Second'])
            for j in table.find_all("tr"):
                row_data = j.find_all("td")
                row = [i.text for i in row_data]
                length = len(df_simple)
                df_simple.loc[length] = row
            index_b = df_simple.index[df_simple['First'] == 'Номер штамма'][0]
            NUM = df_simple.at[index_b, 'Second']
            BNUM = re.search(r'[A-Za-z]+-[0123456789]+', NUM).group()
            if 'Тип' in NUM:
                TIP = '+'
            else:
                TIP = '-'
            index_name = df_simple.index[df_simple['First'] == 'Таксономическое название штамма'][0]
            NAME = df_simple.at[index_name, 'Second']
            try:
                index_temp = df_simple.index[df_simple['First'] == 'Температура культивирования (С)'][0]
                TEMP = df_simple.at[index_temp, 'Second']
            except:
                TEMP = np.nan
                
            try:
                index_cond = df_simple.index[df_simple['First'] == 'Особые условия культивирования'][0]
                COND = df_simple.at[index_cond, 'Second']
            except:
                COND = '-'

            try:
                index_place = df_simple.index[df_simple['First'] == 'Выделен из'][0]
                PLACE = df_simple.at[index_place, 'Second']
            except:
                PLACE = np.nan

            try:
                index_medium = df_simple.index[df_simple['First'] == 'Питательная среда номер'][0]
                MED = df_simple.at[index_medium, 'Second']
            except:
                MED = np.nan
    
            df_global.loc[len(df_global.index)] = [BNUM, TIP, NAME, TEMP, COND, PLACE, MED]
            print(BNUM, NAME)
df_uniq = df_global.drop_duplicates(subset=['Номер ВКМ'])
del df_global
df_uniq.reset_index(drop=True, inplace=True)
df_uniq.to_excel('parsing_table.xlsx')
    
    
