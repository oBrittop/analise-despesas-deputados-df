import requests
import pandas as pd
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
    
    parametros = {'ano': 2024, 'itens': 100} 
    despesas = requests.get(url_despesas, params=parametros).json()['dados']
    
    # Adicionando o nome do deputado em cada nota fiscal para não misturar depois
    for nota in despesas:
        nota['nome_deputado'] = nome
        todas_despesas.append(nota)

df_despesas = pd.DataFrame(todas_despesas)

# Mostrando o tamanho do arquivo e as primeiras linhas
# print(f"\nTotal de notas fiscais baixadas: {len(df_despesas)}")
# print(df_despesas[['nome_deputado', 'tipoDespesa', 'valorDocumento', 'dataDocumento']].head(10))
# print(df_despesas.head())
df_despesas.info()
df_cadastro = pd.DataFrame(deputados)
gastos_grupados = df_despesas.groupby("nome_deputado")["valorLiquido"].sum().sort_values(ascending=False)
df_final = pd.merge(df_cadastro, gastos_grupados, left_on="nome", right_on="nome_deputado", how="left")
df_final["valorDocumento"] = df_final["valorLiquido"].fillna(0)
ranking = df_final.sort_values(by="valorDocumento",ascending=False)

print("Ranking deputado mais gastão de 2024")
ranking["valorFormatado"] = ranking["valorLiquido"].apply(lambda x: f"R$ {x:,.2f}")
print(ranking[["nome","valorFormatado", "siglaPartido"]])