import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
from process_audio import transcribe_audio, identify_speakers

app = Flask(__name__)

os.makedirs('uploads', exist_ok=True)
os.makedirs('output', exist_ok=True)

@app.route('/')
def index():
    transcript_file = os.path.join('output/transcripts', 'transcript.json')
    transcript = None
    if os.path.exists(transcript_file):
        with open(transcript_file, 'r') as f:
            transcript = f.read()
    return render_template('index.html', transcript=transcript)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    audio_file = request.files['audio']
    filepath = os.path.join('uploads', audio_file.filename)
    audio_file.save(filepath)
    
    extracted_audio_file = os.path.join('output/conversion_wav', 'conversion.wav')
    
    transcript = transcribe_audio(filepath)
    speakers = identify_speakers(filepath, extracted_audio_file)

    transcript_file = os.path.join('output/transcripts', 'transcript.json')
    with open(transcript_file, 'w') as f:
        json.dump(transcript, f, indent=4)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)