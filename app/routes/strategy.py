from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.ai.strategy_agent import generate_strategy

router = APIRouter(prefix="/strategy", tags=["Strategy"])

@router.post("/generate")
def generate_strategy_for_user(request: schemas.StrategyRequest, db: Session = Depends(get_db)):
    profile = db.query(models.NonProfitProfile).filter(models.NonProfitProfile.user_id == request.user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    result = generate_strategy(profile)
    new_strategy = models.Strategy(
        user_id=request.user_id,
        strategy_text=result,
        sustainability_score=5  # Placeholder for demo
    )
    db.add(new_strategy)
    db.commit()
    db.refresh(new_strategy)
    return new_strategy
