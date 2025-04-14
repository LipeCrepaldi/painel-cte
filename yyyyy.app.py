import streamlit as st
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
    
    # Acessando as informações do XML
    st.write("Informações extraídas do CT-e:")
    
    # Exemplo de extração de dados específicos:
    
    # Número do CT-e
    cct = root.xpath("//infCTe/ide/cCT/text()")
    st.write(f"CT-e Número: {cct[0]}" if cct else "CT-e Número não encontrado.")
    
    # Data de Emissão
    dhEmi = root.xpath("//infCTe/ide/dhEmi/text()")
    st.write(f"Data de Emissão: {dhEmi[0]}" if dhEmi else "Data de Emissão não encontrada.")
    
    # Remetente (Transportadora)
    remetente = root.xpath("//infCTe/rem/xNome/text()")
    st.write(f"Transportadora: {remetente[0]}" if remetente else "Transportadora não encontrada.")
    
    # Motorista
    motorista = root.xpath("//infCTe/exped/xNome/text()")
    st.write(f"Motorista: {motorista[0]}" if motorista else "Motorista não encontrado.")
    
    # Placa do veículo
    placa_veiculo = root.xpath("//infCTe/veicTracao/placa/text()")
    st.write(f"Placa do Veículo: {placa_veiculo[0]}" if placa_veiculo else "Placa do Veículo não encontrada.")