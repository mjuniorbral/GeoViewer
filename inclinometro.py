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
    yMajorFormatter = FuncFormatter(getFunctionToFuncFormatter(1)),
    y2MajorFormatter = FuncFormatter(getFunctionToFuncFormatter(1)),
    xMajorLocator = AutoLocator(),
    xMinorLocator = AutoMinorLocator(1),
    yMinorLocator = AutoMinorLocator(),
    yMajorLocator = AutoLocator(),
    yLabelFontsize = 12,
    yLabel = "Profundidade (m)",
    xLabelFontsize = 12,
    xLabel = "Deslococamento (m)",
    legendFonteSize = 11,
    legendNcols = 3,
    legendBbox_to_anchor = (1.05, 1),
    legendLoc='upper left',
)

dataTree = dict(
    inc001 = dict(
        incName = "INC-01",
        baseFile = "data/Modelo-INC01.xlsx",
        id_header = 16,
        blacklist = [],
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
        "desloc_A":dict(label = "Deslocamento  - eixo A (mm)", xmax = 20),
        "desloc_B":dict(label="Deslocamento  - eixo B (mm)", xmax = 20),
        "checksum_A":dict(label="Checksum - eixo A (mm)", xmax = 6),
        "checksum_B":dict(label="Checksum - eixo B (mm)", xmax = 6),
        "desvio_A":dict(label="Desvio (mm) - eixo A", xmax = 20),
        "desvio_B":dict(label="Desvio (mm) - eixo B", xmax = 20),
        "face_A+_mm":dict(label="Leitura A+ (mm)", xmax = 20),
        "face_A-_mm":dict(label="Leitura A- (mm)", xmax = 20),
        "face_B+_mm":dict(label="Leitura B+ (mm)", xmax = 20),
        "face_B-_mm":dict(label="Leitura B- (mm)", xmax = 20),
        "perfil_A":dict(label="Perfil A - (mm)", xmax = 600),
        "perfil_B":dict(label="Perfil B - (mm)", xmax = 600),
    },
    axisY = {"Depth":"Profundidade (m)"}
)

lista_inc = [
    "inc001",
    "inc002",
    "inc002_2"
    ]

print("Programa iniciado")

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
            # print(f"Lendo '{nomePlanilha}' do '{baseFile}'")
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
                # print(f"Planilha '{nomePlanilha}' desconsiderada.")
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
        # print(min(graph.xValores),max(graph.xValores))
        graph.save(path=f"images/incGrafico/{inc}-{axisX}.png")
        print(f"Imagem salva: images/incGrafico/{inc}-{axisX}.png")
