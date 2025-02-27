import os
import sys
import logging
import json
from pydub import AudioSegment
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.ERROR)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')


if not OPENAI_API_KEY or not HUGGINGFACE_TOKEN: 
    logging.error(f"Missing required environment variables: {sys.exit(1)}")

def transcribe_audio(filepath):
    client = OpenAI(api_key=OPENAI_API_KEY)
    audio_file= open(filepath, "rb")
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
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text
            }
            transcription_segments.append(transcription_data)
        return transcription_segments
    except Exception as e:
        logging.error(e)
        return "An unexpected error occurred"
    
def identify_speakers(filepath, extracted_audio_file):    
    audio = AudioSegment.from_file(filepath, format="m4a")
    audio.export(extracted_audio_file, format="wav")

    wav_file = open(extracted_audio_file, "rb")
    
    pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization-3.1', use_auth_token=HUGGINGFACE_TOKEN)
    
    with ProgressHook() as hook:
        diarization = pipeline(wav_file, hook=hook)

    diarization_output = os.path.join('output/diarization', 'diarization_output.json')

    speaker_segments = []
    with open(diarization_output, 'w') as f:
        for segment, _, speaker in diarization.itertracks(yield_label=True):
            speaker_data = {
                "speaker": speaker,
                "start": round(segment.start, 2),
                "end": round(segment.end, 2)
            }
            speaker_segments.append(speaker_data)
        json.dump(speaker_segments, f, indent=4)
    
    return ["Speaker 1", "Speaker 2"]