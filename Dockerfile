FROM --platform=linux/amd64 python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker caching
COPY requirements.txt .

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project
COPY . .

# Set entry point
CMD ["python", "app/main.py"]
