from modules import *
import pandas as pd
df = readSheets("Leituras-Monjolo.xlsx")["Planilha1"]
df.columns
data = df["Rótulos de Linha"]

pluv = df["AGLPL001"]
leiturasAutomatizadas = df["AGLBRMRR002_A"]
leiturasManuais = df["AGLBRMRR002"]
pluviometria = Serie(data,pluv,"bar","Pluviometria","blue",True)
manuais = Serie(data,leiturasManuais,"plot","RR002","red",True)
automaticas = Serie(data,leiturasAutomatizadas,"plot","RR002_A","red",True,False)
series = [pluviometria,manuais,automaticas]
Grafico(series=series).save("1.png")