import streamlit as st
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Painel de CT-e", layout="wide")
st.title("📦 Painel de Gestão de CT-e")

uploaded_file = st.file_uploader("Faça o upload de um arquivo XML de CT-e", type=["xml"])

if uploaded_file is not None:
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()

        ns = {'cte': 'http://www.portalfiscal.inf.br/cte'}

        numero = root.find(".//cte:infCte/cte:ide/cte:nCT", ns)
        emitente = root.find(".//cte:emit/cte:xNome", ns)
        valor_total = root.find(".//cte:vPrest/cte:vTPrest", ns)
        peso_total = root.find(".//cte:infCarga/cte:pesoBruto", ns)
        motorista = root.find(".//cte:rodo/cte:xNome", ns)
        placa = root.find(".//cte:rodo/cte:veic/cte:placa", ns)
        destino = root.find(".//cte:dest/cte:xNome", ns)
        data_emissao = root.find(".//cte:ide/cte:dhEmi", ns)

        st.subheader("Informações extraídas:")
        st.write(f"Número do CT-e: {numero.text if numero is not None else 'N/A'}")
        st.write(f"Emitente: {emitente.text if emitente is not None else 'N/A'}")
        st.write(f"Valor Total: R$ {valor_total.text if valor_total is not None else '0.00'}")
        st.write(f"Peso Total: {peso_total.text if peso_total is not None else '0.00'} kg")
        st.write(f"Motorista: {motorista.text if motorista is not None else 'Desconhecido'}")
        st.write(f"Placa do Veículo: {placa.text if placa is not None else 'Não Informada'}")
        st.write(f"Destino: {destino.text if destino is not None else 'N/A'}")
        st.write(f"Data de Emissão: {data_emissao.text if data_emissao is not None else 'N/A'}")

    except Exception as e:
        st.error(f"Erro ao processar o XML: {str(e)}")
else:
    st.warning("Informe um arquivo XML de CT-e para processar.")