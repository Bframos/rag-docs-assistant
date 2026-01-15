import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load vars
load_dotenv()

CHROMA_PATH = "chroma_db"


def query_rag(query_text):
    
    # 1. Load embedding function and vector DB
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # 2. Search
    results = db.similarity_search(query_text, k=3)
    if not results:
        return "Sorry, i did not find any information in the manual.", []

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])

    prompt_template = ChatPromptTemplate.from_template("""
    You are a technical assistant specialist. Answer the question based SOLELY on the context provided below:
    <context>
    {context}
    </context>
    Question from the user: {question}
    If the answer is not in the context, just say "I did not find that information in the manual".
    """)

    # 3. Generate
    model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    chain = prompt_template | model
    response = chain.invoke({"context": context_text, "question": query_text})
    
    return response.content, results
