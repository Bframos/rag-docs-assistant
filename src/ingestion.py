import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "chroma_db"

def ingest_file(file_path):
    """
    Receives a file path to a PDF document, processes it, and ingests it into the Chroma vector database.
    Returns True if successful, False otherwise.
    """
    print(f"🔄 Processing file: {file_path}") # LOG

    # 1. Clean previous DB
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # 2. Load PDF
    try:
        loader = PyPDFLoader(file_path)
        raw_documents = loader.load()
        print(f"📄 Pages loaded: {len(raw_documents)}") # LOG
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return False

    if not raw_documents:
        print("⚠️ PDF appears to be empty or illegible.")
        return False

    # 3. Divide into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "!", "?", ",", " "],
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(raw_documents)
    print(f"🧩 Chunks created: {len(chunks)}") # LOG

    # --- Safety check ---  
    if len(chunks) == 0:
        print("⛔ CRITICAL ERROR: No text was extracted. The PDF might be a scanned image?")
        return False


    # 4. Create Embeddings and store in ChromaDB
    print("🧠 Generating embeddings (this may take a while)...")
    try:
        hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        
        Chroma.from_documents(
            documents=chunks,
            embedding=hf_embeddings,
            persist_directory=CHROMA_PATH
        )
        print("✅ Ingestion completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error in ChromaDB: {e}")
        return False