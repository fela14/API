FROM python:3.10-slim-bullseye

# Install system dependencies (required for moviepy, ffmpeg, bcrypt, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        build-essential \
        python3-dev \
        libffi-dev \
        pkg-config \
        git \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (cache layer)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Default command
CMD ["python3", "consumer.py"]
