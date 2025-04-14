import streamlit as st
import pandas as pd
import os
import xml.etree.ElementTree as ET
import plotly.express as px
from lxml import etree

st.set_page_config(page_title="Painel de CT-e", layout="wide")
st.title("📦 Painel de Gestão de CT-e")

# Upload do arquivo XML
uploaded_file = st.file_uploader("Faça o upload de um arquivo XML de CT-e", type=["xml"])

if uploaded_file is not None:
    try:
        tree = etree.parse(uploaded_file)
        root = tree.getroot()

        # Defina o namespace correto para o XML
        ns = {'cte': 'http://www.portalfiscal.inf.br/cte'}

        # Extração de dados usando o namespace
        ide = root.find('.//cte:infCte/cte:ide', ns)
        emit = root.find('.//cte:infCte/cte:emit', ns)
        vPrest = root.find('.//cte:infCte/cte:vPrest', ns)

        # Garantir que os dados sejam extraídos corretamente
        numero_cte = ide.find('cte:nCT', ns).text if ide is not None else "N/A"
        emitente = emit.find('cte:xNome', ns).text if emit is not None else "N/A"
        valor_total = float(vPrest.find('cte:vTPrest', ns).text) if vPrest is not None else 0.0

        # Exibir as informações extraídas
        st.subheader("Informações extraídas:")
        st.metric("🧾 Número do CT-e", numero_cte)
        st.metric("🚛 Emitente", emitente)
        st.metric("💰 Valor Total", f"R$ {valor_total:,.2f}")

    except Exception as e:
        st.error(f"Erro ao processar o XML: {str(e)}")

else:
    st.warning("Informe um caminho válido com arquivos XML de CT-e.")