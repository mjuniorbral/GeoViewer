from modules import *
import pandas as pd

def fromDataToSerie(nomeInstrumento,df,seco=False,type="plot",label=None,color=None,toSecundary=False,showLegend=True,setup=dict()):
    dados = tratarDados(nomeInstrumento,df,seco=seco)
    dados = dados.reset_index()
    if seco:
        nomeInstrumento+=" (seco)"
    # print(dados)
    X = dados.loc[:,columnData]
    if len(X)==0:
        print(f"Não há leituras para {nomeInstrumento}")
        return
    Y = dados.loc[:,nomeInstrumento]
    return Serie(X,Y,type,label,color,toSecundary,showLegend,setup)

if __name__=="__main__":
    df = readSheets("data/Leituras-Monjolo.xlsx",showLog=False)["Planilha1"]
    data = df["Rótulos de Linha"]
    pluv = df["AGLPL001"]
    leiturasAutomatizadas = df["AGLBRMRR002_A"]
    leiturasManuais = df["AGLBRMRR002"]
    
    # Construindo séries do eixo principal
    toSecundary=False
    manuais = Serie(data,leiturasManuais,"plot","RR002",toSecundary=toSecundary)
    automaticas = Serie(data,leiturasAutomatizadas,"plot","RR002_A",setup=dict(linestyle="--",marker="x"),toSecundary=toSecundary)
    
    # Construindo séries do eixo secundário
    toSecundary = True
    pluviometria = Serie(data,pluv,"bar","Pluviometria","blue",toSecundary=toSecundary)
    
    #Construindo ordem de plotagem
    series = [manuais,automaticas,pluviometria]
    # series = [manuais,automaticas]
    
    #Inicializando, renderizando e salvando o gráfico
    # Definindo período de interesse (2,5 anos hidrológicos no mínimo)
    setup=dict(xlim=(pd.Timestamp(day=1,month=4,year=2022),pd.Timestamp(day=1,month=9,year=2024)))
    graph = Graphic(
        series=series,
        setup=setup,
        )
    graph.render(toFilter=False)
    # series = [manuais,automaticas]
    # graph.set_series(series)
    # graph.render()
    graph.save(path="images/nivelGrafico/RR002.png",showLog=True)