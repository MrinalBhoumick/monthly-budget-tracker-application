# Use official slim Python 3.12 image
FROM python:3.12-slim

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libpq-dev \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Streamlit environment configuration
ENV STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=80 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose Streamlit's default port
EXPOSE 80

# Start the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]
