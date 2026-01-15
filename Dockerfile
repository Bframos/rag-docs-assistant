# 1. Base image
FROM python:3.11-slim

# 2. working directory
WORKDIR /app

# 3. Dependencies (Compiladores C++)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements
COPY requirements.txt .

# 5. Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# 6. Download pytorch cpu version (Saves 4GB!)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 7. Install the rest of dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 8. Copy source code
COPY src/ src/

