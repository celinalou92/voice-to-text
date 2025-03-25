---
title: {{Voice to Text Project}}
sdk: {{streamlit}}
app_file: transcription_app/app.py
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
- **FastAPI**
- **Whisper AI**
- **OpenAI API (responses beta)**
- **pyannote-audio**
- **Jinja2 (HTML templating)**

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Poetry (dependency management)
- OpenAI API key
- Hugging Face token

### Installation

1. Clone the repository
   ```bash
   git clone <repo>
   cd voice-to-text
   ```

2. Install dependencies
   ```bash
   poetry install
   ```

3. Set up environment variables  
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your-openai-key-here
   SUMMARY_AGENT=your-agent-id
   HUGGINGFACE_TOKEN=your-huggingface-key-here
   ```

## 🏃‍♂️ Running the App

```bash
poetry run python app.py
```

The application will be available at http://localhost:8000

## 📋 Usage

1. Upload an audio file (.m4a, .wav)
2. The system will:
   - Convert to WAV format if needed
   - Transcribe the audio
   - Identify different speakers
   - Generate a summary with key points
3. View the results in the web interface

## 📁 Project Structure

```
transcription_app/
├── output/                         
│   ├── conversion_wav/             
│   ├── diarization/                
│   ├── openai/                    
│   ├── transcripts/                
│   └── whisper/                    
├── templates/
├── uploads/                             
├── app.py               
├── diarization_service.py                
├── requirements.txt               
├── summary_agent.py               
├── transcribe_audio.py           
├── transcript_response.py                     
├── CONTRIBUTING.md                      
├── pyproject.toml 
```

## 📄 Output Format

The application generates structured JSON outputs for transcripts, speaker identification, and summaries. See [CONTRIBUTING.md](/transcription_app/CONTRIBUTING.md) for detailed schema information.

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](/transcription_app/CONTRIBUTING.md) for development setup and guidelines.

## 📝 License

[Add your license here]