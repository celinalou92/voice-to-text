# Voice to Text Project 
An audio transcription application. 

## 👨‍💻 Tech Stack

- **Python**
- **FastAPI**
- **Whisper AI**
- **OpenAI API (responses beta)**
- **pyannote-audio**
- **Jinja2 (HTML templating)**


## 📁 Project Structure

```
transcription_app/
├── output/                         
│   ├── conversion_wav/             
│   │   └── conversion.wav
│   ├── diarization/                
│   │   └── diarization_output.json
│   ├── openai/                    
│   │   └── summary.json
│   ├── transcripts/                
│   │   └── transcript.json
│   └── whisper/                    
│       └── whisper_transcript.json
├── templates/
│   └── index.html
├── uploads/
│   └──filename.m4a                             
├── app.py               
├── diarization_service.py                
├── requirements.txt               
├── summary_agent.py               
├── transcribe_audio.py           
├── transcript_response.py                     
├── CONTRIBUTING.md                      
├── pyproject.toml 
```

### ⚙️ **Environment Setup**
Create a `.env` file in your project root with:

OPENAI_API_KEY=your-openai-key-here
SUMMARY_AGENT=you-agent-id
HUGGINGFACE_TOKEN=your-huggingface-key-here

### ▶️ **Running the App**

**Backend**
```bash
poetry run python app.py
```

---

## 📄 JSON Schema 

### Whisper Output
The Whisper response is structured like this:
```json
[
    {
        "start": "double",
        "end": "double",
        "text": "string",
        "speaker": "string"
    },
    {
        "start": "double",
        "end": "double",
        "text": "string",
        "speaker": "string"
    }
]
```

### Summery Output
The OpenAI response is structured like this:
```json
{
  "observations": "string",
  "key_points": {
    "account_status": "string",
    "customer_inquiry": "string",
    "account_issues": "string",
    "customer_service_response": "string",
    "outcome": "string"
  }
}
```

### Speaker Output
The pyannote-audio response is structured like this:
```json
[
    {
        "speaker": "string",
        "start": "double",
        "end": "double"
    },
    {
        "speaker": "string",
        "start": "double",
        "end": "double"
    },
    {
        "speaker": "string",
        "start": "double",
        "end": "double"
    },
    {
        "speaker": "string",
        "start": "double",
        "end": "double"
    },
    {
        "speaker": "string",
        "start": "double",
        "end": "double"
    }
]
```

 
### 📤 **Example Output**
```json
{
  "observations": "The customer experienced a charge after cancellation...",
  "key_points": {
    "account_status": "The customer's account was suspended...",
    "customer_inquiry": "The customer inquired about billing discrepancies...",
    "account_issues": "The cancellation was not processed correctly...",
    "customer_service_response": "The agent acknowledged the error and escalated the case...",
    "outcome": "The customer was informed a follow-up would be provided."
  },
  "segments": [
    {
        "start": 0.0,
        "end": 7.92,
        "text": "Thank you for contacting Apex Services. This is Daniel in account support. How can I assist you today?",
        "speaker": "SPEAKER_00"
    },
    {
        "start": 7.92,
        "end": 14.8,
        "text": "Hi Daniel. I noticed that my account was suspended yesterday, but I also saw a charge of one hundred and forty-nine dollars for a service",
        "speaker": "SPEAKER_01"
    },
    {
        "start": 14.8,
        "end": 21.68,
        "text": "I thought I had canceled last month. I’m just a little confused about what’s going on.",
        "speaker": "SPEAKER_01"
    }
  ]
}
```


