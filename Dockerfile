FROM python:3.13

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    cmake \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY transcription_app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY /transcription_app .

# Set environment variables
ENV PORT=7860

# Expose the port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]