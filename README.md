# 🤖 Intelligent Tech Support Agent (RAG) - Microservices Edition

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)
![Docker Compose](https://img.shields.io/badge/Orchestration-Docker%20Compose-2496ED)
![AI](https://img.shields.io/badge/LLM-Llama%203.3-orange)
![CI Pipeline](https://github.com/bframos/rag-docs-assistant/actions/workflows/ci-pipeline.yml/badge.svg)


An AI-powered Technical Support Assistant architected as a **Microservices Application**. It uses **RAG (Retrieval-Augmented Generation)** to answer questions based on any uploaded PDF manual.

## 🏗 Architecture

The system is decoupled into two containers orchestrated by Docker Compose:

1.  **Backend Service (`api.py`):**
    * **Framework:** FastAPI (High-performance Async API).
    * **Responsibility:** Handles PDF ingestion, Chunking, Vectorization (ChromaDB), and LLM Inference (Llama 3.3 via Groq).
    * **Endpoints:** `/ingest` (Upload) and `/chat` (Q&A).

2.  **Frontend Service (`ui.py`):**
    * **Framework:** Streamlit.
    * **Responsibility:** User Interface.
    * **Communication:** Sends HTTP requests to the Backend API via the internal Docker network (`http://backend:8000`).

## 🛠 Tech Stack

* **Orchestration:** Docker Compose
* **LLM:** Llama 3.3-70b-versatile (Groq API)
* **Vector DB:** ChromaDB (Persistent Volume)
* **CI/CD:** GitHub Actions (Automated Build Pipeline) 
* **Embeddings:** HuggingFace `paraphrase-multilingual`
* **Language:** Python 3.11

## 🚀 How to Run (The Magic Command)

### Prerequisites
* Docker & Docker Compose installed.
* A Groq API Key.

### Steps

1.  **Clone and Configure:**
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_key_here
    ```

2.  **Launch the Stack:**
    This command builds both images and establishes the internal network.
    ```bash
    docker-compose up --build
    ```

3.  **Access the App:**
    * **Frontend:** Open `http://localhost:8501` to chat.
    * **API Docs:** Open `http://localhost:8000/docs` to test endpoints directly.

