from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import cast, String

router = APIRouter(
    prefix="/profile",
    tags=["Non-Profit Profile"]
)

# @router.post("/", response_model=schemas.NonProfitProfileOut)
# def create_profile(profile: schemas.NonProfitProfileCreate, db: Session = Depends(database.get_db)):
#     new_profile = models.NonProfitProfile(
    
#         user_id=profile.user_id,
#         name=profile.name,
#         mission=profile.mission,
#         demographics=profile.demographics,
#         past_methods=profile.past_methods,
#         fundraising_goals=profile.fundraising_goals,
#         service_tags=",".join(profile.service_tags),
#         sustainability_practices=profile.sustainability_practices
#     )
#     db.add(new_profile)
#     db.commit()
#     db.refresh(new_profile)
#     return new_profile

@router.post("/", response_model=schemas.NonProfitProfileOut)
def create_profile(profile: schemas.NonProfitProfileCreate, db: Session = Depends(database.get_db)):
    new_profile = models.NonProfitProfile(
        user_id=profile.user_id,
        name=profile.name,
        mission=profile.mission,
        demographics=profile.demographics,
        past_methods=profile.past_methods,
        fundraising_goals=profile.fundraising_goals,
        service_tags=",".join(profile.service_tags),
        sustainability_practices=profile.sustainability_practices,
        operating_years=profile.operating_years
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile



@router.get("/{user_id}", response_model=schemas.NonProfitProfileOut)
def get_profile(user_id: int, db: Session = Depends(database.get_db)):
    profile = db.query(models.NonProfitProfile).filter(models.NonProfitProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
