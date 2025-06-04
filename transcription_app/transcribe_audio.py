import os
import sys
import logging
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.ERROR)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY: 
    logging.error(f"Missing required environment variables: {sys.exit(1)}")

def transcribe_audio(filepath):
    client = OpenAI(api_key=OPENAI_API_KEY)
    audio_file= open(filepath, "rb")
    whisper_filepath = os.path.join('output/whisper', 'whisper_transcript.json')

    try:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="verbose_json",
            timestamp_granularities="segment"
        )
        transcription_segments = []
        
        for segment in transcription.segments:
            transcription_data = {
                "id": segment.id,
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text
            }
            transcription_segments.append(transcription_data)
        with open(whisper_filepath, "w") as f:
            json.dump(transcription_segments, f, indent=4)
        return transcription_segments
    except Exception as e:
        logging.error(f"Audio processing failed for {filepath}: {e}")
        return f"Audio processing error: {e}"