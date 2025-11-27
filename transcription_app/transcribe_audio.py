import os
import sys
import logging
import json
import subprocess
import glob
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.ERROR)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    logging.error(f"Missing required environment variables: {sys.exit(1)}")

def transcribe_audio(filepath):
    client = OpenAI(api_key=OPENAI_API_KEY)
    whisper_filepath = os.path.join('output/whisper', 'whisper_transcript.json')
    os.makedirs('output/whisper', exist_ok=True)
    
    temp_dir = 'temp_segments'
    os.makedirs(temp_dir, exist_ok=True)

    result = subprocess.run([
        'ffmpeg', '-i', filepath,
        '-f', 'segment', '-segment_time', '900',
        '-c:a', 'aac', '-b:a', '32k',
        '-vn',
        os.path.join(temp_dir, 'segment_%03d.m4a')
    ], capture_output=True, text=True)

    if result.returncode != 0:
        logging.error(f"Segmentation failed: {result.stderr}")
        raise Exception(f"FFmpeg segmentation error: {result.stderr}")

    try:
        for segment in sorted(glob.glob(os.path.join(temp_dir, 'segment_*.m4a'))):
            print(f"  Transcribing {os.path.basename(segment)}...")
            with open(segment, 'rb') as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file, 
                    response_format="verbose_json",
                    timestamp_granularities="segment"
                )
                transcription_segments = []
                segment_id = 1
                for seg in transcription.segments:
                    transcription_data = {
                        "id": segment_id,
                        "start": round(seg.start, 2),
                        "end": round(seg.end, 2),
                        "text": seg.text
                    }
                    transcription_segments.append(transcription_data)
                    segment_id += 1
            os.remove(segment)
        
        os.rmdir(temp_dir)
        
        with open(whisper_filepath, "w") as f:
            json.dump(transcription_segments, f, indent=4)
        return transcription_segments
    except Exception as e:
        logging.error(f"Audio processing failed for {filepath}: {e}")
        return f"Audio processing error: {e}"