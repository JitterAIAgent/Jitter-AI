# Dockerfile for Python FastAPI backend only
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application files
COPY main.py .
COPY core/ ./core/
COPY parsers/ ./parsers/
COPY tasks/ ./tasks/
COPY utils/ ./utils/
COPY rag/ ./rag/
COPY memory/ ./memory/
COPY *.py ./
COPY *.json ./
COPY .env* ./

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]