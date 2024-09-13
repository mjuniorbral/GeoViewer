import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from modules.functions import readSheets
from modules.classes import *
import matplotlib.pyplot as plt

setup_inclinometro = dict(
    width = 5,
    height = 12,
    xMajorFormatter = FuncFormatter(getFunctionToFuncFormatter(4)),
    # xMinorFormatter = "",
    yMajorFormatter = FuncFormatter(getFunctionToFuncFormatter(2)),
    # yMinorFormatter = "",
    y2MajorFormatter = FuncFormatter(getFunctionToFuncFormatter(2)),
    # y2MinorFormatter = "",
    xMajorLocator = AutoLocator(),
    xMinorLocator = AutoMinorLocator(1),
    yMinorLocator = AutoMinorLocator(),
    yMajorLocator = AutoLocator(),
    # ylim = (-31,0),
    # xlim = (-0.002,0.002),
    yLabelFontsize = 10,
    yLabel = "Profundidade (m)",
    xLabelFontsize = 10,
    xLabel = "Deslococamento (m)",
)

dataTree = dict(
    inc001 = dict(
        incName = "INC-01",
        baseFile = "data/Modelo-INC01.xlsx",
        id_header = 16,
        depth = -46,
        deslocMax = 20.0
    ),
    inc002 = dict(
        incName = "INC-02",
        baseFile = "data/Modelo-INC02.xlsx",
        id_header = 16,
        depth = -28,
        deslocMax = 20.0
    ),
    inc002_2 = dict(
        incName = "INC-02",
        baseFile = "data/Modelo-INC02-2.xlsx",
        id_header = 16,
        depth = -31,
        deslocMax = 1.5
    ),
    
    axisX = {
        "desloc_A":"Deslocamento  - eixo A (mm)",
        "desloc_B":"Deslocamento  - eixo B (mm)",
        # "Checksum A":"Checksum - eixo A (mm)",
        # "Checksum B":"Checksum - eixo B (mm)",
        # "desvio_A":"Desvio (mm) - eixo A",
        # "desvio_B":"Desvio (mm) - eixo B",
        # "face_A+_mm":"Leitura A+ (mm)",
        # "face_A-_mm":"Leitura A- (mm)",
        # "face_B+_mm":"Leitura B+ (mm)",
        # "face_B-_mm":"Leitura B- (mm)"
    },
    axisY = {"Depth":"Profundidade (m)"}
)

lista_inc = ["inc001","inc002","inc002_2"]
for inc in lista_inc:
    
    baseFile = dataTree[inc]["baseFile"]
    id_header = dataTree[inc]["id_header"]
    depth = dataTree[inc]["depth"]
    deslocMax = dataTree[inc]["deslocMax"]
    axisY = list(dataTree["axisY"].keys())[0]
    yLabel = dataTree["axisY"][axisY]
    
    planilhas = readSheets(baseFile)
    
    for axisX in dataTree["axisX"].keys():
        
        xLabel = dataTree["axisX"][axisX]
        series = []
        alpha = 0.0
        dAlpha = (1.-alpha)/len(planilhas.keys())
        for nomePlanilha in planilhas.keys():
            # print(f"Lendo '{nomePlanilha}' do '{baseFile}'...")
            df = planilhas[nomePlanilha].copy(deep=True)
            cabecalho = df.iloc[0:id_header]
            df.columns = df.iloc[id_header]
            df = df.drop(index=list(range(id_header+1)))
            X = df[axisX]
            Y = df[axisY]
            nomeSerie = cabecalho.iloc[6,1]
            serie = Serie(X,Y,label=nomePlanilha,
                          setup=dict(marker="",linewidth=0.9,alpha=alpha,color="red"),
                          showLegend=False)
            series.append(serie)
            alpha+=dAlpha

        graph = Graphic(series,
                        title=f"CONFIRMAR UNIDADES - {dataTree[inc]['incName']}",
                        setup=setup_inclinometro)
        graph.update_setup(dict(xLabel=xLabel,yLabel=yLabel,ylim=(depth,0),xlim=(-deslocMax,deslocMax)))
        graph.render(False)
        print(min(graph.xValores),max(graph.xValores))
        graph.save(path=f"images/incGrafico/{inc}-{axisX}.png")
