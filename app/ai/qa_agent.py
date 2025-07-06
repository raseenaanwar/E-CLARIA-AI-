import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama3-8b-8192")

def get_client():
    try:
        return OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_API_KEY,
            timeout=30.0
        )
    except Exception as e:
        print("Groq Client Error:", e)
        return None

client = get_client()

# ---------------------------- TAG CLASSIFIER ----------------------------

def classify_tags_llama(question: str) -> str:
    """
    Use LLaMA to classify tags for a nonprofit question.
    """
    prompt = f"""
Classify this question into 3 relevant tags (comma-separated). Be concise and use lowercase.
---
Question: "{question}"
---
Example tags: fundraising, donors, strategy
Only return comma-separated tags.
"""

    try:
        response = client.chat.completions.create(
            model=LLAMA_MODEL,
            messages=[
                {"role": "system", "content": "You are a smart tag classifier for nonprofit questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Tag classification error:", e)
        return "general,question,nonprofit"

# ---------------------------- SUGGESTED ANSWER ----------------------------

def suggest_answer_llama(question: str) -> str:
    """
    Use LLaMA to suggest an answer for a nonprofit question.
    """
    prompt = f"""
You are an expert advisor for nonprofit organizations.

Based on this question, suggest a clear and helpful answer that a nonprofit leader could implement.
---
Question: "{question}"
"""

    try:
        response = client.chat.completions.create(
            model=LLAMA_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for nonprofit Q&A."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Suggested answer error:", e)
        return "Sorry, the AI could not generate a suggestion at this time."