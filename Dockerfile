# 1. Imagem Base: Usamos uma versão leve do Python (Slim)
# Python 3.10 ou 3.11 são os mais estáveis para AI hoje.
FROM python:3.11-slim

# 2. Definir variáveis de ambiente para o Python não criar ficheiros .pyc
# e para veres os logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Criar a pasta de trabalho dentro do container
WORKDIR /app

# 4. Instalar dependências do sistema operativo
# (Necessário para compilar algumas libs de C++ usadas pelo ChromaDB)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar e instalar as dependências de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar o código todo do projeto para dentro do container
COPY . .

# 7. Expor a porta que o Streamlit usa
EXPOSE 8501

# 8. O comando que corre quando o container arranca
CMD ["streamlit", "run", "src/ui.py", "--server.address=0.0.0.0"]