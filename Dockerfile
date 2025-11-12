# -----------------------------
# Base Image
# -----------------------------
FROM python:3.11-slim

# Avoid prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# -----------------------------
# Copy requirements and install dependencies
# -----------------------------
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    git \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Copy your app code
# -----------------------------
COPY . .

# -----------------------------
# Streamlit configuration (optional)
# -----------------------------
EXPOSE 8501

# To avoid Streamlit asking for email/config
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_PORT=8501

# -----------------------------
# Command to run app
# -----------------------------
CMD ["streamlit", "run", "app.py"]
