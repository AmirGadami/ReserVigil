# Use a lightweight Python image
FROM python:slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \  
    PIP_NO_CACHE_DIR=1  

# Set the working directory
WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

RUN pip install --no-cache-dir -e .

RUN python pipeline/training_pipeline.py

EXPOSE $PORT

CMD ["sh", "-c", "streamlit run application.py --server.port=$PORT --server.enableCORS=false --server.address=0.0.0.0"]