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

COPY requirements.txt .

# 1. Atualizar pip
RUN pip install --no-cache-dir --upgrade pip

# 2. Instalar PyTorch versão CPU (Isto poupa 4GB!)
# É CRUCIAL que isto corra ANTES do requirements.txt
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 3. Instalar o resto
RUN pip install --no-cache-dir -r requirements.txt


# 6. Copiar o código
COPY src/ src/

