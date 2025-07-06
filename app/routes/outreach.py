# app/routes/outreach.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.ai.outreach_agent import generate_outreach

router = APIRouter(prefix="/outreach", tags=["Outreach"])

@router.post("/generate", response_model=schemas.OutreachOut)
def generate_outreach_draft(request: schemas.OutreachRequest, db: Session = Depends(get_db)):
    profile = db.query(models.NonProfitProfile).filter(models.NonProfitProfile.id == request.profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    draft = generate_outreach(profile, request.goal)

    new_draft = models.OutreachDraft(
        profile_id=profile.id,
        title=draft["title"],
        content=draft["content"]
    )

    db.add(new_draft)
    db.commit()
    db.refresh(new_draft)

    return new_draft