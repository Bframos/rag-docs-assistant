import streamlit as st
import os
from ingestion import ingest_file 
from app import query_rag

st.set_page_config(page_title="Assistente de Documentos", page_icon="📄")

st.title("📄 Chat com os teus Documentos")

# --- BARRA LATERAL (Upload) ---
with st.sidebar:
    st.header("1. Carregar Documento")
    uploaded_file = st.file_uploader("Envia o teu PDF aqui", type="pdf")
    
    # Botão para processar
    if uploaded_file:
        # Precisamos de um botão para não reprocessar a cada clique
        if st.button("Processar e Criar Cérebro 🧠"):
            with st.spinner("A ler o PDF e a criar memórias... (isto pode demorar 1 min)"):
                
                # 1. Guardar o ficheiro temporariamente no disco
                # O PyPDFLoader precisa de um ficheiro físico, não de bytes na RAM
                os.makedirs("data", exist_ok=True)
                file_path = os.path.join("data", "temp_manual.pdf")
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 2. Chamar a Ingestão
                ingest_file(file_path)
                
                st.success("Pronto! Podes falar com o documento.")
                st.session_state["db_ready"] = True

# --- ÁREA PRINCIPAL (Chat) ---

# Só mostramos o chat se a base de dados estiver pronta
if st.session_state.get("db_ready"):
    st.caption("Fale com o documento carregado.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Pergunte algo sobre o PDF..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("A pensar..."):
                response_text, sources = query_rag(prompt)
                st.markdown(response_text)
                
                with st.expander("Ver fontes"):
                    for i, doc in enumerate(sources):
                        st.markdown(f"**Fonte {i+1} (Pág {doc.metadata.get('page_label', '?')}):**")
                        st.caption(doc.page_content[:200] + "...")

        st.session_state.messages.append({"role": "assistant", "content": response_text})

else:
    # Ecrã de "Boas Vindas" se ainda não houver PDF
    st.info("👈 Por favor, carrega um PDF na barra lateral para começar.")