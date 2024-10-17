import pandas as pd
from modules import importFromGEOTECModel,readSheets,tratarDados,columnData,Serie,Graphic

# Comando para ignorar os UserWarning dados pelo Pyhton
import warnings
warnings.filterwarnings('ignore')

file = "data\leituras-janeiro2024-agosto2024.xlsx"
registrationsSheet = "Cadastro Agosto2024"
measuresSheet = "Resumo"
cadastro, leituras, columnsRegistrations, columnsMeasures = importFromGEOTECModel(file,registrationsSheet,measuresSheet)

def fromDataToSerie(nomeInstrumento,df,seco=False,type="plot",label=None,color=None,toSecundary=False,showLegend=True,setup=dict(),juntarAutomatizado=False):
    dados = tratarDados(nomeInstrumento,df,seco=seco)
    if juntarAutomatizado:
        dadosAutomatizado = tratarDados(nomeInstrumento+"_A",df,seco=seco)
        dados = pd.concat([dados,dadosAutomatizado])
    dados = dados.reset_index()
    if seco:
        nomeInstrumento+=" (seco)"
    # print(dados)
    X = dados.loc[:,columnData]
    if len(X)==0:
        print(f"Não há leituras para {nomeInstrumento}")
        return
    Y = dados.loc[:,nomeInstrumento]
    return Serie(X,Y,type,label,color,toSecundary,showLegend,setup)

settings = readSheets("data\Config-Graficos.xlsx")
seriesSetting = settings["Séries"]
graphSetting = settings["Gráficos"]

for grafico in graphSetting["Nome do gráfico"]:
    print(f"Construindo \"{grafico}\"")
    filterGrafico = seriesSetting["Nome do gráfico"]==grafico
    seriesToPlot = seriesSetting[filterGrafico]
    for instrumento in seriesToPlot["Instrumentos"].values:
        print(f"\t{instrumento}")
        df_instr = seriesToPlot[seriesToPlot["Instrumentos"]==instrumento]
        if not df_instr["Render"].values:
            continue
        nomeInstrumento=df_instr["Instrumentos"].values[0]
        df=leituras
        seco=False
        type=df_instr["Tipo"].values[0]
        label=df_instr["Instrumentos"].values[0]
        color=df_instr["Cor"].values[0]
        toSecundary=df_instr["Eixo Secundário"].values[0]
        showLegend=True
        setup=dict(marker="",linestyle="-")
        serie = fromDataToSerie(nomeInstrumento=nomeInstrumento,
                                    df=df,
                                    seco=seco,
                                    type=type,
                                    label=label,
                                    color=color,
                                    toSecundary=toSecundary,
                                    showLegend=showLegend,
                                    setup=setup)
        # if df_instr["Verificar seco"]:
        #     leituras_manuais_secas = fromDataToSerie(nomeInstrumento=instrumento,
        #                                 df=df_instr["Instrumentos"],
        #                                 seco=df_instr["Verificar seco"],
        #                                 type=df_instr["Tipo"],
        #                                 label=df_instr["Instrumentos"],
        #                                 color=df_instr["Cor"],
        #                                 toSecundary=df_instr["Eixo Secundário"],
        #                                 showLegend=False,
        #                                 setup=dict(marker="x",linestyle=""))