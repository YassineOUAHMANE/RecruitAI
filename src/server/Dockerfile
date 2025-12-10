FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create entrypoint script that initializes Qdrant then starts API
RUN echo '#!/bin/bash\nset -e\nexport PYTHONPATH=/app:$PYTHONPATH\necho "Initializing Qdrant collection..."\npython -m ml_pipeline.ingest || echo "Qdrant collection init skipped (already exists or error)"\necho "Starting API server..."\nexec uvicorn backend.main:app --host 0.0.0.0 --port 8000' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
