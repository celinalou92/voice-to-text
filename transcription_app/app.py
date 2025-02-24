import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

os.makedirs('uploads', exist_ok=True)
os.makedirs('transcripts', exist_ok=True)

@app.route('/')
def index():
    transcript_file = os.path.join('transcripts', 'transcript.txt')
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

    transcript = process_audio(filepath)

    key_points = extract_key_points(transcript)
    speakers = identify_speakers(filepath)

    transcript_file = os.path.join('transcripts', 'transcript.txt')
    with open(transcript_file, 'w') as f:
        f.write(transcript)

    jsonify({
        'transcript': transcript,
        'key_points': key_points,
        'speakers': speakers
    })
    return index()

def process_audio(filepath):
    return "This is a dummy transcript from the audio."

def extract_key_points(transcript):
    from collections import Counter
    words = transcript.lower().split()
    counter = Counter(words)
    return counter.most_common(3)

def identify_speakers(filepath):
    return ["Speaker 1", "Speaker 2"]

if __name__ == '__main__':
    app.run(debug=True)