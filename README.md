# 🤖 Intelligent Tech Support Agent (RAG)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![AI](https://img.shields.io/badge/LLM-Llama%203.3-orange)

An AI-powered Technical Support Assistant capable of answering questions based on internal documentation (PDFs). It uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware responses without hallucinations.

## 🏗 Architecture

The system is designed with a decoupled architecture for scalability:

1.  **Ingestion Pipeline (`ingestion.py`):**
    * Extracts text from PDF technical manuals.
    * Splits text into semantic chunks (500 chars).
    * Generates embeddings using `sentence-transformers/paraphrase-multilingual`.
    * Stores vectors in **ChromaDB**.

2.  **Inference Engine (`app.py`):**
    * Retrieves top-3 relevant chunks via Semantic Search.
    * Generates answers using **Llama 3.3 (70B)** via Groq API.
    * Strict prompt engineering to enforce factual accuracy.

3.  **Frontend (`ui.py`):**
    * Built with **Streamlit** for a reactive user interface.
    * Displays sources/citations for transparency.

## 🛠 Tech Stack

* **LLM:** Llama 3.3-70b-versatile (via Groq)
* **Embeddings:** HuggingFace (Open Source & Local)
* **Vector DB:** ChromaDB
* **Orchestration:** LangChain
* **Containerization:** Docker
* **Language:** Python 3.11

## 🚀 How to Run

### Option A: Using Docker (Recommended)

This ensures the application runs exactly as intended, regardless of your OS.

1. **Build the image:**
   ```bash
   docker build -t rag-assistant-app .

2. **Run the container: (Replace your_key with your actual Groq API Key)**

   docker run -e GROQ_API_KEY="your_key_here" -p 8501:8501 rag-assistant-app 

3. **Access the App: Open http://localhost:8501 in your browser.** 