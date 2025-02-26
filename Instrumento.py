from pandas import isna,Series,DataFrame,Timestamp,Timedelta
from numpy import where,nan
from modules import log, reduzir_a_um, timeToTimedelta, somar_data_e_hora
from datetime import time

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
        
        self.leituras_nao_realizada = df_mod[df_mod["Situação da Medição"]=="Não Realizada"]
        self.leituras_outliers = df_mod[df_mod["Outlier"]=="SIM"]
        
        df_mod = df_mod[df_mod["Situação da Medição"]=="Realizada"]
        df_mod = df_mod[isna(df_mod["Outlier"])]
        self.leituras_nulas = df_mod[isna(df_mod["Valor"])]
        df_mod = df_mod[~isna(df_mod["Valor"])]
        
        valores_secos_jorrantes = Series(df_mod[~isna(df_mod["Condição Adversa"])]["Valor"])
        if not (len(valores_secos_jorrantes)==0): # Há leituras secas e jorrantes
            valores_secos_jorrantes = valores_secos_jorrantes.dropna()
            if len(valores_secos_jorrantes.to_list())>0:
                raise Exception(f"Valores escritos em leituras secas/jorrantes no instrumento {self.codigo}:\n{isna(valores_secos_jorrantes[0])}")
            df_mod.loc[df_mod["Condição Adversa"]=="SECO"]["Valor"] = self.fundo_ou_base
            df_mod.loc[df_mod["Condição Adversa"]=="JORRANTE"]["Valor"] = self.topo

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
        relatorio += f"""LEITURAS OUTLIERS:\n{self.leituras_outliers[["Data de Medição","Hora da Medição","Valor","Unidade de Medida"]].to_string()}\n\n"""            
        relatorio += f"""LEITURAS ACIMA DE NÍVEL DE CONTROLE:\n{self.leituras_acima_nv_controle[["Data de Medição","Hora da Medição","Valor","Unidade de Medida"]].to_string()}\n\n"""
        relatorio += f"""LEITURAS ABAIXO DA COTA DE FUNDO/BASE:\n{self.leituras_abaixo_base[["Data de Medição","Hora da Medição","Valor","Unidade de Medida"]].to_string()}\n\n"""
        relatorio += f"""LEITURAS ACIMA DA COTA DE TOPO:\n{self.leituras_acima_topo[["Data de Medição","Hora da Medição","Valor","Unidade de Medida"]].to_string()}\n\n"""
        relatorio += f"""LEITURAS NÃO REALIZADAS:\n{self.leituras_nao_realizada[["Data de Medição","Hora da Medição","Justificativa de não Medição","Observação"]].to_string()}\n\n"""
        relatorio+="---------------\n"
        if file_path:
            with open(file=file_path,mode="a") as file:
                file.write(relatorio)
        return relatorio