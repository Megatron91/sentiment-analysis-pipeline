# Use the official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (gcc and others)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    build-essential \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
