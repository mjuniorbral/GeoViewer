import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter,DayLocator,MonthLocator,YearLocator
from matplotlib.ticker import AutoLocator,AutoMinorLocator, MultipleLocator,FuncFormatter
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import rcParams

from pandas import (
    Series,
    DataFrame,
    Timestamp,
    Timedelta,
    isna,
    concat
    )

if __name__=="__main__":
    from log import log
    from functions import (
        pullValues,
        getFunctionToFuncFormatter,
        intervaloPerfeito,
        intervaloPerfeitoData,
        isEvery,
        reduzir_a_um,
        timeToTimedelta,
        somar_data_e_hora
        )
else:
    from .log import log
    from .functions import (
        pullValues,
        getFunctionToFuncFormatter,
        intervaloPerfeito,
        intervaloPerfeitoData,
        isEvery,
        reduzir_a_um,
        timeToTimedelta,
        somar_data_e_hora
        )

plt.rcParams["legend.fontsize"] = 11
plt.rcParams['figure.constrained_layout.use'] = True

class Serie():
    
    def __init__(self,X,Y,type="plot",label=None,color=None,toSecundary=False,showLegend=True,setup=dict()) -> None:
        self.data:DataFrame = concat([X,Y],axis=1)
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
    
    def getYLim(self,interval:list|tuple):
        dataFiltered = self.data.copy()
        dataFiltered = dataFiltered[dataFiltered[self.nameX]>=min(interval)]
        dataFiltered = dataFiltered[dataFiltered[self.nameX]>=max(interval)]
        return (min(dataFiltered[self.nameY]),max(dataFiltered[self.nameY]))
    
    def verificarLeituras(self,ymin,ymax):
        minimo = min(self.data[self.nameY])
        maximo = max(self.data[self.nameY])
        retorno = True
        if minimo<ymin:
            log.info(f"Medição {minimo} < limite {ymin}")
            retorno = False
        if maximo>ymax:
            log.info(f"Medição {maximo} > limite {ymax}")
            retorno = False
        return retorno
    
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
        return f"Serie (label={self.label},showLegend={self.showLegend},color={self.color})\n{str(self.data)}"
        
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
            y2MinorLocator = AutoMinorLocator(5),
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
            legendFonteSize = 10,
            legendLoc='upper center',
            legendBbox_to_anchor = (0.5,-0.25),
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
                log.warning("User Warning: setup['rectFigureBaseAdd_axes'] não foi usado pois self.setup['figureAutoLayout']==True. Aconselha-se alterar o setup['figureAutoLayout'] para False.")
        
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
            if serie == None:
                continue
            xValores.extend(serie.xLim)
            if serie.toSecundary:
                y2Valores.extend(serie.yLim)
            else:
                yValores.extend(serie.yLim)
        if self.setup["xlim"]==(None,None):
            if isEvery(xValores,Timestamp):
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
        self.series = series
    def append_series(self,newSeries:Serie):
        self.series.append(newSeries)
    def extend_series(self,newSeries:list[Serie]):
        self.series.extend(newSeries)

    def update_setup(self,setup:dict):
        self.setup.update(setup)

    def set_title(self,title:str):
        self.title = title

    def save (self,path:str,dpi=500,bbox_inches='tight',showLog=False):
        log.info(f"Salvando imagem: {path}") if showLog else 0
        self.fig.savefig(path,dpi=dpi,bbox_inches=bbox_inches)
        log.info(f"Imagem salva: {path}") if showLog else 0
    
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

EMPTY_SERIE_SECO = Serie(DataFrame([],columns=["Data"]),DataFrame([],columns=["Valor"]),label="Leituras Secas",color="black",showLegend=True,setup=dict(marker="x",linestyle=""))





""" Modelo de cadastro e leituras do GEOTEC """

class Instrumento():
    def __init__(self,
                 dict_cadastro:dict
                 ) -> None:
        self.dict_cadastro = dict_cadastro
        self.ID = reduzir_a_um([dict_cadastro['index']])
        self.complexo = reduzir_a_um([dict_cadastro['Complexo Mineiro']])
        self.mina = reduzir_a_um([dict_cadastro['Mina']])
        self.tipo_estrutura = reduzir_a_um([dict_cadastro['Tipo de Estrutura']])
        self.estrutura = reduzir_a_um([dict_cadastro['Estrutura Geotécnica']])
        self.sistema_coordenadas = reduzir_a_um([dict_cadastro['Sistema de Coordenadas']])
        self.fuso = reduzir_a_um([dict_cadastro['Fuso']])
        self.coordenadas = reduzir_a_um([(dict_cadastro['longitude (UTM)'], dict_cadastro['Latitude (UTM)'], dict_cadastro['Elevação'])])
        self.tipo = reduzir_a_um([dict_cadastro['Tipo de Instrumento']])
        self.sub_tipo = reduzir_a_um([dict_cadastro['Subtipo de Instrumento']])
        self.codigo = reduzir_a_um([dict_cadastro['Código']])
        self.descricao = reduzir_a_um([dict_cadastro['Descrição']])
        self.obs = reduzir_a_um([dict_cadastro['Observação']])
        self.data_instalacao = reduzir_a_um([dict_cadastro['Data de instalação']])
        self.local = reduzir_a_um([dict_cadastro['Local Instalação']])
        self.condicao = reduzir_a_um([dict_cadastro['Condicao de Instrumento']])
        self.fundo_ou_base = reduzir_a_um([dict_cadastro['Cota do Fundo (m)'], dict_cadastro['Cota da Base (m)']])
        if isna(dict_cadastro['Cota da Base (m)']):
            self.label_cota_inferior = "fundo"
        else:
            self.label_cota_inferior = "base"
        self.topo = reduzir_a_um([dict_cadastro['Cota do Topo (m)']])
        self.angulo = reduzir_a_um([dict_cadastro['Ângulo de Instalação (°)']])
        self.prof = reduzir_a_um([dict_cadastro['Profundidade (m)']])
        self.topo_celula = reduzir_a_um([dict_cadastro['Cota de Topo da Célula (m)']])
        self.base_celula = reduzir_a_um([dict_cadastro['Cota da Base da Célula (m)']])
        self.diametro = reduzir_a_um([dict(padrao = dict_cadastro['Diâmetro do Tubo'], pol=dict_cadastro['Diâmetro do Tubo (\')'], mm=dict_cadastro['Diâmetro do Tubo (mm)'])])
        self.atencao = reduzir_a_um([dict_cadastro['Nível de Atenção (Maior que)'], dict_cadastro['Nível de Atenção no vetor deslocamento (Maior que)']])
        self.alerta = reduzir_a_um([dict_cadastro['Nível de Alerta (Maior que)'], dict_cadastro['Nível de Alerta no vetor de deslocamento (Maior que)']])
        self.emergencia = reduzir_a_um([dict_cadastro['Nível de Emergência (Maior que)'], dict_cadastro['Nível de Emergência no vetor de deslocamento (Maior que)']])
        self.crista_barragem = reduzir_a_um([dict_cadastro['Cota da crista da barragem (m)']])
        self.soleira_vertedor = reduzir_a_um([dict_cadastro['Cota da soleira do vertedor (m)']])
        self.porcentagem_seco:float = 0.0
        
        pass

    def set_leituras(self,df:DataFrame):
        self.df_leituras = df.copy()
        df_mod = df.copy()

        df_vazio = DataFrame([],columns=df_mod.columns)
        
        self.leituras_nao_realizada = df_vazio.copy()
        self.leituras_outliers = df_vazio.copy()
        self.leituras_nulas = df_vazio.copy()
        self.leituras_secas = df_vazio.copy()
        self.leituras_jorrantes = df_vazio.copy()
        self.leituras_nao_secas = df_vazio.copy()
        self.leituras_validas = df_vazio.copy()
        self.n_secos = df_vazio.copy()
        self.n_leituras_validas = df_vazio.copy()
        self.leituras_acima_nv_controle = df_vazio.copy()
        self.leituras_acima_nv_controle = df_vazio.copy()
        self.leituras_acima_nv_controle = df_vazio.copy()
        self.leituras_acima_topo = df_vazio.copy()
        self.leituras_abaixo_base = df_vazio.copy()
        self.registro_unico_diario = True
        self.possui_leituras = True
        
        if df_mod.shape[0]==0:
            self.possui_leituras = False
            self.registro_unico_diario = False
            log.info(f"{self.codigo} sem leituras em seu Leitura.df_leituras")
            return
        elif df_mod["Data de Medição"].value_counts().max()>1:
            log.warning(f"{self.codigo} registrou mais de uma leitura no mesmo dia")
            self.registro_unico_diario = False

        hora_em_time = df_mod.apply(lambda row: timeToTimedelta(row['Hora da Medição']), axis=1)
        try:
            df_mod["Hora da Medição"] = hora_em_time
            df_mod["Data/Hora"] = df_mod["Data de Medição"] + df_mod["Hora da Medição"]
        except ValueError as m:
            log.info(f"{self.codigo} sem leituras")
        except Exception as m:
            try:
                log.critical(f"Função somar_data_e_hora foi usada no {self.codigo}")
                df_mod["Data/Hora"] = somar_data_e_hora(df_mod["Data de Medição"], df_mod["Hora da Medição"])
                raise Exception()
            except Exception as m:
                if "###" in str(m):
                    log.critical(self.codigo)
                    log.critical(df_mod.to_string())
                    raise Exception()
        # Ordenando o dataframe conforme a DATA e HORA da medição
        df_mod = df_mod.sort_values("Data/Hora")
        
        self.leituras_nao_realizada = df_mod[df_mod["Situação da Medição"]=="Não Realizada"]
        self.leituras_outliers = df_mod[df_mod["Outlier"]=="SIM"]
        self.leituras_negativas = df_mod[df_mod["Valor"]<0]
        
        df_mod = df_mod[df_mod["Valor"]>=0]
        df_mod = df_mod[df_mod["Situação da Medição"]=="Realizada"]
        df_mod = df_mod[isna(df_mod["Outlier"])]
        self.leituras_nulas = df_mod[isna(df_mod["Valor"])]
        
        valores_secos_jorrantes = Series(df_mod[~isna(df_mod["Condição Adversa"])]["Valor"])
        if not (len(valores_secos_jorrantes)==0): # Há leituras secas e jorrantes
            valores_secos_jorrantes = valores_secos_jorrantes.dropna()
            if len(valores_secos_jorrantes.to_list())>0:
                raise Exception(f"Valores escritos em leituras secas/jorrantes no instrumento {self.codigo}:\n{isna(valores_secos_jorrantes[0])}")
            df_mod.loc[df_mod["Condição Adversa"]=="SECO", "Valor"] = self.fundo_ou_base
            df_mod.loc[df_mod["Condição Adversa"]=="JORRANTE","Valor"] = self.topo

        # Excluindo leituras sem valor depois do filtro de Outliers, Leituras Realizadas e Preenchimento dos SECOS e JORRANTES
        df_mod = df_mod[~isna(df_mod["Valor"])]
        
        # Separando as leituras em atributos de acordo com a Condição Adversa
        self.leituras_secas = df_mod[df_mod["Condição Adversa"]=="SECO"]
        self.leituras_jorrantes = df_mod[df_mod["Condição Adversa"]=="JORRANTE"]
        self.leituras_nao_secas = df_mod[isna(df_mod["Condição Adversa"])]
        
        if (self.fundo_ou_base,self.topo)==(None,)*2:
            log.warning(f"Instrumento {self.codigo} sem cadastro de topo e base/fundo.")
        else:
            if self.topo != None:
                self.leituras_acima_topo = df_mod[df_mod["Valor"]>self.topo]
                df_mod = df_mod[df_mod["Valor"]<=self.topo]
                log.warning(f"Instrumento {self.codigo} possui {len(self.leituras_acima_topo)} acima da cota de topo.")
            else:
                log.warning(f"Instrumento {self.codigo} sem cadastro de topo.")
                
            if self.fundo_ou_base != None:
                self.leituras_abaixo_base = df_mod[df_mod["Valor"]<self.fundo_ou_base]
                df_mod = df_mod[df_mod["Valor"]>=self.fundo_ou_base]
                log.warning(f"Instrumento {self.codigo} possui {len(self.leituras_abaixo_base)} abaixo da cota de base/fundo.")
            else:
                log.warning(f"Instrumento {self.codigo} sem cadastro de base/fundo.")
                

        self.leituras_validas = df_mod.copy()
        self.n_secos = len(self.leituras_secas)
        self.n_leituras_validas = len(self.leituras_validas)
        try:
            self.porcentagem_seco = self.n_secos/float(self.n_leituras_validas)
        except ZeroDivisionError:
            log.warning(f"{self.codigo} não possui leituras.")
            self.possui_leituras = False
        
        if (self.atencao,self.alerta,self.emergencia)==(None,)*3:
            log.warning(f"Instrumento {self.codigo} sem cadastro de níveis de controle.")
        elif self.atencao != None:
            self.leituras_acima_nv_controle = df_mod[df_mod["Valor"]>=self.atencao]
        elif self.alerta != None:
            self.leituras_acima_nv_controle = df_mod[df_mod["Valor"]>=self.atencao]
        elif self.emergencia != None:
            self.leituras_acima_nv_controle = df_mod[df_mod["Valor"]>=self.emergencia]
        
        self.data_maxima = self.leituras_validas["Data de Medição"].max()
        self.data_minima = self.leituras_validas["Data de Medição"].min()
        self.data_hora_maxima = self.leituras_validas["Data/Hora"].max()
        self.data_hora_minima = self.leituras_validas["Data/Hora"].min()
        self.valor_maximo = self.leituras_validas["Valor"].max()
        self.valor_minimo = self.leituras_validas["Valor"].min()
        self.periodo_leituras = self.data_hora_maxima - self.data_hora_minima
        
        return

    def __str__(self):
        return f"""{self.codigo}: {self.tipo} de {self.estrutura} - {self.coordenadas}"""
    __repr__ = __str__
    
    def descrever(self,file_path:str=""):
        relatorio = f"{self.tipo} {self.codigo} - {self.tipo_estrutura} {self.estrutura}\n\n"
        log.info(f"Gerando relatório do instrumento {self.codigo}")
        relatorio += f"""LEITURAS OUTLIERS:\n{self.leituras_outliers[["Data de Medição","Hora da Medição","Valor","Unidade de Medida"]].to_string()}\n\n"""            
        relatorio += f"""LEITURAS ACIMA DE NÍVEL DE CONTROLE:\n{self.leituras_acima_nv_controle[["Data de Medição","Hora da Medição","Valor","Unidade de Medida"]].to_string()}\n\n"""
        relatorio += f"""LEITURAS ABAIXO DA COTA DE FUNDO/BASE:\n{self.leituras_abaixo_base[["Data de Medição","Hora da Medição","Valor","Unidade de Medida"]].to_string()}\n\n"""
        relatorio += f"""LEITURAS ACIMA DA COTA DE TOPO:\n{self.leituras_acima_topo[["Data de Medição","Hora da Medição","Valor","Unidade de Medida"]].to_string()}\n\n"""
        relatorio += f"""LEITURAS NÃO REALIZADAS:\n{self.leituras_nao_realizada[["Data de Medição","Hora da Medição","Justificativa de não Medição","Observação"]].to_string()}\n\n"""
        relatorio += f"""LEITURAS NULAS:\n{self.leituras_nulas[["Data de Medição","Hora da Medição","Justificativa de não Medição","Observação"]].to_string()}\n\n"""
        relatorio += f"""LEITURAS NEGATIVAS:\n{self.leituras_negativas[["Data de Medição","Hora da Medição","Valor","Justificativa de não Medição","Observação"]].to_string()}\n\n"""
        relatorio+="---------------\n"
        if file_path:
            with open(file=file_path,mode="a") as file:
                file.write(relatorio)
                log.info(f"Salvando relatório do instrumento {self.codigo} no caminho {file_path}")
        return relatorio