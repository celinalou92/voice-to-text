import os
import sys
import logging
from pydub import AudioSegment
from pyannote.audio import Pipeline
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
    # try:
    #     transcription = client.audio.transcriptions.create(
    #         model="whisper-1", 
    #         file=audio_file, 
    #         response_format="verbose_json",
    #         timestamp_granularities="segment"
    #     )
    #     return transcription
    # except Exception as e:
    #     logging.error(e)
    #     return "An unexpected error occurred"

    with open('transcript_segment_data.json', 'r') as f:
        return f.read()
    
    
def extract_key_points(transcript):
    from collections import Counter
    words = transcript.lower().split()
    counter = Counter(words)
    return counter.most_common(3)

def identify_speakers(filepath, extracted_audio_file):    
    audio = AudioSegment.from_file(filepath, format="m4a")
    audio.export(extracted_audio_file, format="wav")

    # pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization@2.1', use_auth_token=HUGGINGFACE_TOKEN)
    # diarization = pipeline(output_file)

    # for segment, _, speaker in diarization.itertracks(yield_label=True):
    #    print(f"Speaker {speaker} speaks from {segment.start:.2f} to {segment.end:.2f} seconds.")
    
    return ["Speaker 1", "Speaker 2"]