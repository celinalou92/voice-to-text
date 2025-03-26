---
title: "Voice to Text Project"
sdk: "docker"
app_file: "transcription_app/app.py"
app_port: 7860
pinned: false
---

# Voice to Text Project

An audio transcription application that converts speech to text with advanced features for analysis.

## ⚡ Features

- Audio transcription with Whisper AI
- Speaker identification/diarization using pyannote-audio
- Key point extraction and summarization via OpenAI
- Conversation insights and analysis
- Basic UI for file upload and results

## 👨‍💻 Tech Stack

- **Python**
- **Flask**
- **Whisper AI**
- **OpenAI API (responses beta)**
- **pyannote-audio**
- **Jinja2 (HTML templating)**
  
## 📋 Usage

1. Upload an audio file (.m4a, .wav)
2. The system will:
   - Convert to WAV format if needed
   - Transcribe the audio
   - Identify different speakers
   - Generate a summary with key points
3. View the results in the web interface

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key
- Hugging Face token
- Flask
- 
### ⚙️ **Environment Setup**
Create a `.env` file in your project root with:

OPENAI_API_KEY=your-openai-key-here
SUMMARY_AGENT=you-agent-id
HUGGINGFACE_TOKEN=your-huggingface-key-here
### ▶️ **Running the App**
**Install Dependencies**
1. Clone the repository
   ```bash
   git clone <repo>
   cd voice-to-text
   ```
   
2. Install dependencies
    ```bash
    python -m pip install -r requirements.txt
    ```

## 🏃‍♂️ Running the App

**Run Locally**
**Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

**Backend**
```bash
python app.py
```

The application will be available at http://127.0.0.1:7860
---

## 📄 Output Format

The application generates structured JSON outputs for transcripts, speaker identification, and summaries. See [CONTRIBUTING.md](/transcription_app/CONTRIBUTING.md) for detailed schema information.

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](/transcription_app/CONTRIBUTING.md) for development setup and guidelines.

## 📝 License