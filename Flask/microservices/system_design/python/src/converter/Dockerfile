# Use official Python 3.10 slim image
FROM python:3.10-slim-bullseye

# ----------------------------
# Install system dependencies
# ----------------------------
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
        curl \
        wget \
        libsm6 \
        libxext6 \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Set working directory
# ----------------------------
WORKDIR /app

# ----------------------------
# Copy requirements first for caching
# ----------------------------
COPY requirements.txt .

# ----------------------------
# Upgrade pip and install Python packages
# ----------------------------
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ----------------------------
# Copy the rest of the application
# ----------------------------
COPY . .

# ----------------------------
# Default command to run converter
# ----------------------------
CMD ["python3", "consumer.py"]
