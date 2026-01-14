from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil
from src.ingestion import ingest_file
from src.app import query_rag

app = FastAPI(title="RAG API")

# Modelo de dados para a pergunta
class QueryRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"status": "API is running 🚀"}

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Recebe um ficheiro PDF e processa-o para o ChromaDB.
    """
    try:
        # Salvar o ficheiro temporariamente
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Correr a função de ingestão que já criámos
        success = ingest_file(file_path)
        
        if success:
            return {"message": "Documento processado com sucesso!", "filename": file.filename}
        else:
            raise HTTPException(status_code=500, detail="Erro na ingestão")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_endpoint(request: QueryRequest):
    """
    Recebe uma pergunta e devolve a resposta do LLM.
    """
    try:
        response_text, sources = query_rag(request.query)
        
        # Formatar as fontes para JSON
        sources_json = [
            {"content": doc.page_content, "page": doc.metadata.get("page_label")} 
            for doc in sources
        ]
        
        return {
            "response": response_text,
            "sources": sources_json
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))