# Force AMD64 architecture
FROM --platform=linux/amd64 python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 && \
    rm -rf /var/lib/apt/lists/*

COPY . .


RUN pip install --no-cache-dir -e .


RUN python pipeline/training_pipeline.py

EXPOSE $PORT
CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.enableCORS=false --server.headless=true"]