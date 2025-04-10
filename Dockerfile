FROM python:3.11-slim

# Install yt-dlp & Node.js
RUN apt-get update && apt-get install -y \
    nodejs npm ffmpeg curl && \
    pip install yt-dlp fastapi uvicorn && \
    npm install -g serve && \
    apt-get clean

# Copy backend
WORKDIR /app
COPY backend ./backend
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy frontend build
COPY frontend/build ./frontend/build

# Create download dir
RUN mkdir downloads

# Start both frontend and backend
CMD uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
CMD serve -s frontend/build -l 3000