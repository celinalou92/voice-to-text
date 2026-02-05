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
    logging.error(f"Missing required environment variables: {sys.exit(1)}")

def transcribe_audio(filepath):
    client = OpenAI(api_key=OPENAI_API_KEY)
    print(f"    ... Transcribing...")
    try:
        with open(filepath, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-transcribe-diarize", 
                file=audio_file, 
                response_format="diarized_json",
                chunking_strategy="auto"
            )
        print(f"    ... ✅ Transcription Complete...")
        return transcript
    except ValueError as e:
        logging.error(f"Validation error: {e}")
        return {'error': str(e)}, 400
    except RateLimitError as e:
        logging.error(f"Rate limited: {e}")
        return {'error': 'API rate limit exceeded. Try again later.'}, 429
    except APIConnectionError as e:
        logging.error(f"Connection error: {e}")
        return {'error': 'Failed to connect to OpenAI'}, 503
    except APIStatusError as e:
        logging.error(f"API error: {e.status_code} - {e.message}")
        return {'error': f'OpenAI API error: {e.message}'}, 502
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {'error': 'Internal server error'}, 500