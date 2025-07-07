# app/routes/strategy.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.ai.strategy_agent import generate_strategy
import os
from groq import Groq  # NEW
from datetime import datetime 

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

router = APIRouter(prefix="/strategy", tags=["Strategy"])

@router.post("/generate", response_model=schemas.StrategyOut)
def generate_strategy_for_user(request: schemas.StrategyRequest, db: Session = Depends(get_db)):
    # Step 1: Get the profile
    profile = db.query(models.NonProfitProfile).filter(models.NonProfitProfile.id == request.profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Step 2: Call AI and receive dict with title and content
    strategy_data = generate_strategy(profile, request.query)

    # Step 3: Generate TTS using Groq
    try:
        tts_response = groq_client.audio.speech.create(
            model="playai-tts",
            voice="Fritz-PlayAI",  # You can change voice
            input=strategy_data["content"],
            response_format="wav"
        )
        wav_data = tts_response.read()

        # Save to static/audio/
        timestamp = int(datetime.utcnow().timestamp())  # ✅ Fix: Use datetime
        audio_filename = f"strategy_{profile.id}_{timestamp}.wav"
        audio_path = f"static/audio/{audio_filename}"
        os.makedirs("static/audio", exist_ok=True)
        with open(audio_path, "wb") as f:
            f.write(wav_data)

        audio_url = f"/audio/{audio_filename}"
    except Exception as e:
        print("TTS error:", e)
        audio_url = None

    # Step 4: Save to DB
    new_strategy = models.Strategy(
        profile_id=profile.id,
        title=strategy_data["title"],
        content=strategy_data["content"],
        audio_url=audio_url
    )
    db.add(new_strategy)
    db.commit()
    db.refresh(new_strategy)

    # Step 5: Return response
    return new_strategy


