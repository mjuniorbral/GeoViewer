import pandas as pd
import os
from matplotlib.figure import Figure
from matplotlib.artist import Artist
from datetime import datetime,time
if __name__ == "__main__":
    from log import log
else:
    from .log import log

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

def dropNone(iterable):
    retorno = []
    for i in iterable:
        if i==None:
            continue
        if pd.isna(i):
            continue
        if pd.isnull(i):
            continue
        retorno.append(i)
    return retorno

def minimoValido (iterable):
    iterable = dropNone(iterable)
    if len(iterable)==0:
        return
    else:
        return min(iterable)

def maximoValido (iterable):
    iterable = dropNone(iterable)
    if len(iterable)==0:
        return
    else:
        return max(iterable)
    
    

def importFromGEOTECModel(file,registrationsSheet,measuresSheet):
    df_global = readSheets(file=file,sheetNames=[registrationsSheet,measuresSheet])
    cadastro = df_global[registrationsSheet].copy(deep=True)
    leituras = df_global[measuresSheet].copy(deep=True)
    columnsRegistrations = list(cadastro.columns)
    columnsMeasures = list(leituras.columns)
    return cadastro, leituras, columnsRegistrations, columnsMeasures

def isEvery(iterable,type_):
    for item in iterable:
        if not isinstance(item,type_):
            log.critical(f"Valor {item} não é o type {type_}, mas sim do tipo {type(item)}")
            return False
    return True

def intervaloPerfeito(valores,
                      nDiv=5,
                      dVDefault=(0.01, 0.02, 0.025, 0.05, 0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100)):
    """Substitui a função intervaloPerfeito_old2 anterior"""
    valores = tuple(dropNone(valores))
    log.debug(valores) #############################################################
    if len(valores)==0:
        return (None,None)
    min_ = min(valores)
    max_ = max(valores)
    log.debug(min_,max_) #############################################################
    L = float(abs(max_-min_))
    log.debug(L) #############################################################
    dVDefault = sorted(dVDefault,reverse=True)
    for dVi in dVDefault:
        log.debug(f"{L}/{dVi}={L/dVi}")
        if L/dVi>nDiv:
            dV_=dVi
            break
    else:
        log.critical(f"\n\n\nLOOP FOR foi iterado completamente e não achou a divisão igual a nDiv\n{L=} / {max_=} / {min_=} / {valores=}\n\n\n")
        dV_ = min(dVDefault)
    log.debug(dV_) #############################################################
    correcao = 1
    if min_%dV_==0:
        correcao = 0
    minPerf = ((min_//dV_)-correcao)*dV_
    correcao = 1
    if max_%dV_==0:
        correcao = 0
    maxPerf = ((max_//dV_)+correcao)*dV_
    log.debug((minPerf, maxPerf), dV_)
    return (minPerf, maxPerf), dV_

def monthByInterval(n):
    if 12%n!=0:
        return (False,(),n)
    tupla = ()
    cont = 1
    while cont<13:
        tupla+=(cont,)
        cont+=n
    return (True,tupla,n)

def intervaloPerfeitoDataMes(datas:list[pd.Timestamp],dV:int|None=None,superior=True,min_=None,max_=None):
    datas = tuple(dropNone(datas))
    if not isEvery(datas,pd.Timestamp):
        raise Exception("Nem todos os elementos da variável data é pd.Timestamp")
    if len(datas)==0:
        return (None,None)
    data_min = min(datas)
    data_max = max(datas)
    minCorrigido = pd.Timestamp(day=1,month=int(data_min.month),year=int(data_min.year))
    maxCorrigido = data_max+pd.Timedelta(days=32)
    maxCorrigido = pd.Timestamp(day=1,month=int(maxCorrigido.month),year=int(maxCorrigido.year))
    if dV==None:
        return (minCorrigido,maxCorrigido)
    
    dV = int(dV)
    monthByIntervalValor = monthByInterval(dV)
    if monthByIntervalValor[0]:
        min_month = minCorrigido.month
        while not(min_month in monthByIntervalValor[1]):
            min_month-=1
        minCorrigido = pd.Timestamp(day=1, month=min_month, year=minCorrigido.year)
        return (minCorrigido,maxCorrigido)
    else:
        return (minCorrigido,maxCorrigido)
    
def intervaloPerfeitoData(datas:list[pd.Timestamp],dV:int|None=None,superior=True,min_=None,max_=None):
    datas = tuple(dropNone(datas))
    if len(datas)==0:
        return (None,None)
    if dV!=None:
        raise Exception("Ainda não foi implementado o dV!=None")
    if superior==False:
        raise Exception("Ainda não foi implementado o superior=False")
    
    if min_==None:
        min_:pd.Timestamp = min(datas)
    if min_.month<=6:
        minCorrigido = pd.Timestamp(day=1,month=1,year=min_.year)
    elif min_.month==7 and min_.day==1:
        minCorrigido = min_        
    else:
        minCorrigido = pd.Timestamp(day=1,month=7,year=min_.year)
    
    if max_==None:
        max_:pd.Timestamp = max(datas)
    if max_.month<=6:
        maxCorrigido = pd.Timestamp(day=1,month=7,year=max_.year)
    elif max_.month==7 and max_.day==1:
        maxCorrigido = max_
    else:
        maxCorrigido = pd.Timestamp(day=1,month=1,year=max_.year+1)
    
    return (minCorrigido,maxCorrigido)

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
        
def getWindowsArtist(artist:Artist,fig:Figure,print_=False):
    # Obtendo a posição e o tamanho do artist
    bbox = artist.get_window_extent()
    
    # Convertendo as coordenadas de janela para coordenadas da figura
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())

    if print_:
        # Imprimindo a posição e o tamanho
        log.debug(f'Posição (x0, y0): ({bbox.x0}, {bbox.y0})')
        log.debug(f'Tamanho (largura, altura): ({bbox.width}, {bbox.height})')
    return bbox

def criarDiretorio (relativePath:str) -> None:
    if not os.path.exists(relativePath):
        os.mkdir(relativePath)
    return

def readSheets (file,sheetNames=[],showLog=True):
    log.debug(f"Abrindo o arquivo {file}") if showLog else None
    log.debug(f"Esse processo pode demorar 1 ou 2 minutos...")  if showLog else None
    if len(sheetNames)==0:
        log.debug(f"Lendo as planilhas do arquivo {file}") if showLog else None
        dataFrames = pd.read_excel(file,sheet_name=None)
    else:
        log.debug(f"Lendo as planilhas {sheetNames} do arquivo {file}")  if showLog else None
        dataFrames = {}
        for sheetName in sheetNames:
            log.debug(f"Iniciando leitura {sheetName}")
            dataFrames[sheetName] = pd.read_excel(file,sheetName)
            log.debug(f"Leitura finalizada {sheetName}")
    log.debug("O arquivo foi importado com sucesso.")  if showLog else None
    return dataFrames


def get_info_instrument(nameInstrument,df,nameInfo=colunaCodigoCadastro):
    # df : DataFrame do cadastro GEOTEC
    return df[df[colunaCodigoCadastro]==nameInstrument][nameInfo].values[0]

def tratarDados(nomeInstrumento:str,df:pd.DataFrame,dataInicio:pd.Timestamp|None=None,dataFim:pd.Timestamp|None=None,seco:bool=False):
    if not isinstance(df,pd.DataFrame):
        log.debug(df)
        raise AttributeError()
    leiturasFiltradas = df.copy(deep=True)
    # log.debug(leiturasFiltradas)
    if colunaCodigo not in leiturasFiltradas.columns:
        log.debug("Não está nas colunas")
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
        log.debug(pz)
        log.debug(definirLimites(pz))
        log.debug()

month = datetime.today().month
year = datetime.today().year
dataFimDefault = pd.Timestamp(day=1,month=month,year=year)

def gerarHistorico(nomeInstrumento,
                   nomeInstrumentoPluv="AGLPL001",
                   dataFim=dataFimDefault,
                   temNVControle=True,
                   temCotaFundo=True,
                   temCotaTopo=True,
                   temPLV=True
                   ):
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

def separador(path_csv,sep=","):
    out_lines = []
    try:
        with open(path_csv) as arquivo:
            for line in arquivo.readlines():
                if line[0]=="-":
                    newLine = []
                    cont = 0
                    for c in line:
                        if c == sep:
                            cont+=1
                            if cont%2==0:
                                newLine.append(";")
                            else:
                                newLine.append(c)
                            continue
                        newLine.append(c)
                    out_lines.append("".join(newLine),end="")
                else:
                    out_lines.append(line.replace(",",";"),end="")
                    
    finally:
        arquivo.close()
    return "\n".join(out_lines)

def retornarCaminhoAbsoluto():
    return os.getcwd()

def retornarCaminhoRelativo(caminhoAbsoluto:str=""):
    if not caminhoAbsoluto:
        caminhoAbsoluto = retornarCaminhoAbsoluto()    
    return os.path.dirname(os.path.realpath(caminhoAbsoluto))

def pegarValor(df:pd.DataFrame,column):
    if len(df)>1:
        raise("Dataframe com mais de um elemento para ser extraído")
    return df[column].values[0]

def reduzir_a_um(lista):
    serie = pd.Series(lista).dropna()
    lista = serie[serie!=None].to_list()
    if len(lista)>1:
        raise Exception("Função reduzir_a_um não pode finalizar. Há dois valores válidos")
    elif len(lista)==1:
        return lista[0]
    else:
        return None

def timeToTimedelta(time:time) -> pd.Timestamp:
    if isinstance(time,float):
        return pd.Timestamp(0)
    elif pd.isnull(time):
        return pd.Timestamp(0)

    hours = time.hour
    minutes = time.minute
    seconds = time.second
    microseconds = time.microsecond
    return pd.Timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds
    )

def somar_data_e_hora(data:pd.Series,hora:pd.Series):
    retorno = []
    if len(data)==len(hora):
        for i in data.index:
            if pd.isnull(data[i]):
                raise Exception(f"[###] Data {data[i]} é não válido")
            elif pd.isnull(hora[i]):
                retorno.append(data[i])
            else:
                retorno.append(data[i]+hora[i])
    # raise Exception("Função somar_data_e_hora não implementada ainda. Falar com desenvolvedor do programa.")
    return pd.Series(retorno)

def retornarValorNaoNulo(valorAVerifica,valorParaRetornar):
    if pd.isnull(valorAVerifica):
        return valorParaRetornar
    elif pd.isna(valorAVerifica):
        return valorParaRetornar
    elif valorAVerifica==None:
        return valorParaRetornar
    else:
        return valorAVerifica
    
