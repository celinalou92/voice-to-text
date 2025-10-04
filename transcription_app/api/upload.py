import os
from flask import Blueprint, request, jsonify, redirect, url_for
from transcribe_audio import transcribe_audio
from diarization_service import identify_speakers 
from transcript_response import transcription_response
from summary_agent import generate_summary
from util import format_audio

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    audio_file = request.files['audio']
    filepath = os.path.join('uploads', audio_file.filename)
    audio_file.save(filepath)
    wav_file = format_audio.audio_to_wav(filepath)

    print("\n👨‍💻 Processing Audio....")
    print(f"    ... Transcribing Summary...")
    transcript_data = transcribe_audio(wav_file)
    print(f"    ✅ Transcription Complete!")

    print(f"    ... Generating Summary...")
    summary_data = generate_summary(transcript_data)
    print(f"    ✅ Summary Complete!")

    print("     ... Diaritzation....")
    speaker_data = identify_speakers(wav_file)
    print(f"    ✅ Diaritzation Complete!")

    transcription_response(transcript_data, summary_data, speaker_data)
    print(f"✅ Processing Audio Complete!")

    return redirect(url_for('index'))