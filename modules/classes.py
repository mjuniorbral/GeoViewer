import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter,DayLocator,MonthLocator,YearLocator
from matplotlib.ticker import AutoLocator,AutoMinorLocator, MultipleLocator,FuncFormatter
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import rcParams
import datetime
if __name__=="__main__":
    from functions import pullValues, getFunctionToFuncFormatter, intervaloPerfeito, intervaloPerfeitoData, isEvery
    from annotate import *
else:
    from .functions import pullValues, getFunctionToFuncFormatter, intervaloPerfeito, intervaloPerfeitoData, isEvery
    from .annotate import *

plt.rcParams["legend.fontsize"] = 11
plt.rcParams['figure.constrained_layout.use'] = True

X = pd.DataFrame(np.linspace(0.5, 3.5, 20))
Y = pd.DataFrame(3+np.cos(X))

class Serie():
    
    def __init__(self,X,Y,type="plot",label=None,color=None,toSecundary=False,showLegend=True,setup=dict()) -> None:
        self.data:pd.DataFrame = pd.concat([X,Y],axis=1)
        self.data = self.data.dropna()
        self.nameX = self.data.columns[0]
        self.X = self.data.iloc[:,0]
        self.nameY = self.data.columns[1]
        self.Y = self.data.iloc[:,1]
        if len(self.X)!=0:
            self.xLim:tuple = (min(self.X),max(self.X))
        else:
            self.xLim:tuple = ()
            
        if len(self.Y)!=0:
            self.yLim:tuple = (min(self.Y),max(self.Y))
        else:
            self.yLim:tuple = ()

        self.axes = []
        self.type = type
        self.color = color
        self.label = label # Atributos para recuperação da informação passada no construtor
        if showLegend:
            self.label_legend = label
        else:
            self.label_legend = None
        self.toSecundary = toSecundary
        self.showLegend = showLegend
        if self.type == "plot":
            self.setup = dict(
                label=self.label_legend,   # Nome na legenda
                color=self.color,          # Cor das linhas e marcadores
                linestyle='-',             # Estilo da linha ('-', '--', '-.', ':', 'None', etc.)
                linewidth=1.5,             # Espessura da linha
                marker=None,               # Estilo do marcador ('o', 's', '^', '*', etc.)
                markersize=6.0,            # Tamanho do marcador
                markerfacecolor=None,      # Cor de preenchimento do marcador
                markeredgecolor=None,      # Cor da borda do marcador
                markeredgewidth=1.0,       # Largura da borda do marcador
                alpha=None,                # Transparência (0.0 a 1.0)
                zorder=1,                  # Ordem na sobreposição de elementos
                drawstyle='default',       # Estilo de conexão dos pontos ('default', 'steps-pre', etc.)
                )
        elif self.type == "bar":
            self.setup = dict(
                width=0.8,                 # Largura das barras
                bottom=0,                  # Base das barras
                align='center',            # Alinhamento das barras ('center' ou 'edge')
                color=self.color,          # Cor das barras
                edgecolor=self.color,      # Cor da borda das barras
                linewidth=None,            # Espessura da borda
                tick_label=None,           # Etiquetas do eixo x
                hatch=None,                # Padrão de preenchimento (e.g., '/', '\\', 'x', etc.)
                label=self.label_legend,   # Nome na legenda
                alpha=None,                # Transparência (0.0 a 1.0)
                zorder=100,                # Ordem na sobreposição de elementos
                # log=False,               # Escala logarítmica no eixo y
                error_kw=None,             # Parâmetros de erro adicionais para as barras de erro
                capsize=None,              # Tamanho das extremidades das barras de erro
            )
        self.setup.update(setup)
        pass

    def filterNCopy(self,xmin=None,xmax=None,ymin=None,ymax=None):
        dataFiltered = self.data
        if not xmin==None:
            dataFiltered = dataFiltered[self.data[self.nameX]>xmin]
        if not xmax==None:
            dataFiltered = dataFiltered[self.data[self.nameX]<xmax]
        if not ymin==None:
            dataFiltered = dataFiltered[self.data[self.nameY]>ymin]
        if not ymax==None:
            dataFiltered = dataFiltered[self.data[self.nameY]<ymax]
        X = dataFiltered[self.nameX]
        Y = dataFiltered[self.nameY]
        return Serie(X=X,Y=Y,type=self.type,label=self.label,color=self.color,toSecundary=self.toSecundary,showLegend=self.showLegend,setup=self.setup)
            
    def render(self,axes:plt.Axes):
        self.axes.append(axes)
        if self.type == "plot":
            kwargs = pullValues(
                self.setup,
                [
                "color",
                "label",
                "linewidth",
                "alpha",
                "zorder",
                "xerr",
                "yerr",
                # Exclusive Plot's Params
                "markersize",
                "linestyle",
                "marker",
                "markerfacecolor",
                "markeredgecolor",
                "markeredgewidth",
                "drawstyle",
                ]
                )
            self.art = axes.plot(self.X, self.Y,**kwargs)

        elif self.type == "bar":
            kwargs = pullValues(
                self.setup,
                ["color",
                "label",
                "linewidth",
                "alpha",
                "zorder",
                "xerr",
                "yerr",
                # Exclusive Bar's Params
                "tick_label",
                "hatch",
                "edgecolor",
                "capsize",
                "bottom",
                "width",
                "error_kw"])
            self.art = axes.bar(self.X, self.Y,**kwargs)
        return self.art
    def __repr__(self):
        return str(self.data)
        
class Graphic():
    def __init__(self,
                 series:list[Serie] = [],
                 title:str = "",
                 setup:dict=dict(),
                 hasSecundary:bool=False,
                 intervalX = [None,None]
                 ) -> None:
        self.series = series
        self.title = title
        self.objetcsArtist = []
        
        # Config
        self.setup:dict = dict(
            width=12,
            height=6,
            xlim = (None,None),
            ylim = (None,None),
            y2lim = (None,None),
            xMajorFormatter = DateFormatter("%m/%Y"),
            xMinorFormatter = "",
            yMajorFormatter = FuncFormatter(getFunctionToFuncFormatter(2)),
            yMinorFormatter = "",
            y2MajorFormatter = FuncFormatter(getFunctionToFuncFormatter(2)),
            y2MinorFormatter = "",
            xMajorLocator = MonthLocator(interval=1),
            xMinorLocator = MonthLocator(interval=1),
            yMajorLocator = AutoLocator(),
            yMinorLocator = AutoMinorLocator(2),
            y2MajorLocator = AutoLocator(),
            y2MinorLocator = AutoMinorLocator(1),
            invertSidesYAxis = False,
            figureAutoLayout = True,
            grid = True,
            rectFigureBaseAdd_axes = [0.1, 0.2, 0.8, 0.7],
            xLabelTicksRotation = 90,
            yLabelTicksRotation = 0,
            y2LabelTicksRotation = 0,
            axMargins = 0.1005,
            ax2Margins = 0.1005,

            xLabel = "",
            xLabelFontsize = 14,
            yLabel = "Elevação (m)",
            yLabelFontsize = 14,
            y2Label = "Precipitação (mm)",
            y2LabelFontsize = 14,
            tickMajorWidth = 1.,
            tickMinorWidth = 1.,
            tickMajorLength = 5,
            tickMinorLength = 3,
            labelMajorSize = 14,
            labelMinorSize = 10,
            labelMajorColor = "black",
            labelMinorColor = "black",
            legendFonteSize = 12,
            legendLoc="best",
            legendBbox_to_anchor=(0,0,1,1),
            legendNcols=5,
            labelTitleFontsize = 16
        )
        self.setup.update(setup)
        self.rendered = False
        
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
        
            
        self.hasSecundary = hasSecundary
        # Creating secundary axis, if exist
        for serie in self.series:
            if serie.toSecundary or self.hasSecundary:
                secondAxis = self.ax.twinx()
                # self.ax2 = secondAxis
                # Invert axis because self.ax2 must be the first generated
                self.ax,self.ax2 = secondAxis,self.ax
                self.hasSecundary = True
                break
        if self.setup["grid"]:
            if self.hasSecundary:
                self.ax2.grid(self.setup["grid"],axis="x")
                self.ax.grid(self.setup["grid"],"both",axis="y")
            else:
                self.ax.grid(self.setup["grid"],axis="x")
                self.ax.grid(self.setup["grid"],"both",axis="y")

        # Put the axis on the correct place
        if self.hasSecundary:
            if not self.setup['invertSidesYAxis']:
                self.ax.yaxis.set_label_position("left")
                self.ax.yaxis.tick_left()
                self.ax2.yaxis.set_label_position("right")
                self.ax2.yaxis.tick_right()
        else:
            if self.setup['invertSidesYAxis']:
                self.ax.yaxis.set_label_position("right")
                self.ax.yaxis.tick_right()
            pass
        
        # Set Axis Limits based the self.series
        xValores = []
        yValores = []
        y2Valores = []

        for serie in series:
            xValores.extend(serie.xLim)
            if serie.toSecundary:
                y2Valores.extend(serie.yLim)
            else:
                yValores.extend(serie.yLim)
        if self.setup["xlim"]==(None,None):
            if isEvery(xValores,pd.Timestamp):
                self.setup.update(dict(xlim=intervaloPerfeitoData(xValores)))
            else:
                self.setup.update(dict(xlim=intervaloPerfeito(xValores)))
        if self.setup["ylim"]==(None,None):
            self.setup.update(dict(ylim = intervaloPerfeito(yValores)))
        if self.setup["y2lim"]==(None,None):
            self.setup.update(dict(y2lim = intervaloPerfeito(y2Valores)))
        
        self.xValores = xValores
        self.yValores = yValores
        self.y2Valores = y2Valores
        
        return           

    def render(self,toFilter=False):
        
        if self.rendered:
            # Se foi feito, reiniciar objeto self
            Graphic.__init__(self,self.series,self.title,self.setup)
        
        # Plotting all Serie's entities
        
        for serie in self.series:
            xmin,xmax = self.setup["xlim"]
            if serie.toSecundary:
                if toFilter:
                    serie = serie.filterNCopy(**dict(xmin=xmin,xmax=xmax))
                self.objetcsArtist.append(serie.render(self.ax2))
            else:
                if toFilter:
                    serie = serie.filterNCopy(**dict(xmin=xmin,xmax=xmax))
                self.objetcsArtist.append(serie.render(self.ax))

        
        
        
        self.ax.set_xlabel(self.setup["xLabel"], fontsize=self.setup["xLabelFontsize"])
        self.ax.tick_params(which='major', axis="x", width=self.setup["tickMajorWidth"], length=self.setup["tickMajorLength"], labelsize=self.setup["labelMajorSize"], labelcolor=self.setup["labelMajorColor"])
        self.ax.tick_params(which='minor', axis="x", width=self.setup["tickMinorWidth"], length=self.setup["tickMinorLength"], labelsize=self.setup["labelMinorSize"], labelcolor=self.setup["labelMinorColor"])
        self.ax.set_xlim(self.setup["xlim"][0],self.setup["xlim"][1])
        self.ax.xaxis.set_major_locator(self.setup["xMajorLocator"])
        self.ax.xaxis.set_major_formatter(self.setup["xMajorFormatter"])
        self.ax.xaxis.set_minor_locator(self.setup["xMinorLocator"])
        self.ax.xaxis.set_minor_formatter(self.setup["xMinorFormatter"])
        self.ax.xaxis.set_tick_params(rotation=self.setup["xLabelTicksRotation"])
        if self.hasSecundary:
            self.ax2.set_xlabel(self.setup["xLabel"], fontsize=self.setup["xLabelFontsize"])
            self.ax2.tick_params(which='major', axis="x", width=self.setup["tickMajorWidth"], length=self.setup["tickMajorLength"], labelsize=self.setup["labelMajorSize"], labelcolor=self.setup["labelMajorColor"])
            self.ax2.tick_params(which='minor', axis="x", width=self.setup["tickMinorWidth"], length=self.setup["tickMinorLength"], labelsize=self.setup["labelMinorSize"], labelcolor=self.setup["labelMinorColor"])
            self.ax2.set_xlim(self.setup["xlim"][0],self.setup["xlim"][1])
            self.ax2.xaxis.set_major_locator(self.setup["xMajorLocator"])
            self.ax2.xaxis.set_major_formatter(self.setup["xMajorFormatter"])
            self.ax2.xaxis.set_minor_locator(self.setup["xMinorLocator"])
            self.ax2.xaxis.set_minor_formatter(self.setup["xMinorFormatter"])
            self.ax2.xaxis.set_tick_params(rotation=self.setup["xLabelTicksRotation"])

        # Axis Y
        self.ax.set_ylabel(self.setup["yLabel"], fontsize=self.setup["yLabelFontsize"])
        self.ax.tick_params(which='major', axis="y", width=self.setup["tickMajorWidth"], length=self.setup["tickMajorLength"], labelsize=self.setup["labelMajorSize"], labelcolor=self.setup["labelMajorColor"])
        self.ax.tick_params(which='minor', axis="y", width=self.setup["tickMinorWidth"], length=self.setup["tickMinorLength"], labelsize=self.setup["labelMinorSize"], labelcolor=self.setup["labelMinorColor"])
        self.ax.set_ylim(self.setup["ylim"][0],self.setup["ylim"][1])
        self.ax.yaxis.set_major_locator(self.setup["yMajorLocator"])
        self.ax.yaxis.set_major_formatter(self.setup["yMajorFormatter"])
        self.ax.yaxis.set_minor_locator(self.setup["yMinorLocator"])
        self.ax.yaxis.set_minor_formatter(self.setup["yMinorFormatter"])
        self.ax.yaxis.set_tick_params(rotation=self.setup["yLabelTicksRotation"])
        
        # Axis Y2        
        if self.hasSecundary:
            self.ax2.set_ylabel(self.setup["y2Label"], fontsize=self.setup["y2LabelFontsize"])
            self.ax2.tick_params(which='major', axis="y", width=self.setup["tickMajorWidth"], length=self.setup["tickMajorLength"], labelsize=self.setup["labelMajorSize"], labelcolor=self.setup["labelMajorColor"])
            self.ax2.tick_params(which='minor', axis="y", width=self.setup["tickMinorWidth"], length=self.setup["tickMinorLength"], labelsize=self.setup["labelMinorSize"], labelcolor=self.setup["labelMinorColor"])
            self.ax2.set_ylim(self.setup["y2lim"][0],self.setup["y2lim"][1])
            self.ax2.yaxis.set_major_locator(self.setup["y2MajorLocator"])
            self.ax2.yaxis.set_major_formatter(self.setup["y2MajorFormatter"])
            self.ax2.yaxis.set_minor_locator(self.setup["y2MinorLocator"])
            self.ax2.yaxis.set_minor_formatter(self.setup["y2MinorFormatter"])
            self.ax2.yaxis.set_tick_params(rotation=self.setup["y2LabelTicksRotation"])
        
        # Tirando o espaço 
        self.ax.margins(self.setup["axMargins"])
        if self.hasSecundary:
            self.ax2.margins(self.setup["ax2Margins"])
        # Set Title
        if len(self.title):
            self.ax.set_title(self.title, fontsize=self.setup["labelTitleFontsize"], verticalalignment='bottom')

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
        self.legend:Legend = self.ax.legend(self.handles, self.labels, loc=self.setup["legendLoc"], bbox_to_anchor=self.setup["legendBbox_to_anchor"], ncols=self.setup["legendNcols"], fontsize=self.setup["legendFonteSize"])
        self.fig.tight_layout()
        self.rendered = True
        return

    def get_series(self):
        return self.series
    def get_objetcsArtist(self):
        return self.objetcsArtist

    def set_series(self,series:list[Serie]):
        self.serie = series
    def append_series(self,newSeries:Serie):
        self.series.append(newSeries)
    def extend_series(self,newSeries:list[Serie]):
        self.series.extend(newSeries)

    def update_setup(self,setup:dict):
        self.setup.update(setup)

    def set_title(self,title:str):
        self.title = title

    def save (self,path:str,dpi=500,bbox_inches='tight',showLog=False):
        self.fig.savefig(path,dpi=dpi,bbox_inches=bbox_inches)
        print(f"[{datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}] Imagem salva: {path}") if showLog else 0
    
    def show (self,warn=True):
        self.fig.show(warn=warn)
        
class Serie3D(Serie):
    def __init__(self, X=None, Y=None, Z=None, type="scatter", label="", toSecundary=False, showLegend=True) -> None:
        """!!!!!! Ainda não implementado !!!!!!"""
        self.Z = Z
        super().__init__(X, Y, type, label, toSecundary, showLegend)


class Grafico3D(Graphic):
    def __init__(self, series: list[Serie3D], width=7.5, height=7.5) -> None:
        """!!!!!! Ainda não implementado !!!!!!"""
        super().__init__(series, width, height)

if __name__=="__main__":
    graph = Graphic(series=[Serie(X,Y,label="barra",type="bar",color="red"),Serie(X,Y,label="plot",color="yellow"),Serie(X,Y,label="plot2",toSecundary=True,color="blue")])
    graph.render()
    graph.save("1.png")
