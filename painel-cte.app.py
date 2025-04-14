# 1. Imports
import streamlit as st
import streamlit_authenticator as stauth
import xml.etree.ElementTree as ET
import pandas as pd
import os

# 2. Login
# Dados de exemplo
users = {
    "cliente1": {"name": "Transportadora Fictícia 1", "password": "123"},
    "cliente2": {"name": "Transportadora Fictícia 2", "password": "456"}
}

usernames = list(users.keys())
names = [users[u]["name"] for u in usernames]
passwords = [users[u]["password"] for u in usernames]

authenticator = stauth.Authenticate(names, usernames, passwords, "painel_cte", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

# 3. Se estiver autenticado, mostra painel
if authentication_status:
    st.success(f"Bem-vindo, {name}!")

    st.title("📦 Painel de Gestão de CT-e")

    uploaded_file = st.file_uploader("Faça o upload de um arquivo XML de CT-e", type=["xml"])

    if uploaded_file is not None:
        try:
            tree = ET.parse(uploaded_file)
            root = tree.getroot()

            ns = {'cte': 'http://www.portalfiscal.inf.br/cte'}

            numero = root.find(".//cte:infCte/cte:nCT", ns).text if root.find(".//cte:infCte/cte:nCT", ns) is not None else "N/A"
            emitente = root.find(".//cte:emit/cte:xNome", ns).text if root.find(".//cte:emit/cte:xNome", ns) is not None else "N/A"
            valor_total = root.find(".//cte:vPrest/cte:vTPrest", ns).text if root.find(".//cte:vPrest/cte:vTPrest", ns) is not None else "0.00"
            peso_total = root.find(".//cte:infCarga/cte:pesoBruto", ns).text if root.find(".//cte:infCarga/cte:pesoBruto", ns) is not None else "0.00"
            motorista = root.find(".//cte:infCTe/cte:xNome", ns).text if root.find(".//cte:infCTe/cte:xNome", ns) is not None else "Desconhecido"
            placa = root.find(".//cte:infCTe/cte:placa", ns).text if root.find(".//cte:infCTe/cte:placa", ns) is not None else "Não Informada"
            destino = root.find(".//cte:dest/cte:xNome", ns).text if root.find(".//cte:dest/cte:xNome", ns) is not None else "N/A"
            data_emissao = root.find(".//cte:ide/cte:dhEmi", ns).text if root.find(".//cte:ide/cte:dhEmi", ns) is not None else "N/A"

            st.subheader("Informações extraídas:")
            st.write(f"Número do CT-e: {numero}")
            st.write(f"Emitente: {emitente}")
            st.write(f"Valor Total: R$ {valor_total}")
            st.write(f"Peso Total: {peso_total} kg")
            st.write(f"Motorista: {motorista}")
            st.write(f"Placa do Veículo: {placa}")
            st.write(f"Destino: {destino}")
            st.write(f"Data de Emissão: {data_emissao}")

        except Exception as e:
            st.error(f"Erro ao processar o XML: {str(e)}")
    else:
        st.warning("Faça upload de um arquivo XML.")
elif authentication_status == False:
    st.error("Usuário ou senha incorretos.")
elif authentication_status == None:
    st.warning("Insira usuário e senha para acessar.")