import os
import json
from flask import Flask, render_template
from api.upload import upload_bp 
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(upload_bp, url_prefix='/api')

os.makedirs('uploads', exist_ok=True)
os.makedirs('output', exist_ok=True)

@app.route('/')
def index():
    transcript_file = os.path.join('output/transcripts', 'transcript.json')
    transcript = None
    
    if os.path.exists(transcript_file):
        transcript = load_json(transcript_file)

    return render_template('index.html', transcript=transcript)

def load_json(file_path):
    with open(file_path, "r") as f:
            return json.load(f)
    
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 7860)), debug=False)