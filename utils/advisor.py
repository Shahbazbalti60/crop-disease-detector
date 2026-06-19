import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_advice(crop: str, disease: str, confidence: float) -> dict:
    
    prompt = f"""You are an expert agricultural advisor helping farmers in Pakistan.

A crop disease detection system has identified the following:
- Crop: {crop}
- Disease: {disease}
- Confidence: {confidence}%

Please provide advice in this exact JSON format:
{{
    "cause": "Brief explanation of what causes this disease (1-2 sentences)",
    "immediate_action": "What the farmer should do right now (1-2 sentences)",
    "treatment": "Specific fungicide or treatment recommendation (1-2 sentences)",
    "prevention": "How to prevent this in future (1-2 sentences)",
    "urdu_summary": "ایک جملے میں اردو میں خلاصہ"
}}

Respond with only the JSON, no extra text."""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    
    import json
    raw = response.choices[0].message.content.strip()
    advice = json.loads(raw)
    return advice