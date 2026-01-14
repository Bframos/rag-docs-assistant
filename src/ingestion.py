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
    print(f"🔄 A iniciar ingestão do ficheiro: {file_path}") # LOG

    # 1. Limpar Base de Dados antiga
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # 2. Carregar o PDF
    try:
        loader = PyPDFLoader(file_path)
        raw_documents = loader.load()
        print(f"📄 Páginas carregadas: {len(raw_documents)}") # LOG
    except Exception as e:
        print(f"❌ Erro ao ler o PDF: {e}")
        return False

    if not raw_documents:
        print("⚠️ O PDF parece estar vazio ou ilegível.")
        return False

    # 3. Dividir em chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "!", "?", ",", " "],
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(raw_documents)
    print(f"🧩 Chunks criados: {len(chunks)}") # LOG

    # --- O CHECK DE SEGURANÇA ---
    if len(chunks) == 0:
        print("⛔ ERRO CRÍTICO: Nenhum texto foi extraído. O PDF pode ser uma imagem digitalizada?")
        return False
    # ---------------------------

    # 4. Criar Embeddings e guardar
    print("🧠 A gerar embeddings (isto pode demorar um pouco)...")
    try:
        hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        
        Chroma.from_documents(
            documents=chunks,
            embedding=hf_embeddings,
            persist_directory=CHROMA_PATH
        )
        print("✅ Ingestão concluída com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro no ChromaDB: {e}")
        return False