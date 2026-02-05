import os
import logging
from flask import Blueprint, request, jsonify, app, redirect, url_for
from whisper_transcribe_audio import transcribe_audio
from transcript_response import transcription_response
from summary_service import generate_summary

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_audio():
    ## invalid upload, no upload, wrong file type, too big
    audio_file = request.files.get('audio')
    print(f"Content-Length: {request.content_length}")
    print(f"Content-Type: {request.content_type}")
    print(f"Files: {request.files}")
    print(f"Form data: {request.form}")
    if not audio_file or audio_file.filename == '':
        return {'error': 'No file provided'}, 400
    if not audio_file.filename.endswith(('.wav', '.mp3', '.m4a', '.mp4')):
        return {'error': 'Invalid file type. Allowed: wav, mp3, m4a, mp4'}
    if request.content_length and request.content_length > 100 * 1024 * 1024:
        return {'error': 'File too large. Max 100MB'}
    filepath = os.path.join('uploads', audio_file.filename)
    audio_file.save(filepath)

    try:
        print("\n👨‍💻 Processing Audio....")
        whisper_response = transcribe_audio(filepath)
              
        
        # if whisper_response[1] >= 400:
        #     return jsonify({'error': whisper_response[0]['error'], 'status_code': whisper_response[1]})
        
        summary_response = generate_summary(whisper_response)
        ## bad whisper or summary response - exit

        if summary_response[1] >= 400:
            return jsonify({'error': summary_response[0]['error'], 'status_code': summary_response[1]})
        # transcription_response(whisper_response, summary_response)

        print(f"✅ Processing Audio Complete!")

        # redirect(url_for('index'))
    except Exception as e:
        logging.error(f"File upload error: {e}")
        
        return jsonify({'error': 'Server Error:', 'status_code': 502})
    

# @app.errorhandler(400)
# def bad_request(e):
#     return {"error": "Invalid request", "details": str(e)}, 400

# @app.errorhandler(500)
# def server_error(e):
#     app.logger.error(f"Unhandled error: {e}", exc_info=True)
#     return {"error": "Internal server error"}, 500