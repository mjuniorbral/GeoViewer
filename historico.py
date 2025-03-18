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
PATH_LEITURAS = PATH_FOLDER+"Historico-até-01-FEV-2025.csv"
PATH_CADASTRO = PATH_FOLDER+"Cadastro_Instrumento-01-02-2025-154527.xlsx"
HEADER_CADASTRO = 0
PATH_CONFIG = PATH_FOLDER+"Config-Graficos.xlsx"
##########################################

PATH_OUT = "images/nivelGrafico/"

log.info("Importando leituras")
df = pd.read_csv(PATH_LEITURAS,delimiter=DFT_DELIMITER,encoding=DFT_ENCONDING,low_memory=False,dtype=DFT_DTYPE,parse_dates=DFT_PARSE_DATES,dayfirst=True,decimal=DFT_DECIMAL)
df["Hora da Medição"] = df["Hora da Medição"].dt.time
log.info("Leituras importadas e tratadas\n\n")

log.info("Importando cadastros")
cadastro = UnirCadastroGEOTEC(PATH_CADASTRO,header=HEADER_CADASTRO)
log.info("Cadastros importados\n\n")

log.info("Importando configurações")
settings = readSheets(PATH_CONFIG,showLog=False)
seriesSetting = settings["Séries"]
graphSetting = settings["Gráficos"]

leituras = df.copy(deep=True)

timer_load.get_delta_time_from_time_marker("carregamento")
log.info("Configurações importadas\n\n")

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

timer_load.set_time_marker("renderização")
# Inicializando a variável de armazenamento dos instrumentos
listaInstrumentos = dict()

log.info("Carregamento de dados finalizado.\n\n\n=============================")

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
        log.info(f"Definindo série de \"{instrumento}\"")
        # Extraindo dados sobre o instrumento a ser renderizado nessa iteração
        df_instr:pd.DataFrame = seriesToPlot[seriesToPlot["Instrumentos"]==instrumento]
        
        renderizarSerie = df_instr["Render"].values[0]
        if not renderizarSerie:
            # Avisando os instrumentos que não serão renderizados 
            log.info(f"\t{instrumento} não foi posto para ser renderizado no gráfico {grafico} conforme tabela de configuração.")
            continue
        
        # Isolando os dados do df_instr em variável do programa para melhorar a trabalhabilidade
        type = df_instr["Tipo"].values[0]
        label = df_instr["Instrumentos"].values[0]
        color = df_instr["Cor"].values[0]
        toSecundary = df_instr["Eixo Secundário"].values[0]
        outlier_max = df_instr["outlier_max"].values[0]
        outlier_min = df_instr["outlier_min"].values[0]
        showLegend = df_instr["Mostrar na Legenda"].values[0]
        marker = df_instr["Marcador"].values[0]
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
            leituras_removidas_outlier_max:pd.DataFrame = df_filtered[df_filtered["Código do Instrumento"]==instrumento][df_filtered["Valor"]>=outlier_max]
            if len(leituras_removidas_outlier_max)>0:
                log.info(f"{instrumento} no gráfico {grafico}: Filtro de outlier_max {outlier_max} retirou {len(leituras_removidas_outlier_max)} leitura(s) apresentadas abaixo:\n{leituras_removidas_outlier_max.to_string()}")
                df_filtered = df_filtered[df_filtered["Valor"]<outlier_max]
            else:
                log.info(f"{instrumento} no gráfico {grafico}: Filtro de outlier_max {outlier_max} não retirou nenhuma leitura.")

        if not pd.isna(outlier_min):
            leituras_removidas_outlier_min:pd.DataFrame = df_filtered[df_filtered["Código do Instrumento"]==instrumento][df_filtered["Valor"]<=outlier_min]
            if len(leituras_removidas_outlier_min)>0:
                log.info(f"{instrumento} no gráfico {grafico}: Filtro de outlier_min {outlier_min} retirou {len(leituras_removidas_outlier_min)} leitura(s) apresentadas abaixo:\n{leituras_removidas_outlier_min.to_string()}")
                df_filtered = df_filtered[df_filtered["Valor"]>outlier_min]
            else:
                log.info(f"{instrumento} no gráfico {grafico}: Filtro de outlier_min {outlier_min} não retirou nenhuma leitura.")
        
        # Criando o objeto Instrumento para extrair os valores
        cadastro_instrumento:pd.DataFrame = cadastro.loc[cadastro["Código"]==instrumento]
        try:
            instrumento_obj = Instrumento(cadastro_instrumento.to_dict(orient="records")[0])
        except Exception as m:
            log.critical(f"ERRO FATAL NO {instrumento}: {m}. Ele não será renderizado")
            log.critical(cadastro_instrumento.values)
            continue
        instrumento_obj.set_leituras(df_filtered[df_filtered["Código do Instrumento"]==instrumento_obj.codigo])
        if not instrumento_obj.possui_leituras:
            log.warning(f"Instrumento {instrumento_obj.codigo} não possui leitura, por isso não será renderizado.")
            continue
        listaInstrumentos[instrumento_obj.codigo] = instrumento_obj

        # Salvando relatório de descrição do instrumento no PATH_OUT
        instrumento_obj.descrever(file_path=PATH_OUT+str(instrumento_obj.codigo)+".txt")
        
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

        # Protótipo de visualização de séries problemáticas
        # Adicionando a série abaixo da cota de fundo apenas para os instrumentos na lista na condição abaixo (HARDCODED)
        if instrumento_obj.codigo in ["AGLEDMPZ028_A"]:
            serie = Serie(
                X = instrumento_obj.leituras_abaixo_base["Data/Hora"],
                Y = instrumento_obj.leituras_abaixo_base["Valor"],
                type=type,
                label=label+" (abaixo do fundo/base)",
                color=color,
                toSecundary=toSecundary,
                showLegend=True,
                setup=dict(marker=11,linestyle="",markersize=4)
                )
            list_series.append(serie)
            listaLimitesDatas.append(instrumento_obj.leituras_abaixo_base["Data/Hora"].min())
            
        
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
        
        # Adição os valores das datas máximas e mínimas dos instrumentos sem ser os instrumentos no eixo secundário
        if not toSecundary:
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
        log.info(f"\"{instrumento_obj.codigo}\" finalizado.\n=============================")
    
    # Importando entradas dos gráficos
    df_graph:pd.DataFrame = graphSetting[graphSetting["Nome do gráfico"]==grafico]
    title = df_graph["Nome do gráfico"].values[0]
    xInicial = df_graph["Data Inicial"].values[0]
    xFinal = df_graph["Data Final"].values[0]
    tituloYPrinc = df_graph["Título do Eixo Vertical Principal"].values[0]
    tituloY2Princ = df_graph["Título do Eixo Vertical Secundário"].values[0]
    yInicial = df_graph["Y Inicial"].values[0]
    yFinal = df_graph["Y Final"].values[0]
    y2Inicial = df_graph["Y2 Inicial"].values[0]
    y2Final = df_graph["Y2 Final"].values[0]
    nMonthLocator = df_graph["Distância em Meses dos Tickers"].values[0]
    
    # Adicionando os valores de maior prioridade nas tuplas de limites dos gráficos, caso há valores nas variáveis de limites
    if len(listaLimitesDatas)!=0:
        intervaloData = intervaloPerfeitoDataMes(listaLimitesDatas,dV=nMonthLocator)
        xlim = (
            retornarValorNaoNulo(xInicial,minimoValido(intervaloData)),
            retornarValorNaoNulo(xFinal,maximoValido(intervaloData))
            )
    else:
        xlim = (None,None)
        
    if len(listaLimitesValores)!=0:
        intervaloValor, dVy = intervaloPerfeito(listaLimitesValores)
        ylim = (
            retornarValorNaoNulo(yInicial,minimoValido(intervaloValor)),
            retornarValorNaoNulo(yFinal,maximoValido(intervaloValor))
            )
        nCasaY = get_decimal_places(dVy)
    else:
        ylim = (None,None)
        
    if len(listaLimitesValoresSec)!=0:
        intervaloValorSec, dVy2 = intervaloPerfeito(listaLimitesValoresSec)
        y2lim = (
            retornarValorNaoNulo(y2Inicial,minimoValido(intervaloValorSec)),
            retornarValorNaoNulo(y2Final,maximoValido(intervaloValorSec))
            )
        nCasaY2 = get_decimal_places(dVy2)
    else:
        y2lim = (None,None)
        # log.warning(f"O gráfico {grafico} não será renderizado por não haver leituras nele.")
        # continue
    
    if xlim != (None,None):
        # Verificando PERÍODOS PEQUENOS (<~15 MESES) para definir nMonthLocator
        periodo:pd.Timedelta = pd.Timedelta(maximoValido(xlim) - minimoValido(xlim))
        periodo_meses = periodo.days//30
        if periodo_meses<15:
            nMonthLocator = 3
            log.warning(f"Gráfico {grafico} tem um período de ~{periodo_meses} mês(es), por isso o intervalo dos ticks foi atualizado para {nMonthLocator} meses.")
    else:
        if len(list_series)<=1:
            if list_series[0].toSecundary:
                print("\n"*4)
                log.warning(f"\n\nO único instrumento que tem no gráfico {grafico} é o {list_series[0].label} e ele está no eixo secundário.\n\n-----------> Esse gráfico não pode ser gerado dessa forma com a versão atual do programa.\nPara corrigir, coloque ele no eixo principal.\nAperte ENTER para confirmar a ciência dessa informação")
                input_str = input("\n")
                continue
    
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
        y2Label=tituloY2Princ,
        # legendNcols = 6,
        xMajorLocator = xMajorLocator,
        xLabelFontsize = 10,
        yLabelFontsize = 10,
        y2LabelFontsize = 10,
        labelMajorSize = 12,
        linewidth=2.0
        )
    if ylim!=(None,None):
        setup_grafico.update(
            dict(
                yMajorLocator = MultipleLocator(dVy),
                yMajorFormatter = FuncFormatter(getFunctionToFuncFormatter(nCasaY))
                )
            )
    if y2lim!=(None,None):
        setup_grafico.update(
            dict(
                y2MajorLocator = MultipleLocator(dVy2),
                y2MajorFormatter = FuncFormatter(getFunctionToFuncFormatter(nCasaY2))
                )
            )
    # Inserindo as séries para as legendas de Seco e Jorrante
    if temSeco:
        list_series.append(Serie(pd.DataFrame([],columns=["Data"]),pd.DataFrame([],columns=["Valor"]),label="Leituras Secas",color="black",showLegend=True,setup=dict(marker="x",linestyle="")))
    if temJorrante:
        list_series.append(Serie(pd.DataFrame([],columns=["Data"]),pd.DataFrame([],columns=["Valor"]),label="Leituras Jorrantes",color="black",showLegend=True,setup=dict(marker="s",linestyle="")))
    log.debug("HEY!--------------------")
    # Construindo o gráfico, renderizando e salvando
    graph = Graphic(list_series,title=title,setup=setup_grafico,hasSecundary=hasSecundary,intervalX=[xInicial,xFinal])
    graph.render(toFilter=False)
    log.debug(list_series)
    graph.save(path=f"{PATH_OUT}{title}.png",showLog=True)
    log.info(f"\"{grafico}\" finalizado.\n =============================\n\n")

timer_load.get_delta_time_from_time_marker("renderização")

print("""
 .----------------.  .----------------.  .----------------.
| .--------------. || .--------------. || .--------------. |
| |  _________   | || |     _____    | || | ____    ____ | |
| | |_   ___  |  | || |    |_   _|   | || ||_   \  /   _|| |
| |   | |_  \_|  | || |      | |     | || |  |   \/   |  | |
| |   |  _|      | || |      | |     | || |  | |\  /| |  | |
| |  _| |_       | || |     _| |_    | || | _| |_\/_| |_ | |
| | |_____|      | || |    |_____|   | || ||_____||_____|| |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'
""")