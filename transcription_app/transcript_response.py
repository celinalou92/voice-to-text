import json
import os
import logging
from datetime import timedelta

def transcription_response(whisper_response, summary_response):
    transcript_file = os.path.join('output/transcripts', 'transcript.json')
    try:
        transcription_segments = []
        for segment in whisper_response.segments:
            start_time = str(timedelta(seconds=segment["start"])).split('.')[0]
            end_time = str(timedelta(seconds=segment["end"])).split('.')[0]
            
            transcription_data = {
                "id": segment["id"],
                "start": start_time,
                "end": end_time,
                "speaker": segment["speaker"],
                "text": segment["text"]
            }
            transcription_segments.append(transcription_data)

        final_transcript = {
            "summary": json.loads(summary_response.output_text),
            "segments": transcription_segments
        }

        with open(transcript_file, "w") as f:
            json.dump(final_transcript, f, indent=4)
        return final_transcript
    except Exception as e:
        logging.error(e)
        return f"Transcription Response error: {e}"

