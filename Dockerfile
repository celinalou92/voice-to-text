FROM python:3.13

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    cmake \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*
    
# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY transcription_app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=user /transcription_app $HOME/app

RUN --mount=type=secret,id=OPENAI_API_KEY,mode=0444,required=true,env=OPENAI_API_KEY \ --mount=type=secret,id=SUMMARY_AGENT,mode=0444,required=true,env=SUMMARY_AGENT \ --mount=type=secret,id=HUGGINGFACE_TOKEN,mode=0444,required=true,env=HUGGINGFACE_TOKEN

# Set environment variables
ENV PORT=7860

# Expose the port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]