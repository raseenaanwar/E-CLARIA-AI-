# app/ai/outreach_agent.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load env
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
        print("Client error:", e)
        return None

client = get_client()

def generate_outreach(profile, goal: str) -> dict:
    """
    Generate outreach message based on nonprofit profile and user goal.
    """
    profile_data = f"""
📌 Organization: {profile.name}
🎯 Mission: {profile.mission}
👥 Target Demographics: {profile.demographics}
📚 Past Fundraising Methods: {profile.past_methods}
🥅 Fundraising Goals: {profile.fundraising_goals}
🏷️ Tags: {profile.service_tags}
🌱 Sustainability Practices: {profile.sustainability_practices}
    """

    prompt = (
        f"You are an expert outreach agent for nonprofits.\n"
        f"Create a compelling outreach email or message to help the organization achieve this goal: \"{goal}\".\n"
        f"Highlight their strengths, especially sustainability and community impact.\n\n"
        f"{profile_data}"
    )

    try:
        response = client.chat.completions.create(
            model=LLAMA_MODEL,
            messages=[
                {"role": "system", "content": "You help nonprofits write professional outreach messages."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
            max_tokens=800
        )

        message = response.choices[0].message.content.strip()

        return {
            "title": f"Outreach Draft for: {goal[:50]}",
            "content": message
        }

    except Exception as e:
        return {
            "title": "Error generating outreach",
            "content": f"AI error: {str(e)}"
        }
