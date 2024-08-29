
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter,DayLocator,MonthLocator,YearLocator
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from matplotlib.pyplot import rcParams

plt.rcParams.update({"legend.fontsize":14})

class Serie():
    def __init__(self,X=None,Y=None,type="plot",label="",color=None,toSecundary=False,showLegend=True,barWidth=0.8,setup=dict()) -> None:
        self.setup = dict(
            par1 = "Exemplo de parâmetro padrão"
        )
        self.setup.update(setup)
        
        if X==None or Y==None:
            self.X = np.linspace(0.5, 3.5, 20)
            self.Y = 3+np.cos(self.X)
        else:
            self.X = X
            self.Y = Y
        self.type = type
        self.color = color
        self.label = label # Atributos para recuperação da informação passada no construtor
        if showLegend:
            self.label_legend = label
        else:
            self.label_legend = ""
        self.toSecundary = toSecundary
        self.showLegend = showLegend
        if self.type=="bar":
            if barWidth==0:
                self.width = (max(self.X)-min(self.X))/(len(self.X)-1)
            else:
                self.width = barWidth
        pass
    def render(self,axes:plt.Axes):
        """Ainda não implementado"""
        if self.type == "plot":
            self.art = axes.plot()
        elif self.type == "bar":
            self.art = axes.bar()            
        pass
        
class Grafico():
    def __init__(self,
                 series:list[Serie],
                 title:str = "",
                 setup:dict=dict()
                 ) -> None:
        self.title = title
        
        # Config
        self.setup:dict = dict(
            width=12,
            height=6,
            xlim = (None,None),
            ylim = (None,None),
            y2lim = (None,None),
            xMajorFormatter = DateFormatter("%b/%Y"),
            xMinorFormatter = "",
            yMajorFormatter = "{x:.2f}",
            yMinorFormatter = "",
            y2MajorFormatter = "{x:.2f}",
            y2MinorFormatter = "",
            xMajorLocator = MonthLocator(interval=6),
            xMinorLocator = MonthLocator(interval=6),
            yMajorLocator = MultipleLocator(2.),
            yMinorLocator = AutoMinorLocator(2),
            y2MajorLocator = MultipleLocator(2.),
            y2MinorLocator = AutoMinorLocator(2),
            invertSidesYAxis = True,
            figureAutoLayout = True,
            rectFigureBaseAdd_axes = [0.1, 0.2, 0.8, 0.7]
        )
        self.setup.update(setup)
        
        
        # Hardcoded config ######################### Retirar na versão final ######################################
        self.setup.update(dict(
            xMajorFormatter = "{x:.0f}",
            xMajorLocator = MultipleLocator(2.)
            ))
        ###########################################################################################################
        
        # Setup Figure and Axes
        rcParams["figure.autolayout"] = self.setup["figureAutoLayout"]
        if self.setup["figureAutoLayout"]:
            aux = plt.subplots(figsize=(self.setup["width"], self.setup["height"]))
            self.fig:Figure = aux[0]
            self.ax:plt.Axes = aux[1]
            
            # User Warning
            if "rectFigureBaseAdd_axes" in setup.keys():
                print("User Warning: setup['rectFigureBaseAdd_axes'] não foi usado pois self.setup['figureAutoLayout']==True. Aconselha-se alterar o setup['figureAutoLayout'] para False.")
        
        else:
            # Figure
            self.fig:Figure = plt.figure(figsize=(self.setup["width"], self.setup["height"]))            
            # Axes
            self.ax:plt.Axes = self.fig.add_axes(self.setup["rectFigureBaseAdd_axes"])
        

        # Plotting all Serie's entities
        self.objectsPlot = []
        self.objectsBar = []
        self.objectsScatter = []

        self.hasSecundary = False        
        
        for serie in series:
            if serie.toSecundary:
                if not self.hasSecundary:
                    self.ax2 = self.ax.twinx()
                    if self.setup["invertSidesYAxis"]:
                        # Inverting sides
                        self.ax.yaxis.set_label_position("right")
                        self.ax.yaxis.tick_right()
                        self.ax2.yaxis.set_label_position("left")
                        self.ax2.yaxis.tick_left()
                    self.hasSecundary = True
                # Plot Graph
                if serie.type=="plot":
                    self.objectsPlot.append(self.ax2.plot(serie.X, serie.Y, color=serie.color, lw=2.5, label=serie.label_legend, zorder=10))

                # Bar Graph
                elif serie.type=="bar":
                    self.objectsBar.append(self.ax2.bar(serie.X, serie.Y, width=serie.width, color=serie.color, label=serie.label_legend))
            else:
                # Plot Graph
                if serie.type=="plot":
                    self.objectsPlot.append(self.ax.plot(serie.X, serie.Y, color=serie.color, lw=2.5, label=serie.label_legend, zorder=10))

                # Bar Graph
                elif serie.type=="bar":
                    self.objectsBar.append(self.ax.bar(serie.X, serie.Y, width=serie.width, color=serie.color, label=serie.label_legend))
                    pass

        # Axis X
        self.ax.set_xlabel("x Axis label", fontsize=14)
        self.ax.set_xlim(self.setup["xlim"][0],self.setup["xlim"][1])
        self.ax.tick_params(which='major', width=1.0, length=10, labelsize=14, axis="x")
        self.ax.tick_params(which='minor', width=1.0, length=5, labelsize=10, labelcolor='0.25', axis="x")
        self.ax.xaxis.set_major_locator(self.setup["xMajorLocator"])
        self.ax.xaxis.set_major_formatter(self.setup["xMajorFormatter"])
        self.ax.xaxis.set_minor_locator(self.setup["xMinorLocator"])
        self.ax.xaxis.set_minor_formatter(self.setup["xMinorFormatter"])

        # Axis Y
        self.ax.set_ylabel("y Axis label", fontsize=14)
        self.ax.set_ylim(self.setup["ylim"][0],self.setup["ylim"][1])
        self.ax.tick_params(which='major', width=1.0, length=10, labelsize=14, axis="y")
        self.ax.tick_params(which='minor', width=1.0, length=5, labelsize=10, labelcolor='0.25', axis="y")
        self.ax.yaxis.set_major_locator(self.setup["yMajorLocator"])
        self.ax.yaxis.set_major_formatter(self.setup["yMajorFormatter"])
        self.ax.yaxis.set_minor_locator(self.setup["yMinorLocator"])
        self.ax.yaxis.set_minor_formatter(self.setup["yMinorFormatter"])
        
        # Axis Y2        
        if self.hasSecundary:
            self.ax2.set_ylabel("y2 Axis label", fontsize=14)
            self.ax2.set_ylim(self.setup["y2lim"][0],self.setup["y2lim"][1])
            self.ax2.tick_params(which='major', width=1.0, length=10, labelsize=14, axis="y")
            self.ax2.tick_params(which='minor', width=1.0, length=5, labelsize=10, labelcolor='0.25', axis="y")
            self.ax2.yaxis.set_major_locator(self.setup["y2MajorLocator"])
            self.ax2.yaxis.set_major_formatter(self.setup["y2MajorFormatter"])
            self.ax2.yaxis.set_minor_locator(self.setup["y2MinorLocator"])
            self.ax2.yaxis.set_minor_formatter(self.setup["y2MinorFormatter"])
        
        # Set Title
        if len(self.title):
            self.ax.set_title(self.title, fontsize=20, verticalalignment='bottom')

        # Set Legend
        handles1, labels1 = self.ax.get_legend_handles_labels()
        handles = handles1
        labels = labels1
        if self.hasSecundary:
            handles2, labels2 = self.ax2.get_legend_handles_labels()
            if self.setup["invertSidesYAxis"]:
                handles = handles2 + handles
                labels = labels2 + labels
            else:
                handles += handles2
                labels += labels2
        self.handles, self.labels = handles, labels
        self.ax.legend(self.handles, self.labels, loc="upper center", bbox_to_anchor=(0.5,-0.2), ncols=5, borderaxespad=0.1)
        return

    def save (self,path:str):
        self.fig.savefig(path)

class Serie3D(Serie):
    def __init__(self, X=None, Y=None, Z=None, type="scatter", label="", toSecundary=False, showLegend=True) -> None:
        """!!!!!! Ainda não implementado !!!!!!"""
        self.Z = Z
        super().__init__(X, Y, type, label, toSecundary, showLegend)


class Grafico3D(Grafico):
    def __init__(self, series: list[Serie3D], width=7.5, height=7.5) -> None:
        """!!!!!! Ainda não implementado !!!!!!"""
        super().__init__(series, width, height)

graph = Grafico(series=[Serie(label="barra",type="bar",color="red"),Serie(label="plot",color="yellow"),Serie(label="plot2",toSecundary=True,color="blue")])
graph.save("1.png")
