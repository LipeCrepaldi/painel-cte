import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET

# Configuração da página
st.set_page_config(page_title="Painel de CT-e", layout="wide")

# Título da página
st.title("📦 Painel de Gestão de CT-e")

# Upload do arquivo XML
uploaded_file = st.file_uploader("📄 Faça o upload de um arquivo XML de CT-e", type=["xml"])

# Quando o arquivo é carregado
if uploaded_file is not None:
    try:
        # Parse do XML
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        ns = {'ns': 'http://www.portalfiscal.inf.br/cte'}

        # Extração dos dados do XML
        ide = root.find('.//ns:ide', ns)
        emit = root.find('.//ns:emit', ns)
        vPrest = root.find('.//ns:vPrest', ns)

        numero_cte = ide.find('ns:nCT', ns).text if ide is not None else "N/A"
        emitente = emit.find('ns:xNome', ns).text if emit is not None else "N/A"
        valor_total = float(vPrest.find('ns:vTPrest', ns).text) if vPrest is not None else 0.0

        # Exibindo as métricas
        st.metric("🧾 Número do CT-e", numero_cte)
        st.metric("🚛 Emitente", emitente)
        st.metric("💰 Valor Total", f"R$ {valor_total:,.2f}")

    except Exception as e:
        st.error(f"Erro ao processar o XML: {e}")
else:
    st.warning("Por favor, faça o upload de um arquivo XML de CT-e.")