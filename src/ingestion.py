import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_chroma import Chroma

#######
# Data Ingestion Script

load_dotenv()

DATA_PATH = "data/OGCombo2EssentialEMEAptPT.pdf"
CHROMA_PATH = "chroma_db"

def ingest_documents():
    if not os.path.exists(DATA_PATH):
        print(f"❌ Erro: O ficheiro '{DATA_PATH}' não foi encontrado.")
        return

    print("📄 A carregar o PDF...")
    loader = PyPDFLoader(DATA_PATH)
    raw_documents = loader.load()
    print(f"   -> Carregadas {len(raw_documents)} páginas.")


    print("✂️  A dividir o texto em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # Reduzimos de 1000 para 500
        chunk_overlap=50,    # Reduzimos o overlap para 50
        separators=["\n\n", "\n", ".", "!", "?", ",", " "], # Força a quebra em frases lógicas
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(raw_documents)
    print(f"   -> Criados {len(chunks)} chunks de texto.")

    print("💾 A criar Embeddings (HuggingFace) e a guardar no ChromaDB...")
    
    if os.path.exists(CHROMA_PATH):
        import shutil
        shutil.rmtree(CHROMA_PATH)

    # MUDANÇA 2: Usar um modelo pequeno e rápido que corre no CPU
    hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=hf_embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print(f"✅ Sucesso! Base de dados criada em '{CHROMA_PATH}'.")

if __name__ == "__main__":
    ingest_documents()