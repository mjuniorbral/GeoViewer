# PROGRAMA GEOVIEWER

**Objetivo:** Renderizar gráficos de leituras de instrumentos e outros dados de geotecnia.

**Desenvolvedor:** Marcelo Cabral dos Santos Junior *(Analista Técnico de Engenharia Civil na GEOCOBA - Projetos de Engenharia (https://www.geocoba.com/))*

**Data de início de desenvolvimento:** 02/01/2024

**Contato: mjuniorbral@gmail.com**

## Descrição das dependências
- Versão utilizada do Python: 3.10.11

Módulos externos utilizados (instalados através do pip install obtido no Microsoft Store junto com o Python 3.10.11):
- pandas (2.2.3): utilizado pra abrir e importar a planilha de entradas da sondagem // Instale usando o comando PIP ``pip install pandas``
- numpy (2.1.0): usado para operar vetores e dados // Instale usando o comando PIP ``pip install numpy``
- openpyxl (3.1.5): utilizado para possibilitar a interação com arquivos .xls e .xlsx // Instale usando o comando PIP ``pip install openpyxl``
- matplotlib (3.9.2): utilizado para criar gráficos e visualizações de dados // Instale usando o comando PIP `pip install matplotlib`

## Estrutura de arquivos e pastas necessária
- /.
- /historico.py (programa principal para renderizar os gráficos de histórico das leituras dos instrumentos)
- /inclinometro.py (programa principal para renderizar os gráficos das leituras de inclinômetros)
- /data/ (Planilhas com dados de entrada)
- /images/ (pasta de saídas das imagens)
    - /images/incGrafico (pasta de saídas das imagens do inclinometro.py)
    - /images/nivelGrafico (pasta de saídas das imagens dos níveis do historico.py)
- /modules/ (módulos auxiliares)
    - /modules/AgCadastro/ (módulo de aglutinação de tabelas usado para juntar as planilhas de cadastro)
        - /modules/AgCadastro/\__init__.py (inicializador da pasta de módulos AgCadastro)
        - /modules/AgCadastro/auxiliares.py (funções auxiliares do agCadastro)
        - /modules/AgCadastro/const.py (constantes e hashmap de cabeçalhos)
        - /modules/AgCadastro/main.py (programa com a função principal do módulo)
    - /modules/\__init__.py (inicializador da pasta de módulos)
    - /modules/classes.py (módulo com as classes Serie, Graphic e Instrumento que estão sendo usadas)
    - /modules/functions.py (módulo para funções auxiliares)
    - /modules/log.py (módulo para a função log do módulo logging)
    - /modules/timer_.py (módulo para a classe Timer usada para calcular tempo de execução do programa)
    - /modules/var.py (módulo com valores de cores registrados para uso)

## Notas das atualizações
- Versão 0.0.1 - 27/02/2025 - Beta Testing, versão inicial finalizada
