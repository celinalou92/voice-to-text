import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
from transcribe_audio import transcribe_audio
from diarization_service import identify_speakers 
from transcript_response import transcription_response
from summary_agent import generate_summary
from util import format_audio

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

def load_json(file_path):
    with open(file_path, "r") as f:
            return json.load(f)
    
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 7860)), debug=False)