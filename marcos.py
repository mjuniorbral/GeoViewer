"""
PROGRAMA GEOVIEWER
Objetivo: Renderizar gráficos de leituras de instrumentos e outros dados de geotecnia.
Desenvolvedor: Marcelo Cabral dos Santos Junior (Analista Técnico de Engenharia Civil na GEOCOBA - Projetos de Engenharia (https://www.geocoba.com/))
Data de início de desenvolvimento: 02/01/2024
Contato: mjuniorbral@gmail.com
"""

from modules import Timer
from modules import log
log.setLevel("INFO")
timer_load = Timer()
timer_load.set_time_marker("carregamento")
log.info("Iniciando carregamento de dados...\n\n")

import pandas as pd
from modules.classes import *
from modules import (
    readSheets,
    tratarDados,
    columnData,
    Serie,Graphic,
    retornarValorNaoNulo,
    monthByInterval,
    intervaloPerfeitoDataMes,
    minimoValido,
    maximoValido,
    get_decimal_places
    )
from modules.agCadastro import UnirCadastroGEOTEC

import warnings
warnings.filterwarnings("ignore")

DFT_DELIMITER = ";"
DFT_DECIMAL = ","
DFT_ENCONDING = "ISO-8859-1"
# DFT_ENCONDING = "UTF-8" # Enconding para CSV (UTF-8)
DFT_DTYPE = {
    "Valor": "float",
}
DFT_PARSE_DATES = [
    "Data de Medição",
    "Hora da Medição"
    ]

################ ENTRADAS ################
PATH_FOLDER = "data\\"
PATH_LEITURAS = PATH_FOLDER+"Leituras.csv"
PATH_CADASTRO = PATH_FOLDER+"Cadastro.xlsx"
PATH_CONFIG = PATH_FOLDER+"Config-Graficos.xlsx"
##########################################

PATH_OUT = "images/nivelGrafico/"

log.info("Importando leituras")
df = pd.read_csv(PATH_LEITURAS,delimiter=DFT_DELIMITER,encoding=DFT_ENCONDING,low_memory=False,dtype=DFT_DTYPE,parse_dates=DFT_PARSE_DATES,dayfirst=True,decimal=DFT_DECIMAL)
df["Hora da Medição"] = df["Hora da Medição"].dt.time
log.info("Leituras importadas e tratadas\n\n")

log.info("Importando cadastros")
cadastro = UnirCadastroGEOTEC(PATH_CADASTRO)
log.info("Cadastros importados\n\n")

log.info("Importando configurações")
settings = readSheets(PATH_CONFIG,showLog=False)
seriesSetting = settings["Séries"]
graphSetting = settings["Gráficos"]

leituras = df.copy(deep=True)

timer_load.get_delta_time_from_time_marker("carregamento")
log.info("Configurações importadas\n\n")
