from pydantic import BaseModel, EmailStr
from typing import Optional, List

# ---------------------- USER ----------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
        orm_mode = True

# ---------------------- NONPROFIT PROFILE ----------------------

class NonProfitProfileCreate(BaseModel):
    user_id: int
    name: str
    mission: str
    demographics: Optional[str]
    past_methods: Optional[str]
    fundraising_goals: Optional[str]
    service_tags: List[str] = []
    sustainability_practices: Optional[str]

class NonProfitProfileOut(BaseModel):
    id: int
    name: str
    mission: str
    demographics: Optional[str]
    past_methods: Optional[str]
    fundraising_goals: Optional[str]
    service_tags: str
    sustainability_practices: Optional[str]

    class Config:
        orm_mode = True

# ---------------------- STRATEGY ----------------------

class StrategyRequest(BaseModel):
    profile_id: int
    query: str

class StrategyOut(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True
