import streamlit as st
import os
import requests


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Document Assistant (RAG)", page_icon="📡")

st.title("📡 Document Assistant (RAG)")

# --- Sidebar (Upload) ---
with st.sidebar:
    st.header("1. Load Document ")
    uploaded_file = st.file_uploader("Send your PDF here", type="pdf")
    
    if uploaded_file:
        if st.button("Send to API 🚀"):
            with st.spinner("Sending bytes to the server..."):
                try:
                    # 1. Prepare file for upload
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    
                    # 2. Post to /ingest endpoint
                    response = requests.post(f"{API_URL}/ingest", files=files)
                    
                    if response.status_code == 200:
                        st.success("API: Document processed successfully!")
                        st.session_state["db_ready"] = True
                    else:
                        st.error(f"Error in API: {response.text}")
                        
                except Exception as e:
                    st.error(f"Failed to contact the API. Is it running? Error: {e}")

# --- MAIN AREA (Chat) ---

if st.session_state.get("db_ready"):
    st.caption("Connected to FastAPI.")

    # History of messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do utilizador
    if prompt := st.chat_input("Ask your question about the document"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Waiting for response..."):
                try:
                    # 3. Send to API
                    payload = {"query": prompt}
                    response = requests.post(f"{API_URL}/chat", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("response", "No answer.")
                        sources = data.get("sources", [])
                        
                        st.markdown(answer)
                        
                        # Show sources
                        if sources:
                            with st.expander("Show sources (JSON)"):
                                st.json(sources)
                                
                        # Update history
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"Error from API: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Connection error: {e}")
else:
    st.info("👈 Please upload a PDF in the sidebar.")