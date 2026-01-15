from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil
from src.ingestion import ingest_file
from src.app import query_rag

app = FastAPI(title="RAG API")

# Model for the chat request
class QueryRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"status": "API is running 🚀"}

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Receives a document file and processes it for ingestion.
    """
    try:
        # Save the uploaded file to a temporary location
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Run the ingestion process
        success = ingest_file(file_path)
        
        if success:
            return {"message": "Document processed successfully!", "filename": file.filename}
        else:
            raise HTTPException(status_code=500, detail="Error processing document.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_endpoint(request: QueryRequest):
    """
    Receives a query and returns a response along with source documents.
    """
    try:
        response_text, sources = query_rag(request.query)
        
        # format sources for JSON response
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