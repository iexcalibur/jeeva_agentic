FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations on startup
CMD ["sh", "-c", "python scripts/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

