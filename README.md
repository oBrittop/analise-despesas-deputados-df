# 🕵️‍♂️ Análise de Despesas dos Deputados do DF (Cota Parlamentar)

Este projeto é um pipeline de ETL desenvolvido em **Python** que consome dados reais da API da Câmara dos Deputados, processa as notas fiscais e carrega as informações em um banco de dados **MySQL**.

## 🛠️ Tecnologias Utilizadas
* **Python** (Requests para consumir a API)
* **Pandas** (Tratamento, limpeza e agregação de dados)
* **SQLAlchemy & MySQL** (Carga de dados via Tabela Fato e Dimensão)

## 💡 Principais Descobertas (Insights de 2024)
Durante a análise exploratória, descobrimos que a maior parte da cota é gasta com **Divulgação da Atividade Parlamentar**. 
* O Deputado Alberto Fraga liderou os gastos, concentrando R$ 240 mil em uma única gráfica.
* A Deputada Erika Kokay utilizou R$ 377 mil em uma única associação para gestão de marketing digital e automação.

## 🚀 Como rodar o projeto
1. Clone o repositório.
2. Instale as bibliotecas: `pip install pandas requests sqlalchemy pymysql`
3. Crie um banco chamado `camara_df` no seu MySQL.
4. Altere a string de conexão no arquivo `app.py`.
5. Rode `python app.py`.

## 🧠 Entendendo o Código (Por baixo dos panos)

Para quem quiser mergulhar na engenharia de dados deste projeto, aqui estão os principais conceitos e funções utilizados no script de extração:

* **`requests.get()`**: Responsável por fazer a comunicação HTTP com os servidores do Governo. Um retorno com *Status 200 (OK)* garante que a conexão foi bem-sucedida.
* **`.json()`**: Converte a resposta bruta da web em um Dicionário Python, estruturando os dados para leitura.
* **Acesso à chave `["dados"]`**: A API da Câmara encapsula as informações de retorno dentro desta chave. O script a acessa diretamente para isolar apenas os registros que importam.
* **Uso de `params`**: Parâmetros de URL aplicados para realizar filtros direto na fonte (como `ano=2024` e limites de paginação), respeitando as regras e cotas da API de Dados Abertos.
* **Transformação (The Pandas Magic)**: Após aplicar os filtros de ano e realizar a paginação das notas fiscais, o script carimba o nome do deputado correspondente em cada nota para evitar perda de referência cruzada. Tudo é armazenado em uma lista temporal (`todas_despesas`) e, finalmente, convertido em um DataFrame (`df_despesas`) — o formato ideal para limpeza, agregação e envio ao Banco de Dados.