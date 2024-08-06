# Imports necessários
import numpy as np
import pandas as pd
import streamlit as st

# Carregar dados
caminho = r'df_venda.csv'
df = pd.read_csv(caminho)

# Função para converter preços e outros valores para float
def converter_para_float(valor):
    if isinstance(valor, str):
        valor = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
        return float(valor)
    return valor

# Aplicando a função para as colunas de interesse
df['Preco'] = df['Preco'].apply(converter_para_float)
df['m2'] = df['m2'].apply(converter_para_float)
df['Vagas'] = df['Vagas'].apply(converter_para_float)

# Resolvendo NaN
df['Dormitorios'].fillna(0, inplace=True)
df['Banheiros'].fillna(0, inplace=True)
df['Vagas'].fillna(0, inplace=True)
df['Suite'].fillna(0, inplace=True)
df['mobiliado'].fillna('Não', inplace=True)

# Interface com o usuário usando Streamlit
st.title("Análise de Imóveis - Valores Médios e Filtragem")

# Input do usuário
cidade = st.selectbox("Cidade", df['Cidade'].unique())
bairro = st.selectbox("Bairro", df['Bairro'].unique())
mobiliado = st.selectbox("Mobiliado", ['Sim', 'Não'])
banheiros = st.number_input("Número de Banheiros", min_value=1, max_value=10, step=1)
dormitorios = st.number_input("Número de Dormitórios", min_value=1, max_value=10, step=1)
area_m2 = st.number_input("Área (m²)", min_value=10, max_value=1000, step=1)

# Botão para calcular
if st.button("Calcular Valor Médio"):
    # Calculando a média dos preços dos imóveis similares
    filtros = (
        (df['Cidade'] == cidade) &
        (df['Bairro'] == bairro) &
        (df['mobiliado'] == mobiliado) &
        (df['Banheiros'] >= banheiros) &
        (df['Dormitorios'] >= dormitorios) &
        (df['m2'] >= area_m2)
    )
    imoveis_similares = df[filtros]
    
    if not imoveis_similares.empty:
        media_preco = imoveis_similares['Preco'].mean()
        st.write(f"Valor Médio dos Imóveis Similares: R$ {media_preco:,.2f}")

        # Cálculos de variações
        valor_menos_5 = media_preco * 0.95
        valor_menos_10 = media_preco * 0.90
        valor_menos_15 = media_preco * 0.85

        st.write(f"Valor com -5%: R$ {valor_menos_5:,.2f}")
        st.write(f"Valor com -10%: R$ {valor_menos_10:,.2f}")
        st.write(f"Valor com -15%: R$ {valor_menos_15:,.2f}")
    else:
        st.write("Nenhum imóvel similar encontrado para calcular a média.")


st.title("Amostras por bairro")
amos = df['Bairro'].value_counts()
st.table(data=amos)

# Exibição da tabela de dados original
st.table(data=df)

# Cálculo do valor médio por bairro
Filtro = df.groupby(['Bairro'])['Preco'].mean()
st.title("Valor médio por Bairros")
st.table(data=Filtro)

# Análise de preços por área
f1 = df[df['m2'] <= 20]
f2 = df[df['m2'] <= 40]
f3 = df[df['m2'] <= 60]
f4 = df[df['m2'] <= 80]
f5 = df[df['m2'] <= 100]
f6 = df[df['m2'] <= 120]
f7 = df[df['m2'] <= 140]

st.title("Valor médio por Bairros > 20m2")
Filtro1 = f1.groupby(f1['Bairro'])['Preco'].mean()
st.table(data=Filtro1)

st.title("Valor médio por Bairros > 40m2")
Filtro2 = f2.groupby(f2['Bairro'])['Preco'].mean()
st.table(data=Filtro2)

st.title("Valor médio por Bairros > 60m2")
Filtro3 = f3.groupby(f3['Bairro'])['Preco'].mean()
st.table(data=Filtro3)

st.title("Valor médio por Bairros > 80m2")
Filtro4 = f4.groupby(f4['Bairro'])['Preco'].mean()
st.table(data=Filtro4)

st.title("Valor médio por Bairros > 100m2")
Filtro5 = f5.groupby(f5['Bairro'])['Preco'].mean()
st.table(data=Filtro5)

st.title("Valor médio por Bairros > 120m2")
Filtro6 = f6.groupby(f6['Bairro'])['Preco'].mean()
st.table(data=Filtro6)

st.title("Valor médio por Bairros > 140m2")
Filtro7 = f7.groupby(f7['Bairro'])['Preco'].mean()
st.table(data=Filtro7)
