FROM python:3.11-slim

# UPGRADE: Create a non-root user for enterprise security constraints
RUN adduser --disabled-password --gecos '' vaultuser

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config/ config/
COPY core/ core/
COPY frontend/ frontend/
COPY utils/ utils/

# UPGRADE: Transfer ownership to the secure user and switch context
RUN chown -R vaultuser:vaultuser /app
USER vaultuser

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "frontend/app.py", "--server.headless", "true", "--server.port", "8501", "--server.address", "0.0.0.0"]