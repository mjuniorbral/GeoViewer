'''
Módulo criado por Marcelo Cabral dos Santos Junior
Empresa GEOCOBA, Brasil
Linguagem: Python 3.10
Data: 02/01/2024

ESTRUTURA DE PASTA E ARQUIVOS

arquivos
| main.py: programa principal que deve ser executado
| const.py: valores de referência para o programa ser rodado
| auxiliares.py: operações auxiliares para o funcionamento do programa
'''

# Módulos nativos do Python
from datetime import date

# Módulos externos
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Módulos do programa
from .auxiliares import inverterDicio
from .const import relacaoCabecalho, pastaArquivos, pastaResultados

# Parâmetros padrões
DEFAULT_HEADER = 2

def UnirCadastroGEOTEC(relative_path:str,filtrarColunas:bool=True,header:int=DEFAULT_HEADER):
    listaCadastros = []
    id_planilha = 0
    
    while True:
        try:
            tabela = pd.read_excel(relative_path,id_planilha,header=header)
            # Implementar um módulo de Logging
            # print(f"[UnirCadastroGEOTEC] {id_planilha+1}ª planilha importada")
            listaCadastros.append(tabela)
        except:
            # Implementar um módulo de Logging
            # print(f"[UnirCadastroGEOTEC] {id_planilha} planilhas lidas do arquivo \"{relative_path}\"")
            break
        id_planilha+=1
    
    cadastro = pd.concat(listaCadastros)
    if filtrarColunas:
        for i in cadastro:
            if i in inverterDicio(relacaoCabecalho)[None]:
                cadastro = cadastro.drop(columns=[i])
            else:
                if i not in relacaoCabecalho.keys():
                    pass
                pass
    cadastro = cadastro.reset_index()
    return cadastro

if __name__=="__main__":
    cadastro = UnirCadastroGEOTEC()
    pass
