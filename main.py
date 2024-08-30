from modules import *
import pandas as pd

if __name__=="__main__":
    df = readSheets("Leituras-Monjolo.xlsx")["Planilha1"]
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
    
    #Inicializando, renderizando e salvando o gráfico
    graph = Grafico(series=series)
    graph.render()
    # series = [manuais,automaticas]
    # graph.set_series(series)
    # graph.render()
    graph.save(path="1.png")