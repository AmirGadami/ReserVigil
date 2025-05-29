# Force AMD64 architecture (required for Cloud Run)
FROM --platform=linux/amd64 python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install system dependencies (LightGBM + Streamlit requirements)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining files
COPY . .

# Install in editable mode (if needed)
RUN pip install --no-cache-dir -e .

# Training pipeline (if static, else move to CMD)
RUN python pipeline/training_pipeline.py

EXPOSE $PORT

# Streamlit with production tweaks
CMD ["sh", "-c", "streamlit run application.py \
    --server.port=$PORT \
    --server.enableCORS=false \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false"]