import time
start_time = time.time()
print("Iniciando carregamento de dados...")

import pandas as pd
from modules.classes import *
from modules import readSheets,tratarDados,columnData,Serie,Graphic
from modules.agCadastro import UnirCadastroGEOTEC

import warnings
warnings.filterwarnings("ignore")

DFT_DELIMITER = ";"
DFT_ENCONDING = "ISO-8859-1"
DFT_ENCONDING = "UTF-8"
DFT_DTYPE = {
    "Valor": "float"
}
DFT_PARSE_DATES = [
    "Data de Medição",
    "Hora da Medição"
    ]

PATH_LEITURAS = "data\Historico\Historico-até-01-FEV-2025.csv"
PATH_CADASTRO = "data\Historico\\2298_Instrumento-01-02-2025-154527.xlsx"
PATH_CONFIG = "data\Historico\Config-Graficos_DIO-Historico.xlsx"

# print("Importando leituras")
df = pd.read_csv(PATH_LEITURAS,delimiter=DFT_DELIMITER,encoding=DFT_ENCONDING,low_memory=False,dtype=DFT_DTYPE,parse_dates=DFT_PARSE_DATES,dayfirst=True)
df["Hora da Medição"] = df["Hora da Medição"].dt.time
# print("Leituras importadas e tratadas")

# print("Importando cadastros")
cadastro = UnirCadastroGEOTEC(PATH_CADASTRO,filtrarColunas=False)
# print("Cadastros importados")

# print("Importando configurações")
settings = readSheets(PATH_CONFIG,showLog=False)
seriesSetting = settings["Séries"]
graphSetting = settings["Gráficos"]
# print("Configurações importadas")

df_mod = df.merge(cadastro[["Código", "Cota do Fundo (m)"]],left_on="Código do Instrumento",right_on="Código",how="left")

df_mod["Valor Final"] = np.where(df_mod["Condição Adversa"]=="SECO", df_mod["Cota do Fundo (m)"], df_mod["Valor"])

leituras = df_mod.copy(deep=True)

# piezometros = cadastro[cadastro["Tipo de Instrumento"]=="Piezômetro"].dropna(axis=1)
# tipos = cadastro["Tipo de Instrumento"].drop_duplicates().to_list()
# colunasCadastro = cadastro.columns.to_list()

end_time = time.time()
print(f"Dados carregados em {end_time-start_time:.5f} segs.\n")

start_time = time.time()
print("Iniciando construção dos gráficos...")


def fromDataToSerie(nomeInstrumento,df,seco=False,type="plot",label=None,color=None,toSecundary=False,showLegend=True,setup=dict(),juntarAutomatizado=False):
    dados = tratarDados(nomeInstrumento,df,seco=seco)
    if juntarAutomatizado:
        dadosAutomatizado = tratarDados(nomeInstrumento+"_A",df,seco=seco)
        dados = pd.concat([dados,dadosAutomatizado])
    dados = dados.reset_index()
    if seco:
        nomeInstrumento+=" (seco)"

    X = dados.loc[:,columnData]
    if len(X)==0:
        print(f"Não há leituras para {nomeInstrumento}")
        return
    Y = dados.loc[:,nomeInstrumento]
    return Serie(X,Y,type,label,color,toSecundary,showLegend,setup)

graphSetting = graphSetting[graphSetting["Render"]==True]
for grafico in graphSetting["Nome do gráfico"]:
    print(f"Construindo \"{grafico}\"")
    
    filterGrafico = seriesSetting["Nome do gráfico"]==grafico
    seriesToPlot = seriesSetting[filterGrafico]
    list_series: list[Serie]= []
    for instrumento in seriesToPlot["Instrumentos"].values:
        renderizarSerie = seriesToPlot[seriesToPlot["Instrumentos"]==instrumento]["Render"].values[0]
        if renderizarSerie:
            # print(f"\t{instrumento}")
            ...
        else:
            # print(f"\t{instrumento} não será renderizado")
            ...
            continue
            
        df_instr = seriesToPlot[seriesToPlot["Instrumentos"]==instrumento]
        if not df_instr["Render"].values:
            continue
        
        nomeInstrumento=df_instr["Instrumentos"].values[0]
        type = df_instr["Tipo"].values[0]
        label = df_instr["Instrumentos"].values[0]
        color = df_instr["Cor"].values[0]
        toSecundary = df_instr["Eixo Secundário"].values[0]
        outlier_max = df_instr["outlier_max"].values[0]
        outlier_min = df_instr["outlier_min"].values[0]
        verificarSeco = df_instr["Verificar seco"].values[0]
        showLegend = df_instr["Mostrar na Legenda"].values[0]
        marker = df_instr["Marcador"].values[0]
        if pd.isna(marker):
            setup=dict(marker="",linestyle="-")
        else:
            setup=dict(marker=marker,markersize=3,linestyle="-")
            
        
        df_filtered = leituras.copy(deep=True)
        if not pd.isna(outlier_max):
            df_filtered = df_filtered[df_filtered["Valor Final"]<outlier_max]
        if not pd.isna(outlier_max):
            df_filtered = df_filtered[df_filtered["Valor Final"]<outlier_max]
        
        cotaFundo = cadastro[cadastro["Código"]==nomeInstrumento]["Cota do Fundo (m)"].values[0]
        if nomeInstrumento in ["AGLBDIGPZ012_A"]:
            leiturasRetiradas = df_filtered[df_filtered["Valor Final"]<cotaFundo]
            print(f"Datas retiradas do instrumento {nomeInstrumento}:\n{leiturasRetiradas[leiturasRetiradas['Código do Instrumento']==nomeInstrumento]['Data de Medição'].drop_duplicates()}")
            df_filtered = df_filtered[df_filtered["Valor Final"]>=cotaFundo]
        
        serie = fromDataToSerie(nomeInstrumento=nomeInstrumento,
                                    df=df_filtered,
                                    seco=False,
                                    type=type,
                                    label=label,
                                    color=color,
                                    toSecundary=toSecundary,
                                    showLegend=showLegend,
                                    setup=setup)
        ###########################################################################
        #### VERIFICAÇÃO DE LEITURAS QUE ESTÃO FORA DO INTERVALO DE FUNDO/TOPO ####
        ###########################################################################
        # cotaFundo = cadastro[cadastro["Código"]==nomeInstrumento]["Cota do Fundo (m)"].values[0]
        # cotaTopo = cadastro[cadastro["Código"]==nomeInstrumento]["Cota do Topo (m)"].values[0]
        # if not(pd.isna(cotaFundo)) and not(pd.isna(cotaTopo)):
        #     if not serie.verificarLeituras(cotaFundo,cotaTopo):
        #         instrumentosProblematicos = [
        #             "AGLBDIGPZ012_A" # Medição 635.2541788 < limite 635.56
        #         ]
        #         if nomeInstrumento not in instrumentosProblematicos:
        #             raise Exception(f"{serie.label} com leituras inválidas.")
        ###########################################################################
        ###########################################################################
        ###########################################################################

        list_series.append(serie)
        if verificarSeco:
            leituras_manuais_secas = fromDataToSerie(nomeInstrumento=instrumento,
                                        df = leituras,
                                        seco = True,
                                        type=type,
                                        label=label,
                                        color=color,
                                        toSecundary=toSecundary,
                                        showLegend=False,
                                        setup=dict(marker="x",linestyle=""))
            if leituras_manuais_secas != None:
                list_series.append(leituras_manuais_secas)
    df_graph = graphSetting[graphSetting["Nome do gráfico"]==grafico]
    title = df_graph["Nome do gráfico"].values[0]
    xInicial = df_graph["Data Inicial"].values[0]
    xFinal = df_graph["Data Final"].values[0]
    tituloYPrinc = df_graph["Título do Eixo Vertical Principal"].values[0]
    yInicial = df_graph["Y Inicial"].values[0]
    yFinal = df_graph["Y Final"].values[0]
    y2Inicial = df_graph["Y2 Inicial"].values[0]
    y2Final = df_graph["Y2 Final"].values[0]
    hasSecos = df_graph["Tem Seco"].values[0]
    nMonthLocator = df_graph["Distância em Meses dos Tickers"].values[0]    
    
    listaMins = []
    if pd.isna(xInicial):
        for serie in list_series:
            if serie.label == "AGLPL001":
                continue
            listaMins.append(min(serie.X))
    xInicial = min(intervaloPerfeitoData(listaMins))
    # print(xInicial)
    xMajorLocator = MonthLocator(interval=int(nMonthLocator))
    if nMonthLocator==6:
        xMajorLocator = MonthLocator(bymonth=(1,7))

    hasSecundary = True # Considerando que todos os gráficos de níveis tem pluviometria, está sendo posto em Hardcode esse parâmetro
    
    # setup_grafico = dict(xlim=(pd.Timestamp(day=1,month=4,year=2022),pd.Timestamp(day=1,month=9,year=2024)))

    setup_grafico = dict(
        xlim=(xInicial,xFinal),
        yLabel=tituloYPrinc,
        legendFonteSize = 10,
        legendBbox_to_anchor = (0.5,-0.25),
        # legendNcols = 6,
        xMajorLocator = xMajorLocator,
        legendLoc='upper center',
        xLabelFontsize = 10,
        yLabelFontsize = 10,
        y2LabelFontsize = 10,
        labelMajorSize = 12,
        linewidth=2.0
        )
    
    if not(pd.isna(yInicial) and pd.isna(yFinal)):
        setup_grafico.update(dict(
            ylim=(yInicial,yFinal)
        ))
    if not(pd.isna(y2Inicial) and pd.isna(y2Final)):
        setup_grafico.update(dict(
            y2lim=(y2Inicial,y2Final)
        ))
    # print(setup_grafico)
    
    if hasSecos:
        list_series.append(Serie(pd.DataFrame([],columns=["Data"]),pd.DataFrame([],columns=["Valor"]),label="Leituras Secas",color="black",showLegend=True,setup=dict(marker="x",linestyle="")))
    
    graph = Graphic(list_series,title=title,setup=setup_grafico,hasSecundary=hasSecundary,intervalX=[xInicial,xFinal])
    graph.render(toFilter=False)
    graph.save(path=f"images/nivelGrafico/{title}.png",showLog=True)

end_time = time.time()
print(f"Gráficos construídos em {end_time-start_time:.5f} segs.\n")
