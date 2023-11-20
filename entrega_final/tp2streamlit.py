import pandas as pd
import streamlit as st
import io
import sqlite3
import requests
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Download do dump:
url = 'https://github.com/caio-santt/IBD-2023-2/raw/main/tabelas.zip'
r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("/tmp/dataset")

conn = sqlite3.connect('/tmp/my_database.db')

# Carregar cada arquivo CSV no banco de dados SQLite
for filename in z.namelist():
    if filename.endswith('.csv'):
        df = pd.read_csv(f'/tmp/dataset/{filename}')
        table_name = filename.replace('.csv', '')
        df.to_sql(table_name, conn, if_exists='replace', index=False)

# Título e descrição inicial
st.title('Análise de Dados do Patrimônio Mobilirio Tombado da Fiocruz')
st.write("Neste aplicativo, exploraremos os dados do patrimônio mobiliario tombado da Fiocruz.")

# Descrição dos dados e do trabalho

# Seção de visualização de dados
st.header('Visualização de Dados')
st.write("Aqui, você pode adicionar gráficos e visualizações para representar os dados de forma mais interativa.")

# Exemplo para Consulta C01

st.header('Consulta C01 - Exemplo de Grafico de Barras')
query_c01 = """
-- C01

SELECT DISTINCT Armazenado.Bem_ID, Local.Endereco, Compra.Valor
FROM Armazenado
JOIN Local ON Armazenado.Local_ID = Local.ID
JOIN Compra ON Armazenado.Bem_ID = Compra.Bem_ID
WHERE TRIM(Local.Endereco) LIKE 'Laboratorio'
ORDER BY Valor DESC;

"""
df_c01 = pd.read_sql_query(query_c01, conn)

# Verificando e convertendo os dados
if 'Valor' in df_c01.columns:
    df_c01['Valor'] = df_c01['Valor'].str.replace(',', '.').astype(float)

# Removendo valores nulos
df_c01.dropna(subset=['Bem_ID', 'Valor'], inplace=True)

# Criando o gráfico
sns.barplot(data=df_c01, x='Bem_ID', y='Valor')
plt.xticks(rotation=45)
plt.title("Valores dos Bens em Laboratórios")
plt.xlabel("ID do Bem")
plt.ylabel("Valor")
st.pyplot(plt)
# Exemplo para Consulta C02
st.header('Consulta C02 - Exemplo de Grafico de Linha')
query_c02 = """
-- C02

SELECT strftime('%Y', Data) AS AnoAquisicao, CAST(REPLACE(Valor, ',', '.') AS DECIMAL(10, 2)) AS ValorConvertido
FROM Compra
WHERE CAST(REPLACE(Valor, ',', '.') AS DECIMAL(10, 2)) > 1000
ORDER BY AnoAquisicao ASC;

"""
df_c02 = pd.read_sql_query(query_c02, conn)

# Conversão para datetime e numérico
df_c02['AnoAquisicao'] = pd.to_datetime(df_c02['AnoAquisicao'], errors='coerce')
df_c02['ValorConvertido'] = pd.to_numeric(df_c02['ValorConvertido'], errors='coerce')

# Removendo valores nulos
df_c02.dropna(subset=['AnoAquisicao', 'ValorConvertido'], inplace=True)

# Criando o gráfico
sns.lineplot(data=df_c02, x='AnoAquisicao', y='ValorConvertido')
plt.xticks(rotation=45)
plt.title("Variação do Valor de Aquisição ao Longo do Tempo")
plt.xlabel("AnoAquisicao")
plt.ylabel("Valor Convertido")
st.pyplot(plt)

# Exemplo para Consulta C03
st.header('Consulta C03 - Exemplo de Tabela Interativa')
query_c03 = """
-- C03

SELECT DISTINCT
  A.Local_ID, B.Nome, B. Valor
FROM
  Bem AS B
  Join Armazenado as A
  ON B.Sequencia = A.BEM_ID
WHERE
  B.Valor = (SELECT MAX(Valor) FROM Bem)
ORDER BY A.Local_ID ASC

"""
df_c03 = pd.read_sql_query(query_c03, conn)
st.dataframe(df_c03)

# Exemplo para Consulta C04
st.header('Consulta C04 - Exemplo de Gráfico de Barras')
query_c04 = """
-- C04

SELECT DISTINCT
  B.Nome, C.Data, B.Situacao
FROM
  Bem B
  JOIN Compra C
    ON B.Sequencia = C.Bem_ID
WHERE
  TRIM(B.Situacao) = 'NORMAL'
ORDER BY
  C.Data ASC
LIMIT 20

"""
query_c04 = """
SELECT B.SEQUENCIA, B.NOME, B.SITUACAO, C.Data 
FROM Bem B
JOIN Compra C ON B.SEQUENCIA = C.Bem_ID
WHERE B.SITUACAO LIKE '%NORMAL%'
"""
df_c04 = pd.read_sql_query(query_c04, conn)

# Convertendo a coluna 'Data' para datetime
df_c04['Data'] = pd.to_datetime(df_c04['Data'], errors='coerce')

# Removendo valores nulos
df_c04.dropna(subset=['Data'], inplace=True)

# Contando o número de bens por data
df_c04_count = df_c04.groupby(df_c04['Data'].dt.date).count()['NOME'].reset_index()
df_c04_count.rename(columns={'NOME': 'Contagem'}, inplace=True)

# Criando o gráfico
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_c04_count, x='Data', y='Contagem')
plt.xticks(rotation=45)
plt.title("Contagem de Bens com Situação 'NORMAL' por Data")
plt.xlabel("Data de Compra")
plt.ylabel("Contagem de Bens")
st.pyplot(plt)

# Exemplo para Consulta C05

st.header('Consulta C05 - Exemplo de grafico de barras')
query_c05 = """
-- C05

SELECT DISTINCT
  B.Responsavel, C.Data
FROM
  Bem B
JOIN Compra C
  ON B.Sequencia = C.Bem_ID
ORDER BY
  C.Data ASC
LIMIT 20;

""" 

df_c05 = pd.read_sql_query(query_c05, conn)

st.dataframe(df_c05)

# Opção para ordenar os dados com base na coluna 'Data'
if st.checkbox("Ordenar por Data"):
    sorted_df = df.sort_values(by='Data')
    st.dataframe(sorted_df)


# Exemplo para Consulta C06
st.header('Consulta C06 - Exemplo de indicador numerico')
query_c06 = """
-- C06

SELECT
  COUNT(B.Sequencia)
FROM
  Bem B
  JOIN Armazenado A
    ON B.Sequencia = A.Bem_ID
  JOIN Local L
    ON A.Local_ID = L.ID
WHERE
  TRIM(B.Situacao) = 'ALIENADO POR LEILÃO'
  AND TRIM(L.Endereco) = 'AV. AUGUSTO DE LIMA- Nº1715  - BELO HORIZONTE'

"""

df_c06 = pd.read_sql_query(query_c06, conn)

# Verifique se a consulta retorna um único valor numérico
if df_c06.shape == (1, 1) and pd.api.types.is_numeric_dtype(df_c06.iloc[0, 0]):
    valor = df_c06.iloc[0, 0]
    st.metric(label="Número de Bens com Condição Específica", value=valor)
else:
    st.error("A consulta não retornou um valor numérico único. Por favor, verifique a consulta.")

# Exemplo para consulta C07
st.header('Consulta 07 - Exemplo de grafico de linha')

query_c07 = """
-- C07

SELECT DISTINCT
  B.Nome, C.Data
FROM
  Bem B
  JOIN Grupo_Siafi G
    ON B.Categoria_ID = G.Grupo
  JOIN Compra C
    ON B.Sequencia = C.Bem_ID
WHERE
  TRIM(G.Descricao) = 'VEICULOS EM GERAL'
ORDER BY
  C.Data ASC
LIMIT 20
"""

# Executar a consulta SQL e criar um DataFrame
df_c07 = pd.read_sql_query(query_c07, conn)

# Título da página
st.title("Visualização de Compras de Veículos em Geral")

# Tabela interativa para exibir os dados
st.write("Dados da consulta:")
st.dataframe(df_c07)

# Criar um gráfico de linha para mostrar a evolução das compras de veículos em geral ao longo do tempo
st.write("Evolução das Compras de Veículos em Geral ao Longo do Tempo:")

# Converter a coluna 'Data' para o tipo de data
df_c07['Data'] = pd.to_datetime(df_c07['Data'])

# Criar o gráfico de linha
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_c07['Data'], df_c07.index + 1, marker='o', linestyle='-')
ax.set_xlabel("Data")
ax.set_ylabel("Número de Compras")
ax.set_title("Evolução das Compras de Veículos em Geral ao Longo do Tempo")
ax.grid(True)

# Exibir o gráfico no Streamlit
st.pyplot(fig)

# Exemplo para Consulta C08
st.header('Consulta C08 - Exemplo de tabela interativa')

query_c08 = """
-- C08

SELECT
  B.Nome, B.Situacao
FROM
  Bem B
  JOIN Pertence P
    ON B.Sequencia = P.Bem_ID
  JOIN Unidade U
    ON P.Unidade_ID = U.Sigla
WHERE
  TRIM(U.Setor_Descricao) = 'FARMACIA POPULAR MG-BELO HORIZONTE'
"""

# Executar a consulta SQL e criar um DataFrame
df_c08 = pd.read_sql_query(query_c08, conn)

# Título da página
st.title("Visualização de Bens na FARMÁCIA POPULAR MG-BELO HORIZONTE")

# Tabela interativa para exibir os dados
st.write("Dados da consulta:")
st.dataframe(df_c08)

# Exemplo para consulta C09
st.header('Consulta C09 - Exemplo de Grafico de Barra')

query_c09 = """
-- C09

SELECT gs.Grupo, gs.Descricao, SUM(c.Valor) AS SomaValores
FROM Grupo_Siafi gs
JOIN Bem b ON gs.Grupo = b.Categoria_ID
LEFT JOIN Compra c ON b.Sequencia = c.Bem_Id
WHERE gs.Grupo IN (
  SELECT DISTINCT gs2.Grupo
  FROM (
    SELECT gs.Grupo, SUM(c2.Valor) AS SomaValores
    FROM Grupo_Siafi gs
    JOIN Bem b2 ON gs.Grupo = b2.Categoria_ID
    LEFT JOIN Compra c2 ON b2.Sequencia = c2.Bem_Id
    GROUP BY gs.Grupo
    ORDER BY SomaValores DESC
    LIMIT 7
  ) AS gs2
)
GROUP BY gs.Grupo, gs.Descricao
ORDER BY SomaValores DESC;
"""

# Executar a consulta SQL e criar um DataFrame
df_c09 = pd.read_sql_query(query_c09, conn)

# Título da página
st.title("Visualização dos Grupos e Soma de Valores")

# Gráfico de barras para visualizar os grupos e suas somas de valores
plt.figure(figsize=(10, 6))
plt.bar(df_c09['Descricao'], df_c09['SomaValores'])
plt.xlabel("Grupo de Categoria")
plt.ylabel("Soma de Valores")
plt.title("Soma de Valores por Grupo de Categoria")
plt.xticks(rotation=45, ha="right")
st.pyplot()

# Tabela interativa para exibir os dados
st.write("Dados da consulta:")
st.dataframe(df_c09)

# Exemplo para Consulta C10
st.header('Consulta C10 - Exemplo de Grafico de barras tombado')

query_c10 = """
-- C10

SELECT gs.Grupo,
       gs.Descricao AS DescricaoGrupo,
       SUM(c.Valor) * 1.0 / COUNT(DISTINCT b.Sequencia) AS MediaValorCompraPorBem
FROM Grupo_Siafi gs
JOIN Bem b ON gs.Grupo = b.Categoria_ID
LEFT JOIN Compra c ON b.Sequencia = c.Bem_Id
WHERE gs.Grupo IN (
  SELECT DISTINCT gs2.Grupo
  FROM (
    SELECT gs3.Grupo, SUM(c2.Valor) AS SomaValores
    FROM Grupo_Siafi gs3
    JOIN Bem b2 ON gs3.Grupo = b2.Categoria_ID
    LEFT JOIN Compra c2 ON b2.Sequencia = c2.Bem_Id
    GROUP BY gs3.Grupo
    ORDER BY SomaValores DESC
    LIMIT 7
  ) AS gs2
)
GROUP BY gs.Grupo, gs.Descricao
ORDER BY MediaValorCompraPorBem DESC;
"""

# Executar a consulta SQL e criar um DataFrame
df_c10 = pd.read_sql_query(query_c10, conn)

# Título da página
st.title("Média de Valor de Compra por Bem para Grupos de Categoria")

# Gráfico de barras empilhadas para visualizar a média de valor de compra por bem
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df_c10['DescricaoGrupo'], df_c10['MediaValorCompraPorBem'], color='skyblue')
plt.xlabel("Grupo de Categoria")
plt.ylabel("Média de Valor de Compra por Bem")
plt.title("Média de Valor de Compra por Bem para Grupos de Categoria")
plt.xticks(rotation=45, ha="right")

# Adicionar rótulos aos gráficos de barras
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

# Exibir o gráfico no Streamlit
st.pyplot(fig)

# Tabela interativa para exibir os detalhes dos grupos
st.write("Detalhes dos Grupos de Categoria:")
st.dataframe(df_c10)

