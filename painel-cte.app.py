import streamlit as st
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Painel de CT-e", layout="wide")
st.title("📦 Painel de Gestão de CT-e")

# Upload do arquivo XML
uploaded_file = st.file_uploader("Faça o upload de um arquivo XML de CT-e", type=["xml"])

if uploaded_file is not None:
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()

        # Extrair o namespace (caso tenha, usado na estrutura do XML)
        ns = {'cte': 'http://www.portalfiscal.inf.br/cte'}

        # Extração das informações
        numero = root.find(".//cte:infCte/cte:nCT", ns).text if root.find(".//cte:infCte/cte:nCT", ns) is not None else "N/A"
        emitente = root.find(".//cte:emit/cte:xNome", ns).text if root.find(".//cte:emit/cte:xNome", ns) is not None else "N/A"
        valor_total = root.find(".//cte:vPrest/cte:vTPrest", ns).text if root.find(".//cte:vPrest/cte:vTPrest", ns) is not None else "0.00"
        peso_total = root.find(".//cte:infCarga/cte:pesoBruto", ns).text if root.find(".//cte:infCarga/cte:pesoBruto", ns) is not None else "0.00"
        motorista = root.find(".//cte:infCTe/cte:xNome", ns).text if root.find(".//cte:infCTe/cte:xNome", ns) is not None else "Desconhecido"
        placa = root.find(".//cte:infCTe/cte:placa", ns).text if root.find(".//cte:infCTe/cte:placa", ns) is not None else "Não Informada"
        destino = root.find(".//cte:dest/cte:xNome", ns).text if root.find(".//cte:dest/cte:xNome", ns) is not None else "N/A"
        data_emissao = root.find(".//cte:ide/cte:dhEmi", ns).text if root.find(".//cte:ide/cte:dhEmi", ns) is not None else "N/A"

        # Exibição das informações no Streamlit
        st.subheader("Informações extraídas:")
        st.write(f"*Número do CT-e:* {numero}")
        st.write(f"*Emitente:* {emitente}")
        st.write(f"*Valor Total:* R$ {valor_total}")
        st.write(f"*Peso Total:* {peso_total} kg")
        st.write(f"*Motorista:* {motorista}")
        st.write(f"*Placa do Veículo:* {placa}")
        st.write(f"*Destino:* {destino}")
        st.write(f"*Data de Emissão:* {data_emissao}")

    except Exception as e:
        st.error(f"Erro ao processar o XML: {str(e)}")
else:
    st.warning("Informe um arquivo XML de CT-e para processar.")