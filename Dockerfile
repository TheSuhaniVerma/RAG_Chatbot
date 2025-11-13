FROM python:3.11-slim

# Avoid prompts during install
ENV DEBIAN_FRONTEND=noninteractive

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
# Streamlit configuration
# -----------------------------
EXPOSE 8501

ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_PORT=8501

# -----------------------------
# Run Streamlit
# -----------------------------
CMD ["streamlit", "run", "app.py"]