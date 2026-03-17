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
        
        self.diametro = reduzir_a_um([
            dict(
                padrao=dict_cadastro['Diâmetro do Tubo'],
                pol=dict_cadastro['Diâmetro do Tubo (\')'],
                mm=dict_cadastro['Diâmetro do Tubo (mm)']
            )
        ])
        
        self.atencao = reduzir_a_um([
            dict_cadastro['Nível de Atenção (Maior que)'],
            dict_cadastro['Nível de Atenção no vetor deslocamento (Maior que)']
        ])
        
        self.alerta = reduzir_a_um([
            dict_cadastro['Nível de Alerta (Maior que)'],
            dict_cadastro['Nível de Alerta no vetor de deslocamento (Maior que)']
        ])
        
        self.emergencia = reduzir_a_um([
            dict_cadastro['Nível de Emergência (Maior que)'],
            dict_cadastro['Nível de Emergência no vetor de deslocamento (Maior que)']
        ])
        
        self.crista_barragem = reduzir_a_um([dict_cadastro['Cota da crista da barragem (m)']])
        self.soleira_vertedor = reduzir_a_um([dict_cadastro['Cota da soleira do vertedor (m)']])

        # ==============================
        # ATRIBUTOS EXISTENTES
        # ==============================
        self.porcentagem_seco:float = 0.0

        # ==============================
        # NOVOS ATRIBUTOS – TESTE DE VIDA
        # ==============================
        self.leituras_Teste_de_Vida = []
        self.datas_Teste_de_Vida = []
        self.porcentagem_Teste_de_Vida = 0.0
        
        pass