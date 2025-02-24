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
        
client = OpenAI(api_key=OPENAI_API_KEY)

def process_audio(filepath):
    audio_file= open(filepath, "rb")
    try:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )
        return transcription
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error occurred: {e}")
        return "An unexpected error occurred"
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred"
    
    
def extract_key_points(transcript):
    from collections import Counter
    words = transcript.lower().split()
    counter = Counter(words)
    return counter.most_common(3)

def identify_speakers(filepath):
    return ["Speaker 1", "Speaker 2"]