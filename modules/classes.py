
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

plt.rcParams.update({"legend.fontsize":14})

class Serie():
    def __init__(self,X=None,Y=None,type="plot",label="",toSecundary=False,showLegend=True) -> None:
        if X==None or Y==None:
            self.X = np.linspace(0.5, 3.5, 20)
            self.Y = 3+np.cos(self.X)
        else:
            self.X = X
            self.Y = Y
        self.type = type
        self.label = label # Atributos para recuperação da informação passada no construtor
        if showLegend:
            self.label_legend = label
        else:
            self.label_legend = ""
        self.toSecundary = toSecundary
        self.showLegend = showLegend
        pass
        
class Grafico():
    def __init__(self,
                 series:list[Serie]=[Serie(label="linha"),Serie(label="barra",type="bar"),Serie(toSecundary=True)],
                 width=12,
                 height=6,
                 ) -> None:
        # Figure
        self.fig:Figure = plt.figure(figsize=(width, height))
        
        # Axes
        self.ax:plt.Axes = self.fig.add_axes([0.1, 0.2, 0.8, 0.7])

        # Plotting all Serie's entities
        self.objectsPlot = []
        self.objectsBar = []
        self.objectsScatter = []

        self.hasSecundary = False        
        
        for serie in series:
            if serie.toSecundary:
                if not self.hasSecundary:
                    self.ax2 = self.ax.twinx()
                    self.hasSecundary = True
                # Plot Graph
                if serie.type=="plot":
                    self.objectsPlot.append(self.ax2.plot(serie.X, serie.Y, c='red', lw=2.5, label=serie.label_legend, zorder=10))

                # Bar Graph
                elif serie.type=="bar":
                    self.objectsBar.append(self.ax2.bar(serie.X, serie.Y,label=serie.label_legend))
            else:
                # Plot Graph
                if serie.type=="plot":
                    self.objectsPlot.append(self.ax.plot(serie.X, serie.Y, c='red', lw=2.5, label=serie.label_legend, zorder=10))

                # Bar Graph
                elif serie.type=="bar":
                    self.objectsBar.append(self.ax.bar(serie.X, serie.Y,label=serie.label_legend))
                    pass

        # Axis X
        self.ax.set_xlabel("x Axis label", fontsize=14)
        self.ax.set_xlim(0, 4)
        self.ax.tick_params(which='major', width=1.0, length=10, labelsize=14, axis="x")
        self.ax.tick_params(which='minor', width=1.0, length=5, labelsize=10, labelcolor='0.25', axis="x")
        self.ax.xaxis.set_major_locator(MultipleLocator(1.000))
        self.ax.xaxis.set_major_formatter("{x:.0f}") # Comentar a linha para retirar o número
        self.ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        self.ax.xaxis.set_minor_formatter("{x:.2f}") # Comentar a linha para retirar o número

        # Axis Y
        self.ax.set_ylabel("y Axis label", fontsize=14)
        self.ax.set_ylim(0, 4)
        self.ax.tick_params(which='major', width=1.0, length=10, labelsize=14, axis="y")
        self.ax.tick_params(which='minor', width=1.0, length=5, labelsize=10, labelcolor='0.25', axis="y")
        self.ax.yaxis.set_major_locator(MultipleLocator(1.000))
        self.ax.yaxis.set_major_formatter("{x:.0f}") # Comentar a linha para retirar o número
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(4))
        self.ax.yaxis.set_minor_formatter("{x:.2f}") # Comentar a linha para retirar o número
        
        # Axis Y2        
        if self.hasSecundary:
            self.ax2.set_ylabel("y Axis label", fontsize=14)
            self.ax2.set_ylim(0, 4)
            self.ax2.tick_params(which='major', width=1.0, length=10, labelsize=14, axis="y")
            self.ax2.tick_params(which='minor', width=1.0, length=5, labelsize=10, labelcolor='0.25', axis="y")
            self.ax2.yaxis.set_major_locator(MultipleLocator(1.000))
            self.ax2.yaxis.set_major_formatter("{x:.0f}") # Comentar a linha para retirar o número
            self.ax2.yaxis.set_minor_locator(AutoMinorLocator(4))
            self.ax2.yaxis.set_minor_formatter("{x:.2f}") # Comentar a linha para retirar o número
        
        
        self.ax.set_title("Anatomy of a figure", fontsize=20, verticalalignment='bottom')
        
        
        # self.ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
        # self.ax.plot(X, Y2, c='C1', lw=2.5, label="Orange signal")
        # self.ax.plot(X[::3], Y3[::3], linewidth=0, markersize=9, marker='s', markerfacecolor='none', markeredgecolor='C4', markeredgewidth=2.5)
        
        self.ax.legend(loc="upper center", bbox_to_anchor=(0.5,-0.2), ncols=5, borderaxespad=0.1)
        
        # self.fig.patch.set(linewidth=4, edgecolor='0.5')
        self.fig.savefig("1.png")

class Serie3D(Serie):
    def __init__(self, X=None, Y=None, Z=None, type="scatter", label="", toSecundary=False, showLegend=True) -> None:
        self.Z = Z
        super().__init__(X, Y, type, label, toSecundary, showLegend)


class Grafico3D(Grafico):
    def __init__(self, series: list[Serie3D], width=7.5, height=7.5) -> None:
        """!!!!!! Ainda não implementado !!!!!!"""
        super().__init__(series, width, height)

Grafico()
