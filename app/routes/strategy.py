# app/routes/strategy.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.ai.strategy_agent import generate_strategy

router = APIRouter(prefix="/strategy", tags=["Strategy"])

@router.post("/generate", response_model=schemas.StrategyOut)
def generate_strategy_for_user(request: schemas.StrategyRequest, db: Session = Depends(get_db)):
    # Step 1: Get the profile
    profile = db.query(models.NonProfitProfile).filter(models.NonProfitProfile.id == request.profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Step 2: Call AI and receive dict with title and content
    strategy_data = generate_strategy(profile, request.query)

    # Step 3: Save to DB
    new_strategy = models.Strategy(
        profile_id=profile.id,
        title=strategy_data["title"],
        content=strategy_data["content"]
    )
    db.add(new_strategy)
    db.commit()
    db.refresh(new_strategy)

    # Step 4: Return response
    return new_strategy
