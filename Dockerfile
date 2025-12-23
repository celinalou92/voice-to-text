FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . $HOME/app

RUN mkdir -p uploads \
    output/transcripts

ENV PORT=7860

EXPOSE 7860

CMD ["python", "app.py"]