# Use a slim Python 3.11 image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (Tesseract OCR for forensic image scanning)
# Clean up apt cache to keep the image size small
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements first to leverage Docker's layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY config/ config/
COPY core/ core/
COPY frontend/ frontend/
COPY utils/ utils/

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the application
CMD ["python", "-m", "streamlit", "run", "frontend/app.py", "--server.headless", "true", "--server.port", "8501", "--server.address", "0.0.0.0"]