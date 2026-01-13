import streamlit as st
import os
from app import query_rag  # Importamos a lógica do outro ficheiro

# Configuração da Página
st.set_page_config(page_title="Assistente Técnico AI", page_icon="🤖")

st.title("🤖 Suporte Técnico Inteligente")
st.caption("Pergunte-me qualquer coisa sobre o Manual de Instruções.")

# Inicializar o histórico de chat (Session State)
# Isto é necessário porque o Streamlit "reseta" a cada clique.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensagens antigas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada do utilizador
if prompt := st.chat_input("Como posso ajudar?"):
    # 1. Guardar e mostrar a pergunta do utilizador
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Processar a resposta (Chamar o teu Backend)
    with st.chat_message("assistant"):
        with st.spinner("A consultar o manual..."):
            response_text, sources = query_rag(prompt)
            
            st.markdown(response_text)
            
            # Mostrar as fontes num menu expansível (Fica muito Pro!)
            with st.expander("📚 Ver fontes consultadas"):
                for i, doc in enumerate(sources):
                    st.markdown(f"**Excerto {i+1} (Pág {doc.metadata.get('page_label', '?')}):**")
                    st.caption(doc.page_content[:300] + "...")

    # 3. Guardar a resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": response_text})