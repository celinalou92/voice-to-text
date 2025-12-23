import os
import sys
import logging
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.ERROR)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    logging.error(f"Missing required environment variables: {sys.exit(1)}")

def transcribe_audio(filepath):
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        with open(filepath, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-transcribe-diarize", 
                file=audio_file, 
                response_format="diarized_json",
                chunking_strategy="auto"
            )
        return transcript
    except Exception as e:
        logging.error(f"Transcription processing error: {e}")
        return f"Transcription processing error: {e}"