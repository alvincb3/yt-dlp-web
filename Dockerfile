FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add backend code
COPY backend /app/backend

# Add built React frontend
COPY frontend/build /app/frontend/build

# Create directory for downloads
RUN mkdir -p /app/downloads
WORKDIR /app

# Expose the FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
