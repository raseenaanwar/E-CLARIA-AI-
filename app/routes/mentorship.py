from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.ai.mentor_agent import analyze_message_with_ai

router = APIRouter(prefix="/mentorship", tags=["Mentorship"])

@router.post("/optin", response_model=schemas.MentorProfileOut)
def opt_in(data: schemas.MentorProfileCreate, db: Session = Depends(get_db)):
    existing = db.query(models.MentorProfile).filter_by(user_id=data.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mentor already registered")
    mentor = models.MentorProfile(**data.dict())
    db.add(mentor)
    db.commit()
    db.refresh(mentor)
    return mentor

@router.get("/mentors", response_model=list[schemas.MentorProfileOut])
def list_available_mentors(db: Session = Depends(get_db)):
    return db.query(models.MentorProfile).filter_by(is_available=True).all()

@router.post("/message", response_model=schemas.MessageOut)
def send_message(data: schemas.MessageCreate, db: Session = Depends(get_db)):
    msg = models.MentorshipMessage(**data.dict())
    db.add(msg)
    db.commit()
    db.refresh(msg)

    # Optional: Trigger AI analysis
    analyze_message_with_ai(msg.message)

    return msg

@router.get("/messages/{user_id}", response_model=list[schemas.MessageOut])
def get_messages(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.MentorshipMessage).filter(
        (models.MentorshipMessage.sender_id == user_id) | 
        (models.MentorshipMessage.receiver_id == user_id)
    ).order_by(models.MentorshipMessage.timestamp.desc()).all()
