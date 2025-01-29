# Use official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Upgrade pip & install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Ensure correct permissions for SQLite database (If using SQLite)
RUN chmod -R 777 /app

# Run the application
CMD ["python", "app.py"]