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

....


## 📄 JSON Schema for Summary Output

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

### ⚙️ **Environment Setup**
Create a `.env` file in your project root with:
OPENAI_API_KEY=your-openai-key-here
SUMMARY_AGENT=optional-agent-name


### ▶️ **Running the App**
```bash
# uvicorn src.main:app --reload 
poetry run python app.py

poetry run python manage.py runserver
```
---

### 📥 **Example Input**

```json
[
  {
    "start": 0.0,
    "end": 7.92,
    "text": "Thank you for contacting Apex Services...",
    "speaker": "SPEAKER_00"
  }
]
```
---

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
  }
}
```


