FROM python:3.10-slim-bullseye

# Install system dependencies for MySQL client
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Copy and install dependencies first for caching
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the app
COPY . /app

# Expose Flask port
EXPOSE 5000

# Start the Flask server
CMD ["python3", "server.py"]
