import streamlit as st
import pandas as pd
import os
import xml.etree.ElementTree as ET
import plotly.express as px

st.set_page_config(page_title="Painel de CT-e", layout="wide")

st.title("📦 Painel de Gestão de CT-e")
caminho = st.text_input("📁 Caminho da pasta com XMLs", "")

def ler_cte(path):
    dados = []
    for arquivo in os.listdir(path):
        if arquivo.endswith(".xml"):
            tree = ET.parse(os.path.join(path, arquivo))
            root = tree.getroot()

            # Pode variar por estado, ajustar se necessário
            ide = root.find(".//{*}ide")
            emit = root.find(".//{*}emit")
            dest = root.find(".//{*}dest")
            vPrest = root.find(".//{*}vPrest")
            infCTe = root.find(".//{*}infCte")

            try:
                dados.append({
                    "numero": ide.findtext("{*}nCT"),
                    "data_emissao": ide.findtext("{*}dhEmi")[:10],
                    "cnpj_emitente": emit.findtext("{*}CNPJ"),
                    "razao_emitente": emit.findtext("{*}xNome"),
                    "cnpj_tomador": dest.findtext("{*}CNPJ"),
                    "valor_total": float(vPrest.findtext("{*}vTPrest")),
                    "peso_total": float(root.findtext(".//{*}pesoBruto", default="0")),
                    "motorista": root.findtext(".//{*}xNome", default="Desconhecido")
                })
            except:
                pass
    return pd.DataFrame(dados)

if caminho and os.path.exists(caminho):
    df = ler_cte(caminho)

    col1, col2, col3 = st.columns(3)
    col1.metric("🧾 Total de CT-es", len(df))
    col2.metric("💰 Valor Total Transportado", f"R$ {df['valor_total'].sum():,.2f}")
    col3.metric("⚖ Peso Médio", f"{df['peso_total'].mean():.2f} kg")

    fig = px.line(df, x="data_emissao", y="valor_total", title="Valor por Dia")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Top Motoristas")
    top_motoristas = df.groupby("motorista")["valor_total"].sum().reset_index().sort_values(by="valor_total", ascending=False)
    st.dataframe(top_motoristas)

else:
    st.warning("Informe um caminho válido com arquivos XML de CT-e.")