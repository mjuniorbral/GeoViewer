from modules import Timer
from modules import log
log.setLevel("ERROR")
timer_load = Timer()
timer_load.set_time_marker()
log.info("Iniciando carregamento de dados...")

import pandas as pd
from modules.classes import *
from modules import readSheets,tratarDados,columnData,Serie,Graphic,retornarValorNaoNulo
from modules.agCadastro import UnirCadastroGEOTEC
from Instrumento import Instrumento

import warnings
warnings.filterwarnings("ignore")

DFT_DELIMITER = ";"
DFT_ENCONDING = "ISO-8859-1"
DFT_ENCONDING = "UTF-8"
DFT_DTYPE = {
    "Valor": "float",
}
DFT_PARSE_DATES = [
    "Data de Medição",
    "Hora da Medição"
    ]

PATH_LEITURAS = "data\Historico\Historico-até-01-FEV-2025.csv"
PATH_CADASTRO = "data\Historico\\2298_Instrumento-01-02-2025-154527.xlsx"
PATH_CONFIG = "data\Historico\Config-Graficos_EDMJ-Historico-Individual.xlsx"

log.info("Importando leituras")
df = pd.read_csv(PATH_LEITURAS,delimiter=DFT_DELIMITER,encoding=DFT_ENCONDING,low_memory=False,dtype=DFT_DTYPE,parse_dates=DFT_PARSE_DATES,dayfirst=True)
df["Hora da Medição"] = df["Hora da Medição"].dt.time
log.info("Leituras importadas e tratadas")

log.info("Importando cadastros")
cadastro = UnirCadastroGEOTEC(PATH_CADASTRO)
log.info("Cadastros importados")

log.info("Importando configurações")
settings = readSheets(PATH_CONFIG,showLog=False)
seriesSetting = settings["Séries"]
graphSetting = settings["Gráficos"]
log.info("Configurações importadas")

leituras = df.copy(deep=True)

timer_load.get_delta_time_from_time_marker()


timer_load.set_time_marker()
# Inicializando a variável de armazenamento dos instrumentos
listaInstrumentos = dict()

# Carregando os gráficos que serão renderizados
graphSetting:pd.DataFrame = graphSetting[graphSetting["Render"]==True]
for grafico in graphSetting["Nome do gráfico"]:
    temSeco = False
    temJorrante = False
    listaLimitesDatas = []
    listaLimitesValores = []
    listaLimitesValoresSec = []
    print(f"Construindo \"{grafico}\"")
    # Carregando as séries aliadas àquele gráfico
    filterGrafico = seriesSetting["Nome do gráfico"]==grafico
    seriesToPlot:pd.DataFrame = seriesSetting[filterGrafico]
    list_series: list[Serie]= []
    for instrumento in seriesToPlot["Instrumentos"].values:
        # Extraindo dados sobre o instrumento a ser renderizado nessa iteração
        df_instr:pd.DataFrame = seriesToPlot[seriesToPlot["Instrumentos"]==instrumento]
        
        renderizarSerie = df_instr["Render"].values[0]
        if not renderizarSerie:
            # Avisando os instrumentos que não serão renderizados 
            log.debug(f"\t{instrumento} não será renderizado no gráfico {grafico}")
            continue
        
        # Isolando os dados do df_instr em variável do programa para melhorar a trabalhabilidade
        type = df_instr["Tipo"].values[0]
        label = df_instr["Instrumentos"].values[0]
        color = df_instr["Cor"].values[0]
        toSecundary = df_instr["Eixo Secundário"].values[0]
        outlier_max = df_instr["outlier_max"].values[0]
        outlier_min = df_instr["outlier_min"].values[0]
        verificarSeco = df_instr["Verificar seco"].values[0] #################################### OBSOLETO ############################## <<<-------
        showLegend = df_instr["Mostrar na Legenda"].values[0]
        marker = df_instr["Marcador"].values[0]
        temTeste = df_instr["Testes de Vida"].values[0]
        temAtencao = df_instr["Atenção"].values[0]
        temAlerta = df_instr["Alerta"].values[0]
        temEmerg = df_instr["Emergência"].values[0]
        temTopo = df_instr["Topo"].values[0]
        temFundo_Base = df_instr["Fundo/Base"].values[0]
        
        # Criando o setup de acordo com o campo do marcador do instrumento
        if pd.isna(marker):
            setup=dict(marker="",linestyle="-")
        else:
            setup=dict(marker=marker,markersize=3,linestyle="-")
            
        
        # Resetar a leitura para cada instrumento [VARIPAVEL leituras NÃO É USADA APÓS ESSA LINHA]
        df_filtered = leituras.copy(deep=True)
        
        # Criando o objeto Instrumento para extrair os valores
        cadastro_instrumento:pd.DataFrame = cadastro.loc[cadastro["Código"]==instrumento]
        # instrumento_obj = Instrumento(cadastro_instrumento.to_dict())
        try:
            instrumento_obj = Instrumento(cadastro_instrumento.to_dict(orient="records")[0])
        except Exception as m:
            print(cadastro_instrumento.values)
            print(f"{instrumento}: {m}")
            continue
        instrumento_obj.set_leituras(leituras[leituras["Código do Instrumento"]==instrumento_obj.codigo])
        listaInstrumentos[instrumento_obj.codigo] = instrumento_obj
        
        # Adicionando a série de leituras
        serie = Serie(
            X = instrumento_obj.leituras_validas["Data/Hora"],
            Y = instrumento_obj.leituras_validas["Valor"],
            type=type,
            label=label,
            color=color,
            toSecundary=toSecundary,
            showLegend=showLegend,
            setup=setup
        )
        list_series.append(serie)
        
        # Adicionado a série de leitura seca
        if instrumento_obj.porcentagem_seco>0:
            temSeco=True
            serie = Serie(
                X = instrumento_obj.leituras_secas["Data/Hora"],
                Y = instrumento_obj.leituras_secas["Valor"],
                type=type,
                label=label,
                color=color,
                toSecundary=toSecundary,
                showLegend=showLegend,
                setup=dict(marker="x",linestyle="")
                )
            list_series.append(serie)
        
        # Adicionado a série de leitura jorrantes
        if len(instrumento_obj.leituras_jorrantes.values)>0:
            temJorrante=True
            serie = Serie(
                X = instrumento_obj.leituras_jorrantes["Data/Hora"],
                Y = instrumento_obj.leituras_jorrantes["Valor"],
                type=type,
                label=label,
                color=color,
                toSecundary=toSecundary,
                showLegend=showLegend,
                setup=dict(marker="s",linestyle="")
                )
            list_series.append(serie)
        if instrumento!="AGLPL001":
            listaLimitesDatas.append(instrumento_obj.data_hora_minima)
            listaLimitesDatas.append(instrumento_obj.data_hora_maxima)
        if toSecundary:
            listaLimitesValoresSec.append(instrumento_obj.valor_maximo)
            listaLimitesValoresSec.append(instrumento_obj.valor_minimo)
        else:
            listaLimitesValores.append(instrumento_obj.valor_maximo)
            listaLimitesValores.append(instrumento_obj.valor_minimo)
            
        # Adicionando níveis conforme configuração na tabela
        dataData = pd.DataFrame([instrumento_obj.data_minima,instrumento_obj.data_maxima])
        if temAtencao:
            list_series.append(Serie(dataData,pd.DataFrame([instrumento_obj.atencao]),label="Nível de Atenção",color="black",showLegend=True,setup=dict(marker="s",linestyle="")))

    df_graph:pd.DataFrame = graphSetting[graphSetting["Nome do gráfico"]==grafico]
    title = df_graph["Nome do gráfico"].values[0]
    xInicial = df_graph["Data Inicial"].values[0]
    xFinal = df_graph["Data Final"].values[0]
    tituloYPrinc = df_graph["Título do Eixo Vertical Principal"].values[0]
    yInicial = df_graph["Y Inicial"].values[0]
    yFinal = df_graph["Y Final"].values[0]
    y2Inicial = df_graph["Y2 Inicial"].values[0]
    y2Final = df_graph["Y2 Final"].values[0]
    nMonthLocator = df_graph["Distância em Meses dos Tickers"].values[0]
    hasSecos = df_graph["Tem Seco"].values[0] #################################### OBSOLETO ############################## <<<-------
    
    if len(listaLimitesDatas)!=0:
        xlim = (
            retornarValorNaoNulo(xInicial,min(intervaloPerfeitoData(listaLimitesDatas))),
            retornarValorNaoNulo(xFinal,max(intervaloPerfeitoData(listaLimitesDatas)))
            )
        ylim = (
            retornarValorNaoNulo(yInicial,min(intervaloPerfeito(listaLimitesValores))),
            retornarValorNaoNulo(yFinal,max(intervaloPerfeito(listaLimitesValores)))
            )
        y2lim = (
            retornarValorNaoNulo(y2Inicial,min(intervaloPerfeito(listaLimitesValoresSec))),
            retornarValorNaoNulo(y2Final,max(intervaloPerfeito(listaLimitesValoresSec)))
            )
    else:
        xlim = (None,None)
        ylim = (None,None)
        y2lim = (None,None)
    periodo:pd.Timedelta = max(xlim) - min(xlim)
    periodo_meses = periodo.days//30>11
    if periodo_meses<15:
        nMonthLocator = 3
        log.warning(f"Gráfico {grafico} tem um período de ~{periodo_meses} mês(es), por isso o intervalo dos ticks foi atualizado para {nMonthLocator} meses.")
    xMajorLocator = MonthLocator(interval=int(nMonthLocator))
    if nMonthLocator==6:
        xMajorLocator = MonthLocator(bymonth=(1,7))

    hasSecundary = True # Considerando que todos os gráficos de níveis tem pluviometria, está sendo posto em Hardcode esse parâmetro

    setup_grafico = dict(
        xlim=xlim,
        ylim=ylim,
        y2lim=y2lim,
        yLabel=tituloYPrinc,
        # legendNcols = 6,
        xMajorLocator = xMajorLocator,
        xLabelFontsize = 10,
        yLabelFontsize = 10,
        y2LabelFontsize = 10,
        labelMajorSize = 12,
        linewidth=2.0
        )
    
    
    if temSeco:
        list_series.append(Serie(pd.DataFrame([],columns=["Data"]),pd.DataFrame([],columns=["Valor"]),label="Leituras Secas",color="black",showLegend=True,setup=dict(marker="x",linestyle="")))
    if temJorrante:
        list_series.append(Serie(pd.DataFrame([],columns=["Data"]),pd.DataFrame([],columns=["Valor"]),label="Leituras Jorrantes",color="black",showLegend=True,setup=dict(marker="s",linestyle="")))
    
    graph = Graphic(list_series,title=title,setup=setup_grafico,hasSecundary=hasSecundary,intervalX=[xInicial,xFinal])
    graph.render(toFilter=False)
    graph.save(path=f"images/nivelGrafico/{title}.png",showLog=True)

timer_load.get_delta_time_from_time_marker()