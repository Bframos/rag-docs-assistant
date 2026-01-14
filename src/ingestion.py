import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "chroma_db"

def ingest_file(file_path):
    """
    Recebe o caminho de um ficheiro PDF, limpa a BD antiga e cria uma nova.
    """
    # 1. Limpar Base de Dados antiga (se existir)
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # 2. Carregar o PDF novo
    loader = PyPDFLoader(file_path)
    raw_documents = loader.load()
    
    # 3. Dividir em chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "!", "?", ",", " "],
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(raw_documents)

    # 4. Criar Embeddings e guardar
    hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    
    Chroma.from_documents(
        documents=chunks,
        embedding=hf_embeddings,
        persist_directory=CHROMA_PATH
    )
    
    return True


