# Base image
FROM python:3.10-slim-bullseye

# Install system dependencies needed for bcrypt and general compilation
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libffi-dev \
        pkg-config \
        git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app

# Expose gateway port
EXPOSE 8080

# Run the Flask server
CMD ["python3", "server.py"]
