import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from modules.functions import readSheets
from modules.classes import *
import matplotlib.pyplot as plt

planilhas = readSheets("data/INC02-POR-2024-08.xlsx")
nomePlanilhaTeste = "27-08-2024"
df = planilhas[nomePlanilhaTeste].copy(deep=True)
df.columns = df.iloc[2]
df = df.drop(index=[0,1,2])
X = df["desloc_B"]
Y = df["Depth"]
series = [Serie(X,Y,label=nomePlanilhaTeste,setup=dict(
    marker="o"
))]

# Criar um setup padrão de inclinômetro baseado nesse setup, e implementar novas alterações
graph = Graphic(series,
                title="Desloc. Eixo - INC02",
                setup=dict(
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
                    ylim = (-31,0),
                    xlim = (-0.002,0.002),
                    yLabelFontsize = 10,
                    yLabel = "Profundidade (m)",
                    xLabelFontsize = 10,
                    xLabel = "Desloc. Horizontal (m)",
))
graph.render()
graph.save(path="images/inc002.png")
