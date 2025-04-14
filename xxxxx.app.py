import streamlit as st
import pandas as pd
import lxml.etree as ET

# Título da página
st.title("Painel de Gestão de CT-e")

# Solicita ao usuário para fazer o upload de um arquivo XML
uploaded_file = st.file_uploader("Escolha um arquivo XML de CT-e", type=["xml"])

# Quando o arquivo for carregado
if uploaded_file is not None:
    # Lê o arquivo XML
    tree = ET.parse(uploaded_file)
    root = tree.getroot()
    
    # Exemplo de como você pode acessar e exibir algumas informações do XML
    st.write("Exibindo informações do CT-e:")
    
    # Extrai tags do XML e mostra para o usuário
    for elem in root.iter():
        st.write(f"{elem.tag}: {elem.text}")