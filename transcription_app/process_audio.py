import os
import sys
import logging
import json
from openai import OpenAI
from dotenv import load_dotenv
from summary_agent import response

load_dotenv()
logging.basicConfig(level=logging.ERROR)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SUMMARY_AGENT = os.getenv('SUMMARY_AGENT')

if not OPENAI_API_KEY: 
    logging.error(f"Missing required environment variables: {sys.exit(1)}")

def transcribe_audio(filepath):
    client = OpenAI(api_key=OPENAI_API_KEY)
    audio_file= open(filepath, "rb")

    whisper_file_path = os.path.join('output/whisper', 'whisper_transcript.json')
    transcript_output = os.path.join('output/transcripts', 'transcript.json')

    final_transcript = {
        "summary": response.output_text,
        "transcript_segments": []
    }

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
        final_transcript["transcript_segments"] = transcription_segments

        with open(whisper_file_path, "w") as f:
            json.dump(transcription_segments, f, indent=4)
        with open(transcript_output, "w") as f:
            json.dump(final_transcript, f, indent=4)
        return whisper_file_path
    except Exception as e:
        logging.error(e)
        return "An unexpected error occurred"