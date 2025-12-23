import logging
import json
instructions = """
You are a paralegal assistant that is reviewing conversations to identify customer neglect and liability to the corporation.
You should evaluate these conversations in a non-biased manner, but with deep knowledge of business misconduct and consumer law.
You are reading JSON strings and summarizing the key points. Do not include any personally identifiable information.

An example of the structured input is below. The text segments contain the conversation and the speaker indicates who is talking.

[
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
    },
    {
        "start": 21.68,
        "end": 28.2,
        "text": "I understand your concern. Let me take a look at your account details and see what may have happened.",
        "speaker": "SPEAKER_00"
    },
    {
        "start": 28.2,
        "end": 33.92,
        "text": "Can you confirm your full name and the email address associated with the account?",
        "speaker": "SPEAKER_00"
    },
    {
        "start": 33.92,
        "end": 40.4,
        "text": "Sure. **************** I submitted a cancellation request a few weeks ago, so I’m just not sure why the charge went through.",
        "speaker": "SPEAKER_01"
    }
]

Below are key areas of interest. If information that falls within the criteria below is found in the conversation, it should be recorded in this format.
If any key points arise but do not fit in the categories below, include them in the Observations section.

The output use case example:

----
Observations:
- The customer experienced account suspension and an unexpected charge despite prior cancellation.
- There was a procedural error in handling the cancellation request, contributing to customer confusion and frustration.

Summary of Key Points:
1. Account Status:
   - The customer's account was suspended, and they noticed a charge of $149 for a service they believed had been canceled.

2. Customer Inquiry:
   - The customer sought clarification on the charge and the status of their account due to concerns over access loss and billing discrepancies.

3. Account Issues:
   - The customer had submitted a cancellation request weeks prior, but it was incorrectly routed and not processed, leading to both the account suspension and the charge.

4. Customer Service Response:
   - The representative acknowledged the error, assured the customer that their case would be escalated for review, and provided a timeframe for communication regarding the charge review.

5. Outcome:
   - The customer was informed they would receive a confirmation email within 24 hours and was given the option to follow up with support if needed. The customer expressed appreciation for the support received during the call.
----
"""

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_summary(transcript_data):
    print(f"    ... Generating Summary...")
    transcription = []
    for segment in transcript_data.segments:
        transcription_data = {
                        "id": segment["id"],
                        "start": round(segment["start"], 2),
                        "end": round(segment["end"], 2),
                        "speaker": segment["speaker"],
                        "text": segment["text"]
                    }
        transcription.append(transcription_data)
    transcript_text = json.dumps(transcription)

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=instructions,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": transcript_text,
                            "type": "input_text",
                        }
                    ],
                }
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "summary",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "observations": {"type": "string"},
                            "key_points": {
                                "type": "object",
                                "properties": {
                                    "account_status": {"type": "string"},
                                    "customer_inquiry": {"type": "string"},
                                    "account_issues": {"type": "string"},
                                    "customer_service_response": {"type": "string"},
                                    "outcome": {"type": "string"},
                                },
                                "required": [
                                    "account_status",
                                    "customer_inquiry",
                                    "account_issues",
                                    "customer_service_response",
                                    "outcome",
                                ],
                                "additionalProperties": False,
                            },
                        },
                        "required": ["observations", "key_points"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                }
            },
            temperature=1,
            max_output_tokens=2048,
            top_p=1,
            store=False,
        )        
        print(f"    ✅ Summary Complete!")
        return response
    except Exception as e:
        logging.error(f"Summary processing error: {e}")
        return f"Summary processing error: {e}"