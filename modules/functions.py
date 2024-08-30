import pandas as pd
import os
from matplotlib.figure import Figure
from matplotlib.legend import Legend

# Comando para ignorar os UserWarning dados pelo Pyhton
import warnings
warnings.filterwarnings('ignore')

# Nome das colunas do cadastro
colunaCodigoCadastro = "Código"
colunaCotaFundo = "Cota do Fundo (m)"
colunaCotaTopo = "Cota do Topo (m)"
colunaAtencao = "Nível de Atenção (Maior que)"
colunaAlerta = "Nível de Alerta (Maior que)"
colunaEmergencia = "Nível de Emergência (Maior que)"
colunaEstrutura = "Estrutura Geotécnica"
colunaTipo = "Tipo de Instrumento"

# Nome das colunas da medição
columnData = "Data de Medição"
columnIndex = columnData
colunaCodigo = "Código do Instrumento"
colunaSituacaoMedicao = "Situação da Medição"
colunaOutlier = "Outlier"
columnValues = "Valor Final"
columnColumns = "Código do Instrumento"
columnGrandeza = "Grandeza física"
columnUnidade = "Unidade de Medida"

instrumentoToEixo = {
    "Régua de Reservatório": "Elevação (m)",
    "Medidor de Nível de Água": "Elevação (m)",
    "Piezômetro": "Elevação (m)",
    
    "Medidor de Vazão": "Vazão (L/s)",
    
    "Marco Topográfico": "Vetor Deslocamento (m)",
    "Radar Orbital": "Vetor Deslocamento (m)",
    "Estação Topográfica": "Vetor Deslocamento (m)",
    "Radar": "Vetor Deslocamento (m)",
    
    "Pluviômetro": "Pluviometria (mm)",
    "Pluviógrafo": "Precipitação (mm)",
    
    "Câmera": "",
    "Poço": "",
    }

def getWindowsLegend(legend:Legend,fig:Figure):
    # Obtendo a posição e o tamanho da legenda
    bbox = legend.get_window_extent()

    # Convertendo as coordenadas de janela para coordenadas da figura
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())

    # Imprimindo a posição e o tamanho
    print(f'Posição (x0, y0): ({bbox.x0}, {bbox.y0})')
    print(f'Tamanho (largura, altura): ({bbox.width}, {bbox.height})')
    return bbox
def getFunctionToFuncFormatter(nCasasDecimais,sepDecimal=",",sepMilhar=""):
    """Função para construir uma função de formatação de float com separador de milhar e decimal customizado para a classe FuncFormatter."""
    def functionToReturn(x,pos):
        x = round(float(x),nCasasDecimais)
        xStr = f"{x:,}".replace(",","#")
        toReturn = xStr.replace(".","$")
        toReturn = toReturn.replace('$', sepDecimal).replace("#",sepMilhar)
        return toReturn+"0"*max(nCasasDecimais-len(toReturn.split(sepDecimal)[-1]),0)
    return functionToReturn

def pullValues(dict:dict,keys:list):
    dictToReturn = {}
    for key,value in dict.items():
        if key in keys:
            dictToReturn.update({key:value})
    return dictToReturn
        

def criarDiretorio (relativePath:str) -> None:
    if not os.path.exists(relativePath):
        os.mkdir(relativePath)
    return

def readSheets (file,sheetNames=[]):
    print(f"Abrindo o arquivo {file}")
    print(f"Esse processo pode demorar 1 ou 2 minutos...")
    if len(sheetNames)==0:
        print(f"Lendo as planilhas do arquivo {file}")
        dataFrames = pd.read_excel(file,sheet_name=None)
    else:
        print(f"Lendo as planilhas {sheetNames} do arquivo {file}")
        dataFrames = {sheetName:pd.read_excel(file,sheetName) for sheetName in sheetNames}
    print("O arquivo foi importado com sucesso.")
    return dataFrames


dataFimDefault = pd.Timestamp('2024-07-01')

def analisarLeiturasTipoInstrumento(tipoinstrumento, leituras, listColumns:list = [columnGrandeza,columnUnidade,colunaCodigo,"Estrutura"]):
    return pd.concat([leituras[leituras[colunaTipo] == tipoinstrumento]])[listColumns].drop_duplicates().dropna()

def get_info_instrument(nameInstrument,df,nameInfo=colunaCodigoCadastro):
    # df : DataFrame do cadastro GEOTEC
    return df[df[colunaCodigoCadastro]==nameInstrument][nameInfo].values[0]

def tratarDados(nomeInstrumento:str,df:pd.DataFrame,dataInicio:pd.Timestamp|None=None,dataFim:pd.Timestamp|None=None,seco:bool=False):
    leiturasFiltradas = df.copy(deep=True)
    leiturasFiltradas = leiturasFiltradas[leiturasFiltradas[colunaCodigo]==nomeInstrumento][leiturasFiltradas[colunaSituacaoMedicao]=="Realizada"][leiturasFiltradas[colunaOutlier]!="Sim"]
    if seco:
        leiturasFiltradas = leiturasFiltradas[leiturasFiltradas["Condição Adversa"]=="SECO"]
    leiturasFiltradas = leiturasFiltradas[leiturasFiltradas["Condição Adversa"]!="JORRANTE"]
    pivotLeiturasFiltradas = leiturasFiltradas.pivot_table(values=columnValues,
                                                           index=columnIndex,
                                                           columns=columnColumns,
                                                           dropna=True,
                                                           aggfunc=max
                                                           )
    if dataInicio!=None:
        pivotLeiturasFiltradas = pivotLeiturasFiltradas.loc[dataInicio:]
    if dataFim!=None:
        pivotLeiturasFiltradas = pivotLeiturasFiltradas.loc[:dataFim]
    if seco:
        try:
            pivotLeiturasFiltradas.rename(columns={nomeInstrumento:f"{nomeInstrumento} (seco)"},inplace=True)
        except Exception:
            return pivotLeiturasFiltradas
    return pivotLeiturasFiltradas

def definirLimites(nomeInstrumento:str, df:pd.DataFrame):
    serie = tratarDados(nomeInstrumento=nomeInstrumento,df=df).dropna()
    if len(serie)!=0:
        return pd.DataFrame(dict(
            data=dict(
                min=serie.sort_index().index[0],
                max=serie.sort_index().index[-1]
            ),
            leitura=dict(
                min=serie.sort_values(by=nomeInstrumento).values[0][0],
                max=serie.sort_values(by=nomeInstrumento).values[-1][0]
            )
        ))
    else:
        return pd.DataFrame(dict(
            data=dict(
                min=pd.Timestamp(0),
                max=pd.Timestamp(0)
            ),
            leitura=dict(
                min=0,
                max=0
            )
        ))

def listarInstrumentos(estrutura="",tipoInstrumento="",df:pd.DataFrame=pd.DataFrame()):
    if estrutura!="":
        df = df[df[colunaEstrutura]==estrutura]
    if tipoInstrumento!="":
        df = df[df[colunaTipo]==tipoInstrumento]
    return list(df["Código"].values)

def exibirLimites(estrutura,tipoInstrumento):
    pzs = listarInstrumentos(estrutura=estrutura,tipoInstrumento=tipoInstrumento)
    for pz in pzs:
        print(pz)
        print(definirLimites(pz))
        print()

def gerarHistorico(nomeInstrumento,
                   nomeInstrumentoPluv="AGLPL001",
                   dataFim=dataFimDefault,
                   temNVControle=True,
                   temCotaFundo=True,
                   temCotaTopo=True,
                   temPLV=True
                   ):
    print(1)
    pluv = tratarDados(nomeInstrumentoPluv)
    inst = tratarDados(nomeInstrumento)
    seco = tratarDados(nomeInstrumento,seco=True)
    historico = pd.concat([pluv,
                           inst,
                           seco],join="outer",axis=1)
    seriesExtras = [
        [temNVControle,"atenção",colunaAtencao],
        [temNVControle,"alerta",colunaAlerta],
        [temNVControle,"emergência",colunaEmergencia],
        [temCotaFundo,"cota de fundo",colunaCotaTopo],
        [temCotaTopo,"cota de topo",colunaCotaFundo]
    ]
    for boolean,string,column in seriesExtras:
        if boolean:
            historico.loc[:,f"{nomeInstrumento} ({string})"] = get_info_instrument(nomeInstrumento,column)
    return historico

def intervaloPerfeitoData(nomeInstrumento):
    
    min = definirLimites(nomeInstrumento)["data"]["min"]
    if min.month<=6:
        minCorrigido = pd.Timestamp(day=1,month=1,year=min.year)
    elif min.month==7 and min.day==1:
        minCorrigido = min        
    else:
        minCorrigido = pd.Timestamp(day=1,month=7,year=min.year)
    
    max = definirLimites(nomeInstrumento)["data"]["max"]
    if max.month<=6:
        maxCorrigido = pd.Timestamp(day=1,month=7,year=max.year)
    elif max.month==7 and max.day==1:
        maxCorrigido = max
    else:
        maxCorrigido = pd.Timestamp(day=1,month=1,year=max.year+1)
    
    return minCorrigido,maxCorrigido

def intervaloPerfeito(nomeInstrumento,dV:float|int|None=None,superior=True,min=None,max=None):
    if min==None or max==None:
        min = definirLimites(nomeInstrumento)["leitura"]["min"]
        max = definirLimites(nomeInstrumento)["leitura"]["max"]
    
    if max<min:
        raise Exception("Valor max menor do que valor min.")
    if dV==None:
        dVDefault = [
            0.01,
            0.02,
            0.05,
            0.1,
            0.2,
            0.5,
            1,
            2,
            5,
            10,
            20,
            50]
        L = abs(max-min)
        for dVi in sorted(dVDefault):
            if 0<L/dVi<=10:
                dV = dVi
                break
            else:
                dV=1
    if superior:
        minPerf, maxPerf = (min//dV)*dV-dV,(max//dV)*dV+dV
        if minPerf<0:
            minPerf=0
        return minPerf, maxPerf, dV
    else:
        raise Exception("Ainda não foi implementado o superior=False")

def avaliarTrecho (nomeInstrumento,y0=0,yi=10**10,percentiles=[.25,.5,.75]):
    serie:pd.date_range = tratarDados(nomeInstrumento)
    serie = serie[(y0<=serie[nomeInstrumento]) & (serie[nomeInstrumento]<=yi)]
    return serie.describe(percentiles=percentiles)
