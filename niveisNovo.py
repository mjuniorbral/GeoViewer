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
    list_series = []
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
        list_series.append(serie)
    df_graph = graphSetting[graphSetting["Nome do gráfico"]==grafico]
    title = df_graph["Nome do gráfico"].values[0]
    xInicial = df_graph["Data Inicial"].values[0]
    xFinal = df_graph["Data Final"].values[0]
    hasSecundary = True # Considerando que todos os gráficos de níveis tem pluviometria, está sendo posto em Hardcode esse parâmetro
    # setup_grafico = dict(xlim=(pd.Timestamp(day=1,month=4,year=2022),pd.Timestamp(day=1,month=9,year=2024)))
    setup_grafico = dict(xlim=(xInicial,xFinal))
    graph = Graphic(list_series,title=title,setup=setup_grafico,hasSecundary=hasSecundary,intervalX=[xInicial,xFinal])
    graph.render(toFilter=False)
    graph.save(path=f"images/nivelGrafico/{title}.png",showLog=True)