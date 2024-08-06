# Imports necessários
#%%
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression, Ridge
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score

# Carregar dados
caminho = r'paulo1258/Gramado/df_venda.csv'
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

# Transformando as colunas em dummies
df_dummies = pd.get_dummies(df)

# Dividir os dados em características e alvo
x = df_dummies.drop(['Preco'], axis=1)
y = df_dummies['Preco']

# Dividir os dados em conjuntos de treino e teste
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

# Alinhando colunas de treino e teste
x_train, x_test = x_train.align(x_test, axis=1, fill_value=0)

# Instanciar e treinar os modelos
model_XGB = XGBRegressor()
model_lin_reg = LinearRegression()
model_ridge = Ridge()

model_XGB.fit(x_train, y_train)
model_lin_reg.fit(x_train, y_train)
model_ridge.fit(x_train, y_train)

# Interface com o usuário usando Streamlit
st.title("Previsão de Preço de Imóvel - Ridge, Regressão linear e XGB")

# Input do usuário
cidade = st.selectbox("Cidade", df['Cidade'].unique())
bairro = st.selectbox("Bairro", df['Bairro'].unique())
mobiliado = st.selectbox("Mobiliado", ['Sim', 'Não'])
banheiros = st.number_input("Número de Banheiros", min_value=1, max_value=10, step=1)
dormitorios = st.number_input("Número de Dormitórios", min_value=1, max_value=10, step=1)
area_m2 = st.number_input("Área (m²)", min_value=10, max_value=1000, step=1)

# Definindo tolerância para valores numéricos
tolerancia = 0.8  # 20%
tolerancia2 = 0.2  # 20%

# Botão para prever
if st.button("Prever Preço"):
    # Criando um DataFrame com os dados de entrada do usuário
    dados_usuario = pd.DataFrame({
        'Cidade': [cidade],
        'Bairro': [bairro],
        'mobiliado': [mobiliado],
        'Banheiros': [banheiros],
        'Dormitorios': [dormitorios],
        'm2': [area_m2]
    })

    # Convertendo variáveis categóricas em dummies
    dados_usuario = pd.get_dummies(dados_usuario, drop_first=True)

    # Alinhando colunas do input do usuário com o modelo
    dados_usuario = dados_usuario.reindex(columns=x_train.columns, fill_value=0)

    # Fazendo a previsão com cada modelo
    previsao_XGB = model_XGB.predict(dados_usuario)
    previsao_lin_reg = model_lin_reg.predict(dados_usuario)
    previsao_ridge = model_ridge.predict(dados_usuario)

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
 
st.table(data=df)
#%%
Filtro = df.groupby(['Bairro'])['Preco'].mean()
st.title("Valor médio por Bairros")
st.table(data=Filtro)

#%%

f1 = df[df['m2'] <= 20]

f2 = df[df['m2'] <= 40]

f3 = df[df['m2'] <= 60]

f4 = df[df['m2'] <= 80]

f5 = df[df['m2'] <= 100]

f6 = df[df['m2'] <= 120]

f7 = df[df['m2'] <= 140]

st.title("Valor médio por Bairros > 20m2")
# Valor médio por Bairros > 20m2
Filtro1 = df.groupby(f1['Bairro'])['Preco'].mean()
st.table(data=Filtro1)

st.title("Valor médio por Bairros > 40m2")
# Valor médio por Bairros > 40m2
Filtro2 = df.groupby(f2['Bairro'])['Preco'].mean()
st.table(data=Filtro2)

st.title("Valor médio por Bairros > 60m2")
# Valor médio por Bairros > 60m2
Filtro3 = df.groupby(f3['Bairro'])['Preco'].mean()
st.table(data=Filtro3)

st.title("Valor médio por Bairros > 80m2")
# Valor médio por Bairros > 80m2
Filtro4 = df.groupby(f4['Bairro'])['Preco'].mean()
st.table(data=Filtro4)

st.title("Valor médio por Bairros > 100m2")
# Valor médio por Bairros > 100m2
Filtro5 = df.groupby(f5['Bairro'])['Preco'].mean()
st.table(data=Filtro5)

st.title("Valor médio por Bairros > 120m2")
# Valor médio por Bairros > 120m2
Filtro6 = df.groupby(f6['Bairro'])['Preco'].mean()
st.table(data=Filtro6)

st.title("Valor médio por Bairros > 140m2")
# Valor médio por Bairros > 140m2
Filtro7 = df.groupby(f7['Bairro'])['Preco'].mean()
st.table(data=Filtro7)
