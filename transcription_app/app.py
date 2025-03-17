import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
from process_audio import transcribe_audio, identify_speakers 
from transcript_response import parse

app = Flask(__name__)

os.makedirs('uploads', exist_ok=True)
os.makedirs('output', exist_ok=True)

@app.route('/')
def index():
    transcript_file = os.path.join('output/transcripts', 'transcript.json')
    transcript = None
    
    if os.path.exists(transcript_file):
        transcript = load_json(transcript_file)

    return render_template('index.html', transcript=transcript)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    audio_file = request.files['audio']
    filepath = os.path.join('uploads', audio_file.filename)
    audio_file.save(filepath)
    
    
    print("👨‍💻 Whisper....")
    transcript_data = transcribe_audio(filepath)
    print("✅ Whisper Complete")

    print("👨‍💻 Diaritzation....")
    speaker_data = identify_speakers(filepath)
    print("✅ Diaritzation Complete")

    print("👨‍💻 Parsing...")
    parse(transcript_data,speaker_data)
    print("✅ Parsing Complete")
    
    return redirect(url_for('index'))

def load_json(file_path):
    with open(file_path, "r") as f:
            return json.load(f)
    
if __name__ == '__main__':
    app.run(debug=True)