
FROM python:3.13

RUN useradd -m -u 1000 user

USER user

ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    cmake \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*
    
COPY --chown=user . $HOME/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . $HOME/app

ENV PORT=7860

EXPOSE 7860

RUN --mount=type=secret,id=SUMMARY_AGENT, mode=0444,required=true, env=SUMMARY_AGENT\
--mount=type=secret,id=HUGGINGFACE_TOKEN, mode=0444,required=true, env=HUGGINGFACE_TOKEN\
--mount=type=secret,id=OPENAI_API_KEY, mode=0444,required=true, env=OPENAI_API_KEY\
 git init && \
 git remote add origin $(cat /run/secrets/SUMMARY_AGENT) \
 git remote add origin $(cat /run/secrets/HUGGINGFACE_TOKEN) \
 git remote add origin $(cat /run/secrets/OPENAI_API_KEY)

CMD ["python", "app.py"]