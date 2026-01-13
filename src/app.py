import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Carregar variáveis
load_dotenv()

CHROMA_PATH = "chroma_db"


def query_rag(query_text):
    
    # 1. Preparar a BD
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # 2. Pesquisar
    results = db.similarity_search(query_text, k=3)
    if not results:
        return "Desculpa, não encontrei informação suficiente no manual.", []

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])

    prompt_template = ChatPromptTemplate.from_template("""
    És um assistente técnico especializado. Responde à pergunta baseando-te APENAS no contexto fornecido abaixo:
    <contexto>
    {context}
    </contexto>
    Pergunta do utilizador: {question}
    Se a resposta não estiver no contexto, diz apenas "Não encontrei essa informação no manual".
    """)

    # 3. Gerar
    model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    chain = prompt_template | model
    response = chain.invoke({"context": context_text, "question": query_text})
    
    return response.content, results
