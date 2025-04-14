import streamlit as st
import pandas as pd
import os
import xml.etree.ElementTree as ET
import plotly.express as px

st.set_page_config(page_title="Painel de CT-e", layout="wide")

st.title("📦 Painel de Gestão de CT-e")

# Upload do arquivo XML
uploaded_file = st.file_uploader("Faça o upload de um arquivo XML de CT-e", type=["xml"])

if uploaded_file is not None:
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()

        # Extração de dados adicionais
        numero = root.find(".//infCte/nCT").text
        emitente = root.find(".//emit/xNome").text
        valor_total = root.find(".//vPrest/vTPrest").text
        peso_total = root.find(".//infCarga/pesoBruto").text
        motorista = root.find(".//infCTe/motorista").text if root.find(".//infCTe/motorista") is not None else "Desconhecido"
        placa = root.find(".//infCarga/placa").text if root.find(".//infCarga/placa") is not None else "Não Informada"
        destino = root.find(".//dest/xNome").text

        st.subheader("Informações extraídas:")
        st.write(f"Número do CT-e: {numero}")
        st.write(f"Emitente: {emitente}")
        st.write(f"Valor Total: R$ {valor_total}")
        st.write(f"Peso Total: {peso_total} kg")
        st.write(f"Motorista: {motorista}")
        st.write(f"Placa do Veículo: {placa}")
        st.write(f"Destino: {destino}")

    except Exception as e:
        st.error(f"Erro ao processar o XML: {str(e)}")
else:
    st.warning("Informe um caminho válido com arquivos XML de CT-e.")