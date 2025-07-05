# app/ai/strategy_agent.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get values from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama3-8b-8192")

# Initialize Groq's OpenAI-compatible client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

def generate_strategy(profile, query: str) -> dict:
    """
    Generate a nonprofit fundraising strategy using Groq + LLaMA.
    Args:
        profile: SQLAlchemy NonProfitProfile instance
        query: Strategy request from user
    Returns:
        dict: {'title': ..., 'content': ...}
    """

    # Profile formatted prompt
    profile_data = f"""
📌 Organization: {profile.name}
🎯 Mission: {profile.mission}
👥 Target Demographics: {profile.demographics}
📚 Past Fundraising Methods: {profile.past_methods}
🥅 Fundraising Goals: {profile.fundraising_goals}
🏷️ Tags: {profile.service_tags}
🌱 Sustainability Practices: {profile.sustainability_practices}
    """

    full_prompt = (
        f"You are a fundraising strategist for nonprofits.\n"
        f"Use the following profile to create a tailored fundraising strategy for the query below.\n"
        f"{profile_data}\n"
        f"💬 Query: {query}\n\n"
        f"Provide a creative, clear, and effective fundraising strategy in bullet points or paragraphs."
    )

    # Call Groq's LLaMA model
    try:
        response = client.chat.completions.create(
            model=LLAMA_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert AI fundraising coach."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        result = response.choices[0].message.content.strip()

        return {
            "title": f"Strategy for: {query[:50]}",
            "content": result
        }

    except Exception as e:
        # fallback or log
        return {
            "title": "Strategy generation failed",
            "content": f"An error occurred: {str(e)}"
        }
