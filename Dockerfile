# 1. Imagem Base (Python leve)
FROM python:3.11-slim

# 2. Definir pasta de trabalho
WORKDIR /app

# --- NOVO BLOCO DE CORREÇÃO ---
# 3. Instalar dependências de sistema (Compiladores C++)
# Isto é obrigatório para bibliotecas de IA como ChromaDB e Numpy
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*
# ------------------------------

# 4. Copiar requirements
COPY requirements.txt .

# 5. Instalar dependências de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copiar o código
COPY src/ src/

