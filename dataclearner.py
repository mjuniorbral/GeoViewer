import pandas as pd
from modules.functions import readSheets
import datetime

arquivo_excel = 'data/INC01-clean.xlsx'
dictDF = readSheets("data\INC01-Dados_Brutos.xlsx")
# arquivo_excel = 'data/INC02-clean.xlsx'
# dictDF = readSheets("data\INC02-Dados_Brutos.xlsx")

nomes_planilhas = list(dictDF.keys())
data_antigo_novo_nome = dict()


# Criar um objeto ExcelWriter e escrever vários DataFrames em diferentes planilhas
with pd.ExcelWriter(arquivo_excel, engine='xlsxwriter') as writer:
    for nome_antigo in nomes_planilhas:
        novo_nome = nome_antigo.replace("BRPINC202001","").replace("(","").replace(")","").replace("AGLBRPINC01","")
        # novo_nome = nome_antigo.replace("BRPINC202002","").replace("(","").replace(")","").replace("AGLBRPINC02","")
        day = int(novo_nome.split("-")[0])
        month = int(novo_nome.split("-")[1])
        year = int(novo_nome.split("-")[2])
        if year in [19,20,21,22,23,24]:
            year = 2000+year
        
        data_nome = pd.Timestamp(day=day,month=month,year=year)
        df = dictDF[nome_antigo]
        celula = df.iloc[7,1]

        if isinstance(celula,(pd.Timestamp,datetime.datetime)):
            data_celula_inverted = celula
            data_celula = pd.Timestamp(day=data_celula_inverted.month,month=data_celula_inverted.day,year=data_celula_inverted.year) # Invertendo

        elif not ("/" in str(celula)):
            data_celula_inverted:pd.Timestamp = pd.to_datetime(celula, unit='D', origin='1899-12-30')
            data_celula = pd.Timestamp(day=data_celula_inverted.month,month=data_celula_inverted.day,year=data_celula_inverted.year) # Invertendo

        else:
            day = int(celula.split("/")[1]) # Invertendo
            month = int(celula.split("/")[0]) # Invertendo
            year = int(celula.split("/")[2])
            data_celula = pd.Timestamp(day=day,month=month,year=year)
        data_antigo_novo_nome[data_nome] = (nome_antigo,novo_nome,data_celula)
        text_celula = datetime.date.strftime(data_celula,"%d/%m/%Y")            
        
        print(novo_nome,text_celula,sep="\t")
        continue
    
    datas = list(data_antigo_novo_nome.keys())
    datas.sort()
    for data in datas:
        nome_antigo,novo_nome,data_celula = data_antigo_novo_nome[data]
        df = dictDF[nome_antigo]
        df.iloc[7,0] = "Data/Hora"
        df.iloc[7,1] = datetime.date.strftime(data_celula,"%d/%m/%Y")
        if not data_celula == data:
            df.iloc[7,4] = "VALOR DIFERENTE DO TÍTULO !!!!!!!!!!!!!!!!!!!"
        df.to_excel(writer, sheet_name=novo_nome, index=False)
        continue
    
print(f'Arquivo Excel "{arquivo_excel}" criado com sucesso.')
