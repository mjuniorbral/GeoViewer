from modules import Timer
from modules import log
log.setLevel("ERROR")
timer_load = Timer()
timer_load.set_time_marker()
log.info("Iniciando carregamento de dados...")

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
    maximoValido
    )
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

setups_series_niveis_notaveis = {
    "Nível de Atenção": dict(
        label = "Nível de Atenção",
        color = "#ffbb00",
        type = "plot",
        setup = dict(marker="",linestyle="--",linewidth=1.0,alpha=1.),
        toSecundary=False,
        showLegend=True,
        ),
    "Nível de Alerta": dict(
        label = "Nível de Alerta",
        color = "orange",
        type = "plot",
        setup = dict(marker="",linestyle="--",linewidth=1.0,alpha=1.),
        toSecundary=False,
        showLegend=True,
        ),
    "Nível de Emergência": dict(
        label = "Nível de Emergência",
        color = "red",
        type = "plot",
        setup = dict(marker="",linestyle="--",linewidth=1.0,alpha=1.),
        toSecundary=False,
        showLegend=True,
        ),
    "Cota do Topo": dict(
        label = "Cota do Topo",
        color = "gray",
        type = "plot",
        setup = dict(marker="",linestyle="--",linewidth=1.0,alpha=1.),
        toSecundary=False,
        showLegend=True,
        ),
    "Cota da Base": dict(
        label = "Cota da Base",
        color = "gray",
        type = "plot",
        setup = dict(marker="",linestyle="--",linewidth=1.0,alpha=1.),
        toSecundary=False,
        showLegend=True,
        ),
    "Cota do Fundo": dict(
        label = "Cota do Fundo",
        color = "gray",
        type = "plot",
        setup = dict(marker="",linestyle="--",linewidth=1.0,alpha=1.),
        toSecundary=False,
        showLegend=True,
        ),
}

log.setLevel("CRITICAL")
timer_load.set_time_marker()
# Inicializando a variável de armazenamento dos instrumentos
listaInstrumentos = dict()

# Carregando os gráficos que serão renderizados
graphSetting:pd.DataFrame = graphSetting[graphSetting["Render"]==True]
for grafico in graphSetting["Nome do gráfico"]:
    # Inicialização das variáveis para cada gráfico
    temSeco = False
    temJorrante = False
    hasSecundary = False
    listaLimitesDatas = []
    listaLimitesValores = []
    listaLimitesValoresSec = []
    log.info(f"Construindo \"{grafico}\"")
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
        
        # Retirada das leituras fora do intervalo definido pelo Outlier na planilha Config
        if not pd.isna(outlier_max):
            df_filtered = df_filtered[df_filtered["Valor"]<outlier_max]
        if not pd.isna(outlier_max):
            df_filtered = df_filtered[df_filtered["Valor"]<outlier_max]
        
        # Criando o objeto Instrumento para extrair os valores
        cadastro_instrumento:pd.DataFrame = cadastro.loc[cadastro["Código"]==instrumento]
        # instrumento_obj = Instrumento(cadastro_instrumento.to_dict())
        try:
            instrumento_obj = Instrumento(cadastro_instrumento.to_dict(orient="records")[0])
        except Exception as m:
            print(cadastro_instrumento.values)
            print(f"{instrumento}: {m}")
            continue
        instrumento_obj.set_leituras(df_filtered[df_filtered["Código do Instrumento"]==instrumento_obj.codigo])
        listaInstrumentos[instrumento_obj.codigo] = instrumento_obj
        
        # Caso alguma série tenha secundário, podemos mudar para True a variável inicializada como False no início do loop do gráfico
        if toSecundary:
            hasSecundary = True
            
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
                showLegend=False,
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
                showLegend=False,
                setup=dict(marker="s",linestyle="")
                )
            list_series.append(serie)
        
        # Adicionando níveis notáveis conforme configuração na tabela
        
        # COMENTADO POR SER UMA OPÇÃO PIOR: Níveis notáveis estão apenas sobre o período de leitura
        # datas = pd.DataFrame([instrumento_obj.data_minima,instrumento_obj.data_maxima])
        
        # Níveis notáveis estão sobre todo o gráfico, considerando as leituras entre 01/01/1000 e 01/01/3000
        datas = pd.DataFrame([pd.Timestamp(day=1,month=1,year=1000),pd.Timestamp(day=1,month=1,year=3000)])
        if temAtencao:
            valor = instrumento_obj.atencao
            if valor:
                log.debug(f"{instrumento_obj.codigo} - Atenção {valor}")
                listaLimitesValores.append(valor)
                valores = pd.DataFrame([valor,valor])
                kwargs = setups_series_niveis_notaveis["Nível de Atenção"]
                list_series.append(Serie(datas,valores,**kwargs))
        if temAlerta:
            valor = instrumento_obj.alerta
            if valor:
                log.debug(f"{instrumento_obj.codigo} - Alerta {valor}")
                listaLimitesValores.append(valor)
                valores = pd.DataFrame([valor,valor])
                kwargs = setups_series_niveis_notaveis["Nível de Alerta"]
                list_series.append(Serie(datas,valores,**kwargs))
        if temEmerg:
            valor = instrumento_obj.emergencia
            if valor:
                log.debug(f"{instrumento_obj.codigo} - Emergência {valor}")
                listaLimitesValores.append(valor)
                valores = pd.DataFrame([valor,valor])
                kwargs = setups_series_niveis_notaveis["Nível de Emergência"]
                list_series.append(Serie(datas,valores,**kwargs))
        if temFundo_Base:
            valor = instrumento_obj.fundo_ou_base
            if valor:
                listaLimitesValores.append(valor)
                valores = pd.DataFrame([valor,valor])
                if instrumento_obj.label_cota_inferior == "fundo":
                    log.debug(f"{instrumento_obj.codigo} - Fundo {valor}")
                    kwargs = setups_series_niveis_notaveis["Cota do Fundo"]
                    list_series.append(Serie(datas,valores,**kwargs))
                if instrumento_obj.label_cota_inferior == "base":
                    log.debug(f"{instrumento_obj.codigo} - Base {valor}")
                    kwargs = setups_series_niveis_notaveis["Cota da Base"]
                    list_series.append(Serie(datas,valores,**kwargs))
        if temTopo:
            valor = instrumento_obj.topo
            if valor:
                log.debug(f"{instrumento_obj.codigo} - Topo {valor}")
                listaLimitesValores.append(valor)
                valores = pd.DataFrame([valor,valor])
                kwargs = setups_series_niveis_notaveis["Cota do Topo"]
                list_series.append(Serie(datas,valores,**kwargs))
        
        # Adição os valores das datas máximas e mínimas dos instrumentos sem ser a pluviometria na lista de limites de datas
        if instrumento!="AGLPL001":
            listaLimitesDatas.append(instrumento_obj.data_hora_minima)
            listaLimitesDatas.append(instrumento_obj.data_hora_maxima)
        
        # Adição os valores dos valores y do eixo secundário de todos os instrumentos
        if toSecundary:
            listaLimitesValoresSec.append(instrumento_obj.valor_maximo)
            listaLimitesValoresSec.append(instrumento_obj.valor_minimo)
        
        # Adição os valores dos valores y do eixo principal de todos os instrumentos
        else:
            listaLimitesValores.append(instrumento_obj.valor_maximo)
            listaLimitesValores.append(instrumento_obj.valor_minimo)
    
    # Importando entradas dos gráficos
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
    
    # Adicionando os valores de maior prioridade nas tuplas de limites dos gráficos, caso há valores nas variáveis de limites
    if len(listaLimitesDatas)!=0 and len(listaLimitesValores)!=0 and len(listaLimitesValoresSec)!=0:
        intervaloData = intervaloPerfeitoDataMes(listaLimitesDatas,dV=nMonthLocator)
        intervaloValor, dVy = intervaloPerfeito(listaLimitesValores)
        intervaloValorSec, dVy2 = intervaloPerfeito(listaLimitesValoresSec)
        xlim = (
            retornarValorNaoNulo(xInicial,min(intervaloData)),
            retornarValorNaoNulo(xFinal,max(intervaloData))
            )
        ylim = (
            retornarValorNaoNulo(yInicial,min(intervaloValor)),
            retornarValorNaoNulo(yFinal,max(intervaloValor))
            )
        y2lim = (
            retornarValorNaoNulo(y2Inicial,min(intervaloValorSec)),
            retornarValorNaoNulo(y2Final,max(intervaloValorSec))
            )
    else:
        xlim = (None,None)
        ylim = (None,None)
        y2lim = (None,None)
    
    # Verificando PERÍODOS PEQUENOS (<~15 MESES) para definir nMonthLocator
    periodo:pd.Timedelta = max(xlim) - min(xlim)
    periodo_meses = periodo.days//30
    if periodo_meses<15:
        nMonthLocator = 3
        log.warning(f"Gráfico {grafico} tem um período de ~{periodo_meses} mês(es), por isso o intervalo dos ticks foi atualizado para {nMonthLocator} meses.")
    
    # transformando o nMonthLocator em intervalos constantes dentro dos anos com a função monthByInterval
    monthLocatorValor = monthByInterval(nMonthLocator)
    if monthLocatorValor[0]:
        xMajorLocator = MonthLocator(bymonth=monthLocatorValor[1])
    else:
        xMajorLocator = MonthLocator(interval=monthLocatorValor[2])


    # Colocando as variáveis construídas no loop no setup do gráfico
    setup_grafico = dict(
        xlim=xlim,
        ylim=ylim,
        y2lim=y2lim,
        yLabel=tituloYPrinc,
        yMajorLocator = MultipleLocator(dVy),
        y2MajorLocator = MultipleLocator(dVy2),
        # legendNcols = 6,
        xMajorLocator = xMajorLocator,
        xLabelFontsize = 10,
        yLabelFontsize = 10,
        y2LabelFontsize = 10,
        labelMajorSize = 12,
        linewidth=2.0
        )
    
    # Inserindo as séries para as legendas de Seco e Jorrante
    if temSeco:
        list_series.append(Serie(pd.DataFrame([],columns=["Data"]),pd.DataFrame([],columns=["Valor"]),label="Leituras Secas",color="black",showLegend=True,setup=dict(marker="x",linestyle="")))
    if temJorrante:
        list_series.append(Serie(pd.DataFrame([],columns=["Data"]),pd.DataFrame([],columns=["Valor"]),label="Leituras Jorrantes",color="black",showLegend=True,setup=dict(marker="s",linestyle="")))
    
    # Construindo o gráfico, renderizando e salvando
    graph = Graphic(list_series,title=title,setup=setup_grafico,hasSecundary=hasSecundary,intervalX=[xInicial,xFinal])
    graph.render(toFilter=False)
    graph.save(path=f"images/nivelGrafico/{title}.png",showLog=True)

timer_load.get_delta_time_from_time_marker()