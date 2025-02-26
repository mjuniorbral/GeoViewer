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
PATH_CONFIG = "data\Historico\Config-Graficos_EDMJ-Historico-Individual.xlsx"

# print("Importando leituras")
df = pd.read_csv(PATH_LEITURAS,delimiter=DFT_DELIMITER,encoding=DFT_ENCONDING,low_memory=False,dtype=DFT_DTYPE,parse_dates=DFT_PARSE_DATES,dayfirst=True)
df["Hora da Medição"] = df["Hora da Medição"].dt.time
# print("Leituras importadas e tratadas")

# print("Importando cadastros")
cadastro = UnirCadastroGEOTEC(PATH_CADASTRO)
# print("Cadastros importados")

# print("Importando configurações")
settings = readSheets(PATH_CONFIG,showLog=False)
seriesSetting = settings["Séries"]
graphSetting = settings["Gráficos"]
# print("Configurações importadas")

df_mod = df.merge(cadastro[["Código", "Cota do Fundo (m)"]],left_on="Código do Instrumento",right_on="Código",how="left")

df_mod["Valor Final"] = np.where(df_mod["Condição Adversa"]=="SECO", df_mod["Cota do Fundo (m)"], df_mod["Valor"])

leituras = df_mod.copy(deep=True)

end_time = time.time()
print(f"Dados carregados em {end_time-start_time:.5f} segs.\n")

from Instrumento import *

listaInstrumentos = dict()
for i in range(len(cadastro)):
    instrumento = Instrumento(cadastro.iloc[i].to_dict())
    instrumento.setLeituras(leituras[leituras["Código do Instrumento"]==instrumento.codigo])
    listaInstrumentos[instrumento.codigo] = instrumento

# start_time = time.time()
# print("Iniciando construção dos gráficos...")

# def fromDataToSerie(nomeInstrumento,df,seco=False,type="plot",label=None,color=None,toSecundary=False,showLegend=True,setup=dict(),juntarAutomatizado=False):
#     dados = tratarDados(nomeInstrumento,df,seco=seco)
#     if juntarAutomatizado:
#         dadosAutomatizado = tratarDados(nomeInstrumento+"_A",df,seco=seco)
#         dados = pd.concat([dados,dadosAutomatizado])
#     dados = dados.reset_index()
#     if seco:
#         nomeInstrumento+=" (seco)"

#     X = dados.loc[:,columnData]
#     if len(X)==0:
#         print(f"Não há leituras para {nomeInstrumento}")
#         return
#     Y = dados.loc[:,nomeInstrumento]
#     return Serie(X,Y,type,label,color,toSecundary,showLegend,setup)

# graphSetting = graphSetting[graphSetting["Render"]==True]
# for grafico in graphSetting["Nome do gráfico"]:
#     print(f"Construindo \"{grafico}\"")
    
#     has_fundo = graphSetting["Exibir Cota Fundo"].values[0]
#     has_topo = graphSetting["Exibir Cota Topo"].values[0]
#     has_atencao = graphSetting["Exibir Cota Atenção"].values[0]
#     has_alerta = graphSetting["Exibir Cota Alerta"].values[0]
#     has_emergencia = graphSetting["Exibir Cota Emergência"].values[0]
#     has_teste_vida = graphSetting["Exibir Testes de Vida"].values[0]
#     df_graph:pd.DataFrame = graphSetting[graphSetting["Nome do gráfico"]==grafico]
#     title = df_graph["Nome do gráfico"].values[0]
#     xInicial = df_graph["Data Inicial"].values[0]
#     xFinal = df_graph["Data Final"].values[0]
#     tituloYPrinc = df_graph["Título do Eixo Vertical Principal"].values[0]
#     yInicial = df_graph["Y Inicial"].values[0]
#     yFinal = df_graph["Y Final"].values[0]
#     y2Inicial = df_graph["Y2 Inicial"].values[0]
#     y2Final = df_graph["Y2 Final"].values[0]
#     hasSecos = df_graph["Tem Seco"].values[0]
    
#     filterGrafico = seriesSetting["Nome do gráfico"]==grafico
#     seriesToPlot = seriesSetting[filterGrafico]
#     list_series: list[Serie]= []
#     for instrumento in seriesToPlot["Instrumentos"].values:
#         renderizarSerie = seriesToPlot[seriesToPlot["Instrumentos"]==instrumento]["Render"].values[0]
#         if renderizarSerie:
#             # print(f"\t{instrumento}")
#             ...
#         else:
#             # print(f"\t{instrumento} não será renderizado")
#             ...
#             continue
            
#         df_instr:pd.DataFrame = seriesToPlot[seriesToPlot["Instrumentos"]==instrumento]
#         if not df_instr["Render"].values:
#             continue
        
#         nomeInstrumento=df_instr["Instrumentos"].values[0]
#         type = df_instr["Tipo"].values[0]
#         label = df_instr["Instrumentos"].values[0]
#         color = df_instr["Cor"].values[0]
#         toSecundary = df_instr["Eixo Secundário"].values[0]
#         outlier_max = df_instr["outlier_max"].values[0]
#         outlier_min = df_instr["outlier_min"].values[0]
#         verificarSeco = df_instr["Verificar seco"].values[0]
#         showLegend = df_instr["Mostrar na Legenda"].values[0]
#         marker = df_instr["Marcador"].values[0]
#         if pd.isna(marker):
#             setup=dict(marker="",linestyle="-")
#         else:
#             setup=dict(marker=marker,markersize=3,linestyle="-")
            
        
#         # Resetar a leitura para cada instrumento
#         df_filtered = leituras.copy(deep=True)
        
#         # Retirada das leituras fora do intervalo definido pelo Outlier na planilha Config
#         if not pd.isna(outlier_max):
#             df_filtered = df_filtered[df_filtered["Valor Final"]<outlier_max]
#         if not pd.isna(outlier_max):
#             df_filtered = df_filtered[df_filtered["Valor Final"]<outlier_max]
        
#         instrumentosProblematicos = [
#             "AGLBDIGPZ012_A", # Medição 635.2541788 < limite 635.56
#             "AGLBRMPZ006", # Medição 643.198 < limite 643.52
#             "AGLEDMPZ003_A", # Medição 955.9489035 > limite 860.354
#             "AGLEDMPZ004_A", # Medição 996.9196595 > limite 843.051
#             "AGLEDMPZ005_A", # Medição 813.6301204 < limite 813.845 & Medição 868.7457174 > limite 843.165
#             "AGLEDMPZ006_A", # Medição 787.0252079 < limite 797.88
#             "AGLEDMPZ007_A", # Medição 600.3071088 < limite 825.017 & Medição 1199.470392 > limite 877.017
#             "AGLEDMPZ024_A", # Medição 1070.303131 > limite 900.718
#             "AGLEDMPZ028_A", # Medição 844.5427838 < limite 853.494
#             "AGLPRMNA002", # Medição 826.69 < limite 826.735
#             "AGLPRMNA004", # Medição 833.914 < limite 834.238
#             "AGLPRMNA005", # Medição 824.915 < limite 825.039
#             "AGLPRMNA007", # Medição 823.685 < limite 824.097
#             "AGLPRMNA009_A", # Medição 995.577116 > limite 877.02
#             "AGLPRMNA013", # Medição 857.192 < limite 857.26
#                 ]
#         #################################################
#         # Retirada das leituras abaixo da cota de Fundo #
#         cotaFundo = cadastro[cadastro["Código"]==nomeInstrumento]["Cota do Fundo (m)"].values[0]
#         if nomeInstrumento in instrumentosProblematicos:
#             leiturasRetiradas = df_filtered[df_filtered["Valor Final"]<cotaFundo]
#             print(f"Datas retiradas do instrumento {nomeInstrumento}:\n{leiturasRetiradas[leiturasRetiradas['Código do Instrumento']==nomeInstrumento]['Data de Medição'].drop_duplicates()}")
#             df_filtered = df_filtered[df_filtered["Valor Final"]>=cotaFundo]
#         #################################################
        
#         serie = fromDataToSerie(nomeInstrumento=nomeInstrumento,
#                                     df=df_filtered,
#                                     seco=False,
#                                     type=type,
#                                     label=label,
#                                     color=color,
#                                     toSecundary=toSecundary,
#                                     showLegend=showLegend,
#                                     setup=setup)
#         ###########################################################################
#         #### VERIFICAÇÃO DE LEITURAS QUE ESTÃO FORA DO INTERVALO DE FUNDO/TOPO ####
#         ###########################################################################
#         cotaFundo = cadastro[cadastro["Código"]==nomeInstrumento]["Cota do Fundo (m)"].values[0]
#         cotaTopo = cadastro[cadastro["Código"]==nomeInstrumento]["Cota do Topo (m)"].values[0]
#         if not(pd.isna(cotaFundo)) and not(pd.isna(cotaTopo)):
#             if not serie.verificarLeituras(cotaFundo,cotaTopo):
#                 if nomeInstrumento not in instrumentosProblematicos:
#                     # print(f"{serie.label} com leituras inválidas.")
#                     raise Exception(f"{serie.label} com leituras inválidas.")
#         ###########################################################################
#         ###########################################################################
#         ###########################################################################

#         list_series.append(serie)
#         if verificarSeco:
#             leituras_manuais_secas = fromDataToSerie(nomeInstrumento=instrumento,
#                                         df = leituras,
#                                         seco = True,
#                                         type=type,
#                                         label=label,
#                                         color=color,
#                                         toSecundary=toSecundary,
#                                         showLegend=False,
#                                         setup=dict(marker="x",linestyle=""))
#             if leituras_manuais_secas != None:
#                 list_series.append(leituras_manuais_secas)
#                 hasLeituraSeco = True
#             else:
#                 hasLeituraSeco = False
            
#             if has_atencao:
#                 label = "Nível de Atenção"
#                 color = "yellow"
#                 nivelAtencao = cadastro[cadastro["Código"]==nomeInstrumento][label].values[0]
#                 valor = nivelAtencao
#                 list_series.append(Serie(pd.DataFrame([valor,valor]),pd.DataFrame([pd.Timestamp(day=1,month=1,year=2002),xFinal]),label=label,color=color,showLegend=True,setup=dict(marker="",linestyle="--")))
#             if has_alerta:
#                 label = "Nível de Alerta"
#                 color = "orange"
#                 nivelAlerta = cadastro[cadastro["Código"]==nomeInstrumento][label].values[0]
#                 valor = nivelAlerta
#                 list_series.append(Serie(pd.DataFrame([valor,valor]),pd.DataFrame([pd.Timestamp(day=1,month=1,year=2002),xFinal]),label=label,color=color,showLegend=True,setup=dict(marker="",linestyle="--")))
#             if has_emergencia:
#                 label = "Nível de Emergência"
#                 color = "red"
#                 nivelEmerg = cadastro[cadastro["Código"]==nomeInstrumento][label].values[0]
#                 valor = nivelEmerg
#                 list_series.append(Serie(pd.DataFrame([valor,valor]),pd.DataFrame([pd.Timestamp(day=1,month=1,year=2002),xFinal]),label=label,color=color,showLegend=True,setup=dict(marker="",linestyle="--")))
#             if has_fundo:
#                 label = "Cota do Fundo (m)"
#                 color = "gray"
#                 cotaFundo = cadastro[cadastro["Código"]==nomeInstrumento][label].values[0]
#                 valor = cotaFundo
#                 list_series.append(Serie(pd.DataFrame([valor,valor]),pd.DataFrame([pd.Timestamp(day=1,month=1,year=2002),xFinal]),label=label,color=color,showLegend=True,setup=dict(marker="",linestyle="--")))
#             if has_topo:
#                 label = "Cota do Topo (m)"
#                 color = "gray"
#                 cotaTopo = cadastro[cadastro["Código"]==nomeInstrumento][label].values[0]
#                 valor = cotaTopo
#                 list_series.append(Serie(pd.DataFrame([valor,valor]),pd.DataFrame([pd.Timestamp(day=1,month=1,year=2002),xFinal]),label=label,color=color,showLegend=True,setup=dict(marker="",linestyle="--")))
                
#     if hasSecos:
#         if not hasLeituraSeco:
#             print("legenda de leituras secas obsoleta, pois não há leituras secas nos dados entregues")
#             hasSecos = False
#     else:
#         if hasLeituraSeco:
#             raise Exception(f"Há leituras que não serão exibidas, pois não foi configurado o render das leituras secas do instrumento {instrumento} na planilha de configuração.")
        
#     nMonthLocator = df_graph["Distância em Meses dos Tickers"].values[0]    
    
#     listaMins = []
#     if pd.isna(xInicial):
#         for serie in list_series:
#             if serie.label == "AGLPL001":
#                 continue
#             listaMins.append(min(serie.X))
#     xInicial = min(intervaloPerfeitoData(listaMins))
#     # print(xInicial)
#     xMajorLocator = MonthLocator(interval=int(nMonthLocator))
#     if nMonthLocator==6:
#         xMajorLocator = MonthLocator(bymonth=(1,7))

#     hasSecundary = True # Considerando que todos os gráficos de níveis tem pluviometria, está sendo posto em Hardcode esse parâmetro
    
#     # setup_grafico = dict(xlim=(pd.Timestamp(day=1,month=4,year=2022),pd.Timestamp(day=1,month=9,year=2024)))

#     setup_grafico = dict(
#         xlim=(xInicial,xFinal),
#         yLabel=tituloYPrinc,
#         legendFonteSize = 10,
#         legendBbox_to_anchor = (0.5,-0.25),
#         # legendNcols = 6,
#         xMajorLocator = xMajorLocator,
#         legendLoc='upper center',
#         xLabelFontsize = 10,
#         yLabelFontsize = 10,
#         y2LabelFontsize = 10,
#         labelMajorSize = 12,
#         linewidth=2.0
#         )
    
#     if not(pd.isna(yInicial) and pd.isna(yFinal)):
#         setup_grafico.update(dict(
#             ylim=(yInicial,yFinal)
#         ))
#     if not(pd.isna(y2Inicial) and pd.isna(y2Final)):
#         setup_grafico.update(dict(
#             y2lim=(y2Inicial,y2Final)
#         ))
#     # print(setup_grafico)
    
#     if hasSecos:
#         list_series.append(Serie(pd.DataFrame([],columns=["Data"]),pd.DataFrame([],columns=["Valor"]),label="Leituras Secas",color="black",showLegend=True,setup=dict(marker="x",linestyle="")))
    
#     graph = Graphic(list_series,title=title,setup=setup_grafico,hasSecundary=hasSecundary,intervalX=[xInicial,xFinal])
#     graph.render(toFilter=False)
#     graph.save(path=f"images/nivelGrafico/{title}.png",showLog=True)

# end_time = time.time()
# print(f"Gráficos construídos em {end_time-start_time:.5f} segs.\n")
