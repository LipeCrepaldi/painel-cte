import streamlit as st
import pandas as pd
import os
import xml.etree.ElementTree as ET
import plotly.express as px

st.set_page_config(page_title="Painel de CT-e", layout="wide")

st.title("📦 Painel de Gestão de CT-e")
import streamlit as st
import pandas as pd
from lxml import etree

st.title("Painel de Gestão de CT-e")

# Upload do arquivo XML
uploaded_file = st.file_uploader("Faça o upload de um arquivo XML de CT-e", type=["xml"])

if uploaded_file is not None:
    try:
        tree = etree.parse(uploaded_file)
        root = tree.getroot()

        # Exemplo de extração de dados
        numero = root.find(".//infCte/nCT").text
        emitente = root.find(".//emit/xNome").text

        st.subheader("Informações extraídas:")
        st.write(f"Número do CT-e: {numero}")
        st.write(f"Emitente: {emitente}")

    except Exception as e:
        st.error(f"Erro ao processar o XML: {str(e)}")
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

uploaded_file = st.file_uploader("📄 Faça o upload de um arquivo XML de CT-e", type="xml")

if uploaded_file is not None:
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        ns = {'ns': 'http://www.portalfiscal.inf.br/cte'}

        ide = root.find('.//ns:ide', ns)
        emit = root.find('.//ns:emit', ns)
        vPrest = root.find('.//ns:vPrest', ns)

        numero_cte = ide.find('ns:nCT', ns).text if ide is not None else "N/A"
        emitente = emit.find('ns:xNome', ns).text if emit is not None else "N/A"
        valor_total = float(vPrest.find('ns:vTPrest', ns).text) if vPrest is not None else 0.0

        st.metric("🧾 Número do CT-e", numero_cte)
        st.metric("🚛 Emitente", emitente)
        st.metric("💰 Valor Total", f"R$ {valor_total:,.2f}")
    except Exception as e:
        st.error(f"Erro ao processar o XML: {e}")
else:
    st.warning("Informe um caminho válido com arquivos XML de CT-e.")