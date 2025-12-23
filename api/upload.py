import os
from flask import Blueprint, request, jsonify, redirect, url_for
from whisper_transcribe_audio import transcribe_audio
from transcript_response import transcription_response
from summary_service import generate_summary

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    audio_file = request.files['audio']
    filepath = os.path.join('uploads', audio_file.filename)
    audio_file.save(filepath)

    print("\n👨‍💻 Processing Audio....")
    
    whisper_response = transcribe_audio(filepath)
    summary_response = generate_summary(whisper_response)
    
    transcription_response(whisper_response, summary_response)

    print(f"✅ Processing Audio Complete!")

    return redirect(url_for('index'))