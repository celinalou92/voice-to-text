import os
import sys
import json
import logging
from openai import OpenAI, APIError, APIConnectionError, RateLimitError, APIStatusError
from dotenv import load_dotenv
load_dotenv()
logging.basicConfiglevel=logging.ERROR

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    logging.error(f"Missing required environment variable: OPEN_API_KEY")
    {sys.exit(1)}

def transcribe_audio(filepath):
    client = OpenAI(api_key=OPENAI_API_KEY)

    print(f"    ... Transcribing...")
    
    with open(filepath, 'rb') as audio_file:
        try:   
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-transcribe-diarize", 
                file=audio_file, 
                response_format="diarized_json",
                chunking_strategy="auto"
            )
            print(f"    ... ✅ Transcription Complete...")
            return transcript
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return {'error': 'Internal server error'}, 500