import requests
import pandas as pd
from sqlalchemy import create_engine
url_deputados = "https://dadosabertos.camara.leg.br/api/v2/deputados?siglaUf=DF"
deputados = requests.get(url_deputados).json()["dados"]

todas_despesas = []

# 2. Um loop para pegar as notas fiscais de cada um dos 8 deputados
for deputado_da_vez in deputados:
    id_deputado = deputado_da_vez['id']
    nome = deputado_da_vez['nome']
    
    print(f"Baixando notas fiscais de: {nome}...")
    
    # API que puxa os gastos do deputado usando o ID dele
    url_despesas = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_deputado}/despesas"
    pagina_atual = 1
    
    while True:
    
        parametros = {'ano': 2024, 'itens': 100, "pagina" : pagina_atual} 
        despesas_pagina = requests.get(url_despesas, params=parametros).json()['dados']
        
        if len(despesas_pagina) == 0:
            break
    
        # Adicionando o nome do deputado em cada nota fiscal para não misturar depois
        for nota in despesas_pagina:
            nota['nome_deputado'] = nome
            todas_despesas.append(nota)
        pagina_atual += 1

df_despesas = pd.DataFrame(todas_despesas)

# Mostrando o tamanho do arquivo e as primeiras linhas
print(f"\nTotal de notas fiscais baixadas: {len(df_despesas)}")
# print(df_despesas[['nome_deputado', 'tipoDespesa', 'valorDocumento', 'dataDocumento']].head(10))
# print(df_despesas.head())
df_despesas.info()
df_cadastro = pd.DataFrame(deputados)
gastos_grupados = df_despesas.groupby("nome_deputado")["valorLiquido"].sum().sort_values(ascending=False)
df_final = pd.merge(df_cadastro, gastos_grupados, left_on="nome", right_on="nome_deputado", how="left")
df_final["valorLiquido"] = df_final["valorLiquido"].fillna(0)
ranking = df_final.sort_values(by="valorLiquido",ascending=False)

print("Ranking deputado mais gastão de 2024")
ranking["valorFormatado"] = ranking["valorLiquido"].apply(lambda x: f"R$ {x:,.2f}")
print(ranking[["nome","valorFormatado", "siglaPartido"]])

# Agrupa por categoria de gasto e soma o valor
print("-" * 50)
print("---Onde cada deputado mais gastou---")
print("-" * 50)
lista_deputados = df_despesas['nome_deputado'].unique()

for deputado_da_vez in lista_deputados:
    print(f"\n=> DEPUTADO(A): {deputado_da_vez.upper()}")   
     
    df_deputado_atual = df_despesas[df_despesas['nome_deputado'] == deputado_da_vez]
    gastos = df_deputado_atual.groupby("tipoDespesa")["valorLiquido"].sum().sort_values(ascending=False)
    print(gastos.head(5).apply(lambda x: f"R$ {x:,.2f}"))
    print("-" * 50) 
 
print("\n--- TOP 5 FORNECEDORES POR DEPUTADO ---")

for deputado in lista_deputados:
    print(f"\n=> DEPUTADO(A): {deputado.upper()}")

    df_deputado_atual = df_despesas[df_despesas['nome_deputado'] == deputado]
    
    # Agrupa pelo nome da empresa e soma
    fornecedores = df_deputado_atual.groupby('nomeFornecedor')['valorLiquido'].sum().sort_values(ascending=False)
    
    print(fornecedores.head(5).apply(lambda x: f"R$ {x:,.2f}"))
    print("-" * 50)
    
    # Salva a base completa com todas as colunas
df_despesas.to_csv("despesas_detalhadas_2024.csv", index=False)

# Salva a tabela resumo com o ranking
df_final.to_csv("ranking_resumo_2024.csv", index=False)
#---Salvar NO Banco de Dados SQL----
engine = create_engine('mysql+pymysql://root:sua_senha_aqui@localhost:3306/camara_df')


print("Salvando Tabela Fato (Despesas Detalhadas)...")
df_despesas.to_sql('fato_despesas', con=engine, if_exists='replace', index=False)

print("Salvando Tabela Dimensão (Cadastro dos Deputados)...")
df_cadastro.to_sql('dim_deputados', con=engine, if_exists='replace', index=False)

print("✅ Sucesso! Dados salvos no banco de dados 'camara_df.db'.")