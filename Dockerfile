# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files from your folder into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt || true

# Expose port (for web apps)
EXPOSE 8501

# Default command to run the main file
CMD ["python", "main.py"]
