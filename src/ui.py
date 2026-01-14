import streamlit as st
import os
import requests


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Assistente de Documentos (Via API)", page_icon="📡")

st.title("📡 Chat com Docs (Arquitetura API)")

# --- BARRA LATERAL (Upload) ---
with st.sidebar:
    st.header("1. Carregar Documento")
    uploaded_file = st.file_uploader("Envia o teu PDF aqui", type="pdf")
    
    if uploaded_file:
        if st.button("Enviar para a API 🚀"):
            with st.spinner("A enviar bytes para o servidor..."):
                try:
                    # 1. Preparar o ficheiro para envio via HTTP
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    
                    # 2. Fazer o POST request para o endpoint /ingest
                    response = requests.post(f"{API_URL}/ingest", files=files)
                    
                    if response.status_code == 200:
                        st.success("API: Documento processado com sucesso!")
                        st.session_state["db_ready"] = True
                    else:
                        st.error(f"Erro na API: {response.text}")
                        
                except Exception as e:
                    st.error(f"Não consegui contactar a API. Ela está ligada? Erro: {e}")

# --- ÁREA PRINCIPAL (Chat) ---

if st.session_state.get("db_ready"):
    st.caption("Conectado ao Cérebro Remoto via FastAPI.")

    # Histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do utilizador
    if prompt := st.chat_input("Pergunte algo sobre o PDF..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("A aguardar resposta da API..."):
                try:
                    # 3. Enviar a pergunta para o endpoint /chat
                    payload = {"query": prompt}
                    response = requests.post(f"{API_URL}/chat", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("response", "Sem resposta.")
                        sources = data.get("sources", [])
                        
                        st.markdown(answer)
                        
                        # Mostrar fontes vindas do JSON
                        if sources:
                            with st.expander("Ver fontes (JSON)"):
                                st.json(sources)
                                
                        # Atualizar histórico
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"Erro da API: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")

else:
    st.info("👈 A API está à espera do teu PDF na barra lateral.")