import os
import logging
import json
import torch
import sys
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.ERROR)


def identify_speakers(filepath): 
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')
    if not  HUGGINGFACE_TOKEN: 
        logging.error(f"Missing required environment variables: {sys.exit(1)}")
    extracted_audio_file = os.path.join('output/conversion_wav', 'conversion.wav')
    diarization_filepath = os.path.join('output/diarization', 'diarization_output.json')

    try:
        audio = AudioSegment.from_file(filepath, format="m4a")
        audio.export(extracted_audio_file, format="wav")
        wav_file = open(extracted_audio_file, "rb")
        pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization-3.1', use_auth_token=HUGGINGFACE_TOKEN)
        if torch.cuda.is_available():
            pipeline.to("cuda")
        else:
            print("Warning: CUDA not available, running on CPU")
        with ProgressHook() as hook:
            diarization = pipeline(wav_file, hook=hook)

        speaker_segments = []
        with open(diarization_filepath, 'w') as f:
            for segment, _, speaker in diarization.itertracks(yield_label=True):
                speaker_data = {
                    "speaker": speaker,
                    "start": round(segment.start, 2),
                    "end": round(segment.end, 2)
                }
                speaker_segments.append(speaker_data)
            json.dump(speaker_segments, f, indent=4)
            
        return speaker_segments
    except Exception as e:
     logging.error(e)
    return f"An unexpected error occurred {e}"