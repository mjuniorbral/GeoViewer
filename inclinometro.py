import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from modules.functions import readSheets
from modules.classes import *
import matplotlib.pyplot as plt
import datetime

setup_inclinometro = dict(
    width = 9,
    height = 12,
    xMajorFormatter = FuncFormatter(getFunctionToFuncFormatter(2)),
    # xMinorFormatter = "",
    yMajorFormatter = FuncFormatter(getFunctionToFuncFormatter(1)),
    # yMinorFormatter = "",
    y2MajorFormatter = FuncFormatter(getFunctionToFuncFormatter(1)),
    # y2MinorFormatter = "",
    xMajorLocator = AutoLocator(),
    xMinorLocator = AutoMinorLocator(1),
    yMinorLocator = AutoMinorLocator(),
    yMajorLocator = AutoLocator(),
    # ylim = (-31,0),
    # xlim = (-0.002,0.002),
    yLabelFontsize = 12,
    yLabel = "Profundidade (m)",
    xLabelFontsize = 12,
    xLabel = "Deslococamento (m)",
    
    
    # legend.set_bbox_to_anchor((1.05, 1), loc='upper left', borderaxespad=0.)
    legendFonteSize = 11,
    legendNcols = 3,
    legendBbox_to_anchor = (1.05, 1),
    legendLoc='upper left',
    # borderaxespad=0.
    
)

dataTree = dict(
    inc001 = dict(
        incName = "INC-01",
        baseFile = "data/Modelo-INC01.xlsx",
        id_header = 16,
        blacklist = [],
        depth = -46,
        deslocMax = 10.0
    ),
    inc002 = dict(
        incName = "INC-02",
        baseFile = "data/Modelo-INC02.xlsx",
        blacklist = ["12/04/2022"],
        id_header = 16,
        depth = -28,
        deslocMax = 20.0
    ),
    inc002_2 = dict(
        incName = "INC-02",
        baseFile = "data/Modelo-INC02-2.xlsx",
        blacklist = [],
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

lista_inc = [
    # "inc001",
    "inc002",
    # "inc002_2"
    ]
for inc in lista_inc:
    
    baseFile = dataTree[inc]["baseFile"]
    blacklist = dataTree[inc]["blacklist"]
    id_header = dataTree[inc]["id_header"]
    depth = dataTree[inc]["depth"]
    deslocMax = dataTree[inc]["deslocMax"]
    axisY = list(dataTree["axisY"].keys())[0]
    yLabel = dataTree["axisY"][axisY]
    
    planilhas = readSheets(baseFile)
    
    for axisX in dataTree["axisX"].keys():
        
        xLabel = dataTree["axisX"][axisX]
        series = []
        alpha = 1
        nPlanilha = len(planilhas.keys())
        for nomePlanilha in planilhas.keys():
            # print(f"Lendo '{nomePlanilha}' do '{baseFile}'...")
            df = planilhas[nomePlanilha].copy(deep=True)
            cabecalho = df.iloc[0:id_header]
            df.columns = df.iloc[id_header]
            df = df.drop(index=list(range(id_header+1)))
            X = df[axisX]
            Y = df[axisY]
            nomeSerie = cabecalho.iloc[6,1]
            if (str(nomeSerie) in blacklist) or ("desconsiderar" in nomePlanilha.lower()):
                print(f"Planilha '{nomePlanilha}' desconsiderada.")
                continue
            serie = Serie(X,Y,label=nomeSerie,
                          setup=dict(markersize=2,marker="o",linewidth=1.2,alpha=alpha),
                          showLegend=True)
            series.append(serie)
        # alpha*=1/nPlanilha

        graph = Graphic(series,
                        title=f"{axisX}-{dataTree[inc]['incName']}",
                        setup=setup_inclinometro)
        graph.update_setup(dict(xLabel=xLabel,yLabel=yLabel,ylim=(depth,0),xlim=(-deslocMax,deslocMax)))
        graph.render(False)
        print(min(graph.xValores),max(graph.xValores))
        graph.save(path=f"images/incGrafico/{inc}-{axisX}.png")
