from modules import log, Timer
log.setLevel("INFO")
timer_ = Timer()
timer_.set_time_marker("carregamento e renderização")

log.info("Programa iniciado")

import datetime
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from modules.functions import readSheets
from modules.classes import *
import matplotlib.pyplot as plt

# Variável abaixo indicam as datas das séries a SEREM OCULTADAS NOS GRÁFICOS
# INSERIDO EM 04/11/2024
series_para_ocultar = [
    '14/05/2021',
    '19/05/2021',
    '26/05/2021',
    '02/06/2021',
    '11/06/2021',
    '17/06/2021',
    '23/06/2021',
    '30/06/2021',
    '12/07/2021',
    '22/07/2021',
    '29/07/2021',
    '02/08/2021',
    '12/08/2021',
    '17/08/2021',
    '26/08/2021',
    '03/09/2021',
    '08/09/2021',
    '16/09/2021',
    '23/09/2021',
    '14/10/2021',
    '18/10/2021',
    '24/10/2021',
    '01/11/2021',
    '07/11/2021',
    '16/11/2021',
    '17/11/2021',
    '01/12/2021',
    '07/12/2021',
    '15/12/2021',
    '20/12/2021',
    '27/12/2021',
    '13/01/2022',
    '20/01/2022',
    '26/01/2022',
    '02/02/2022',
    '10/02/2022',
    '17/02/2022',
    '02/03/2022',
    '13/03/2022',
    '14/03/2022',
    '31/03/2022',
    '12/04/2022',
    '19/04/2022',
    '27/04/2022',
    '05/05/2022',
    '10/05/2022',
    '17/05/2022',
    '25/05/2022',
    '02/06/2022',
    '07/06/2022',
    '14/06/2022',
    '21/06/2022',
    '28/06/2022',
    '15/07/2022',
    '20/07/2022',
    '26/07/2022',
    '04/08/2022',
    '10/08/2022',
    '16/08/2022',
    '22/08/2022',
    '30/08/2022',
    '06/09/2022',
    '23/09/2022',
    '30/09/2022',
    '13/10/2022',
    '20/10/2022',
    '08/11/2022',
    '17/11/2022',
    '02/12/2022',
    '21/12/2022',
    '16/01/2023',
    '04/02/2023',
    '18/02/2023',
    '06/03/2023',
    '18/03/2023',
    '18/04/2023',
    '04/05/2023',
    '19/05/2023',
    '06/06/2023',
    '26/06/2023',
    '21/07/2023',
    '03/08/2023',
    '21/08/2023',
    '01/09/2023',
    '25/09/2023',
    '23/10/2023',
    '13/11/2023',
    '21/11/2023',
    '08/12/2023',
    '20/12/2023',
    '30/01/2024',
    '07/02/2024',
    '27/02/2024',
    '14/03/2024',
    '25/03/2024',
    '26/04/2024',
    '14/05/2024',
    '06/06/2024'
    ]

setup_inclinometro = dict(
    width = 6, # Antes: 9 (atualizado em 04/11/2024)
    height = 12,
    xMajorFormatter = FuncFormatter(getFunctionToFuncFormatter(2)),
    yMajorFormatter = FuncFormatter(getFunctionToFuncFormatter(1)),
    y2MajorFormatter = FuncFormatter(getFunctionToFuncFormatter(1)),
    xMajorLocator = MultipleLocator(4), # Antes: AutoLocator() (atualizado em 04/11/2024)
    xMinorLocator = AutoMinorLocator(2), # Antes: AutoMinorLocator(5) (atualizado em 04/11/2024)
    yMajorLocator = MultipleLocator(5), # Antes: AutoLocator() (atualizado em 04/11/2024)
    yMinorLocator = AutoMinorLocator(1), # Antes: AutoMinorLocator(10) (atualizado em 04/11/2024)
    yLabelFontsize = 12,
    yLabel = "Profundidade (m)",
    xLabelFontsize = 12,
    xLabel = "Deslococamento (m)",
    legendFonteSize = 11,
    legendNcols = 1, # Antes: 3 (atualizado em 04/11/2024) - Foi diminuido de 3 para 1 por causa do filtro de datas do gráfico, por isso não há necessidade de tantas colunas
    legendBbox_to_anchor = (1.05, 1),
    legendLoc='upper left',
    labelTitleFontsize = 14,
)

dataTree = dict(
    inc001 = dict(
        incName = "INC-01",
        baseFile = "data/Modelo-INC01.xlsx",
        id_header = 16,
        blacklist = []+series_para_ocultar, # Inserido a série para ocultar a grande quantidade de dados
        depth = -46,
        deslocMax = 20.0,
        checksumMax = 1,
        desvioMax = 1,
        facemax = 1,
        perfilmax = 600,
    ),
    inc002 = dict(
        incName = "INC-02",
        baseFile = "data/Modelo-INC02.xlsx",
        blacklist = ["12/04/2022"],
        id_header = 16,
        depth = -28,
        deslocMax = 20.0,
        checksumMax = 1,
        desvioMax = 1,
        facemax = 1,
        perfilmax = 600,
    ),
    inc002_2 = dict(
        incName = "INC-02",
        baseFile = "data/Modelo-INC02-2.xlsx",
        blacklist = [],
        id_header = 16,
        depth = -31,
        deslocMax = 20,
        checksumMax = 1,
        desvioMax = 1,
        facemax = 1,
        perfilmax = 600,
    ),
    
    axisX = {
        "desloc_A":dict(label = "Deslocamento  - eixo A (mm)", xmax = 8), # Valor anterior 20 (alterado em 04/11/2024)
        "desloc_B":dict(label="Deslocamento  - eixo B (mm)", xmax = 8), # Valor anterior 20 (alterado em 04/11/2024)
        # "checksum_A":dict(label="Checksum - eixo A (mm)", xmax = 6),
        # "checksum_B":dict(label="Checksum - eixo B (mm)", xmax = 6),
        # "desvio_A":dict(label="Desvio (mm) - eixo A", xmax = 20),
        # "desvio_B":dict(label="Desvio (mm) - eixo B", xmax = 20),
        # "face_A+_mm":dict(label="Leitura A+ (mm)", xmax = 20),
        # "face_A-_mm":dict(label="Leitura A- (mm)", xmax = 20),
        # "face_B+_mm":dict(label="Leitura B+ (mm)", xmax = 20),
        # "face_B-_mm":dict(label="Leitura B- (mm)", xmax = 20),
        # "perfil_A":dict(label="Perfil A - (mm)", xmax = 600),
        # "perfil_B":dict(label="Perfil B - (mm)", xmax = 600),
    },
    axisY = {"Depth":"Profundidade (m)"}
)

lista_inc = [
    "inc001",
    # "inc002",
    "inc002_2"
    ]


for inc in lista_inc:
    
    baseFile = dataTree[inc]["baseFile"]
    blacklist = dataTree[inc]["blacklist"]
    id_header = dataTree[inc]["id_header"]
    depth = dataTree[inc]["depth"]
    deslocMax = dataTree[inc]["deslocMax"]
    checksumMax = dataTree[inc]["checksumMax"]
    desvioMax = dataTree[inc]["desvioMax"]
    facemax = dataTree[inc]["facemax"]
    perfilmax = dataTree[inc]["perfilmax"]
    axisY = list(dataTree["axisY"].keys())[0]
    yLabel = dataTree["axisY"][axisY]
    
    planilhas = readSheets(baseFile,showLog=False)
    
    for axisX in dataTree["axisX"].keys():
        
        xLabel = dataTree["axisX"][axisX]["label"]
        series = []
        alpha = 1
        nPlanilha = len(planilhas.keys())
        for nomePlanilha in planilhas.keys():
            log.info(f"Lendo '{nomePlanilha}' do '{baseFile}'")
            df = planilhas[nomePlanilha].copy(deep=True)
            cabecalho = df.iloc[0:id_header]
            df.columns = df.iloc[id_header]
            df = df.drop(index=list(range(id_header+1)))
            X = df[axisX]
            Y = df[axisY]
            nomeSerie = cabecalho.iloc[6,1]
            if not isinstance(nomeSerie,str):
                nomeSerie = cabecalho.iloc[6,1].strftime("%d/%m/%Y")
            if (str(nomeSerie) in blacklist) or ("desconsiderar" in nomePlanilha.lower()):
                log.warning(f"Planilha '{nomePlanilha}' desconsiderada.")
                continue
            serie = Serie(X,Y,label=nomeSerie,
                          setup=dict(markersize=2,marker="o",linewidth=1.2,alpha=alpha),
                          showLegend=True)
            series.append(serie)
        graph = Graphic(series,
                        title=f"{axisX}-{dataTree[inc]['incName']}",
                        setup=setup_inclinometro)
        xmin = -dataTree["axisX"][axisX]["xmax"]
        xmax = +dataTree["axisX"][axisX]["xmax"]
        graph.update_setup(dict(xLabel=xLabel,yLabel=yLabel,ylim=(depth,0),xlim=(xmin,xmax)))
        graph.render(False)
        log.debug(f"{min(graph.xValores)},{max(graph.xValores)}")
        graph.save(path=f"images/incGrafico/{inc}-{axisX}.png",showLog=True)

timer_.get_delta_time_from_time_marker("carregamento e renderização")