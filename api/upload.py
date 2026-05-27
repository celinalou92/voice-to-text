import os
import logging
from flask import Blueprint, request, jsonify, redirect, url_for
from whisper_transcribe_audio import transcribe_audio
from transcript_response import transcription_response
from summary_service import generate_summary
from yt_download import yt_download

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_audio():
    if request.form:
        filepath = yt_download(request.form.get('link'), 'uploads')
    else:
        audio_file = request.files.get('audio')
        filepath = os.path.join('uploads', audio_file.filename)
        audio_file.save(filepath)

    try:
        print("\n👨‍💻 Processing Audio....")
        whisper_response = transcribe_audio(filepath)
        summary_response = generate_summary(whisper_response)
        transcription_response(whisper_response, summary_response)

        print(f"✅ Processing Audio Complete!")

        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"File upload error: {e}")
        return jsonify({'error': 'Server Error:', 'status_code': 502})