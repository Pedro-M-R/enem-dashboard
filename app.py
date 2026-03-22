import pandas as pd
import psycopg2 as pg
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# CONEXÃO COM BANCO
# -----------------------------
def connect_to_db():
    conn = pg.connect(
        host="bigdata.dataiesb.com",
        database="iesb",
        user="data_iesb",
        password="iesb",
        options='-c client_encoding=UTF8'
    )
    return conn


@st.cache_data
def load_data():
    conn = connect_to_db()

    query = """
    SELECT 
        no_municipio_prova,
        co_municipio_prova,
        sg_uf_prova,
        nome_uf_prova,
        regiao_nome_prova,
        nota_cn_ciencias_da_natureza,
        nota_lc_linguagens_e_codigos,
        nota_mt_matematica,
        nota_redacao,
        tp_status_redacao
    FROM public.ed_enem_2024_resultados
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df


df = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Escolha a análise:", [
    "Visão Geral",
    "Variáveis Qualitativas",
    "Variáveis Quantitativas",
    "Correlação"
])

# -----------------------------
# VISÃO GERAL
# -----------------------------
if opcao == "Visão Geral":
    st.title("Análise ENEM 2024")

    st.subheader("Dados")
    st.dataframe(df.head())

    st.subheader("Resumo Estatístico")
    st.write(df.describe())


# -----------------------------
# VARIÁVEIS QUALITATIVAS
# -----------------------------
elif opcao == "Variáveis Qualitativas":
    st.title("Análise de Variáveis Qualitativas")

    colunas_cat = [
        "sg_uf_prova",
        "nome_uf_prova",
        "regiao_nome_prova",
        "tp_status_redacao"
    ]

    variavel = st.selectbox("Escolha a variável:", colunas_cat)

    # Frequência
    freq = df[variavel].value_counts()
    st.subheader("Tabela de Frequência")
    st.write(freq)

    # Gráfico
    st.subheader("Gráfico de Barras")
    fig, ax = plt.subplots()
    freq.plot(kind='bar', ax=ax)
    st.pyplot(fig)


# -----------------------------
# VARIÁVEIS QUANTITATIVAS
# -----------------------------
elif opcao == "Variáveis Quantitativas":
    st.title("Análise de Variáveis Quantitativas")

    colunas_num = [
        "nota_cn_ciencias_da_natureza",
        "nota_lc_linguagens_e_codigos",
        "nota_mt_matematica",
        "nota_redacao"
    ]

    variavel = st.selectbox("Escolha a variável:", colunas_num)

    # Histograma
    st.subheader("Histograma")
    fig, ax = plt.subplots()
    sns.histplot(df[variavel].dropna(), kde=True, ax=ax)
    st.pyplot(fig)

    # Boxplot
    st.subheader("Boxplot")
    fig, ax = plt.subplots()
    sns.boxplot(x=df[variavel], ax=ax)
    st.pyplot(fig)


# -----------------------------
# CORRELAÇÃO
# -----------------------------
elif opcao == "Correlação":
    st.title("Matriz de Correlação")

    colunas_num = [
        "nota_cn_ciencias_da_natureza",
        "nota_lc_linguagens_e_codigos",
        "nota_mt_matematica",
        "nota_redacao"
    ]

    corr = df[colunas_num].corr()

    st.subheader("Tabela de Correlação")
    st.write(corr)

    st.subheader("Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)