# 🤖 Intelligent Tech Support Agent (RAG)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![AI](https://img.shields.io/badge/LLM-Llama%203.3-orange)
![Streamlit](https://img.shields.io/badge/UI-Interactive-red)

An AI-powered Technical Support Assistant capable of answering questions based on **any PDF documentation** you upload. It uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware responses without hallucinations.

## ✨ Key Features

* **Drag & Drop Interface:** Upload any technical manual directly in the browser.
* **On-the-Fly Ingestion:** Automatically processes, chunks, and vectorizes documents in real-time.
* **Source Citations:** Every answer cites the specific page of the PDF used.
* **Privacy First:** Runs locally (or in container); data is processed within your session.

## 🏗 Architecture

The system is designed with a decoupled architecture for scalability:

1.  **Frontend & Orchestration (`ui.py`):**
    * Manages user file uploads.
    * Triggers the ingestion pipeline upon file receipt.
    * Displays chat interface only after the "Knowledge Base" is ready.

2.  **Ingestion Pipeline (`ingestion.py`):**
    * Extracts text from the uploaded PDF.
    * Splits text into semantic chunks (500 chars).
    * Generates embeddings using `sentence-transformers/paraphrase-multilingual`.
    * Stores vectors in **ChromaDB** (ephemeral or persistent).

3.  **Inference Engine (`app.py`):**
    * Retrieves top-3 relevant chunks via Semantic Search.
    * Generates answers using **Llama 3.3 (70B)** via Groq API.

## 🛠 Tech Stack

* **LLM:** Llama 3.3-70b-versatile (via Groq)
* **Embeddings:** HuggingFace (Open Source & Local)
* **Vector DB:** ChromaDB
* **Frontend:** Streamlit
* **Containerization:** Docker
* **Language:** Python 3.11

## 🚀 How to Run

### Option A: Using Docker (Recommended)

This ensures the application runs exactly as intended, regardless of your OS.

1.  **Build the image:**
    ```bash
    docker build -t rag-assistant-app .
    ```

2.  **Run the container:**
    *(Replace `your_key` with your actual Groq API Key)*
    ```bash
    docker run -e GROQ_API_KEY="your_key_here" -p 8501:8501 rag-assistant-app
    ```

3.  **Access the App:**
    * Open `http://localhost:8501` in your browser.
    * **Upload a PDF** in the sidebar and click "Processar".
    * Start chatting!

### Option B: Local Development

1.  **Clone and Install:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```

2.  **Configure Environment:**
    Create a `.env` file:
    ```env
    GROQ_API_KEY=gsk_...
    ```

3.  **Start App:**
    *(No need to run ingestion scripts manually anymore)*
    ```bash
    streamlit run src/ui.py
    ```



