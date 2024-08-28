import pandas as pd
import matplotlib.pyplot as plt

class Grafico():
    def __init__(self,nome="graph",width=12,height=6) -> None:
        self.nome = str(nome)
        self.figure, self.axes = plt.subplots(figsize=(width, height))
        self.figure.tight_layout()
        self.series:list[Serie] = []
        pass
    def addSeries(self,series:list=[]):
        if isinstance(series,list):
            if len(series)>0:
                self.series.extend(series)
            else:
                raise Exception("Parâmetros series do método Grafico.addSeries está vazio.")
        else:
            raise Exception("Parâmetros series do método Grafico.addSeries não é do tipo list.")
    def plotar(self):
        for serie in self.series:
            # Implementar color no plot
            # implementar marker no plot
            # implementar tipo de linha no plot

            if serie.tipo == "line":
                self.axes.plot(serie.x,serie.y,label=serie.nome)
            elif serie.tipo == "bar":
                self.axes.bar(x=serie.x,height=serie.y,label=self.nome)
            elif serie.tipo == "scatter":
                self.axes.scatter(x=serie.x,y=serie.y,label=self.nome)


    def salvar(self,nomeArquivo="",format="png",transparent=False):
        if nomeArquivo=="":
            nomeArquivo = self.nome+"."+format
        else:
            nomeArquivo = nomeArquivo+"."+format
        self.axes.legend(
            # loc='upper center',
            bbox_to_anchor=(0.5, -0.25),
            fancybox=True,
            shadow=False,
            ncol=5)
        plt.subplots_adjust(bottom=0.2)
        self.figure.savefig(fname=nomeArquivo,transparent=transparent,format=format)


class Serie():
    def __init__(self,nome,df,xNome,yNome,tipo="line",mostrarNaLegenda:bool=True,ID:str="") -> None:
        if ID=="":
            self.ID = nome
        else:
            self.ID = ID
        self.nome = nome
        self.x = df[xNome]
        self.y = df[yNome]
        self.maximos = dict(
            xMax = max(self.x),
            xMin = min(self.x),
            yMax = max(self.y),
            yMin = min(self.y)
        )
        self.data = pd.DataFrame({
            xNome:self.x,
            yNome:self.y
            })
        self.tipo = tipo
        self.mostrarNaLegenda = mostrarNaLegenda

if __name__=="__main__":
    df = pd.DataFrame(
        dict(
            x=[1,2,3,4],
            y=[1,3,6,3]
        )
    )
    serie1 = Serie("pico",df,"x","y","line",True)
    serie2 = Serie("pico",df,"x","y","bar",True)
    serie3 = Serie("pico",df,"x","y","scatter",True)
    graf1 = Grafico(1)
    graf1.addSeries([serie1,serie2,serie3])
    graf1.plotar()
    graf1.salvar()
    print(graf1.axes.get_legend_handles_labels())