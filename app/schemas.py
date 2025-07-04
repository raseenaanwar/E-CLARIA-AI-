from pydantic import BaseModel, EmailStr
from typing import Optional, List

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

class ProfileCreate(BaseModel):
    mission: str
    goals: str
    sustainability_data: Optional[str]

class StrategyIn(BaseModel):
    prompt: str

class StrategyOut(BaseModel):
    id: int
    title: str
    content: str
    class Config:
        orm_mode = True

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


class StrategyRequest(BaseModel):
    profile_id: int
    query: str
