import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama3-8b-8192")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

def analyze_message_with_ai(message_text: str):
    prompt = f"""
You are analyzing this mentorship message for educational insights:
"{message_text}"

Please extract:
1. Main topics discussed
2. Nonprofit advice given
3. Any emotional tone (supportive, instructional, motivational, etc.)
Only return clean insights. Remove personal details.
"""

    try:
        response = client.chat.completions.create(
            model=LLAMA_MODEL,
            messages=[
                {"role": "system", "content": "You're an AI assistant for mentorship content analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        print("AI Insight:", response.choices[0].message.content)
        # You could store this in DB for training, metrics, or dashboard later
    except Exception as e:
        print("AI Error:", e)
