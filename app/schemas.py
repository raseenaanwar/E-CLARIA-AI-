# from datetime import datetime
# from pydantic import BaseModel, EmailStr
# from typing import Optional, List

# # ---------------------- USER ----------------------

# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str
#     name: str

# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# class UserOut(BaseModel):
#     id: int
#     email: EmailStr
#     name: str

#     class Config:
#         from_attributes = True

# # ---------------------- NONPROFIT PROFILE ----------------------

# class NonProfitProfileCreate(BaseModel):
#     user_id: int
#     name: str
#     mission: str
#     demographics: Optional[str]
#     past_methods: Optional[str]
#     fundraising_goals: Optional[str]
#     service_tags: List[str] = []
#     sustainability_practices: Optional[str]
#     operating_years: int = 0  
   

# class NonProfitProfileOut(BaseModel):
#     id: int
#     name: str
#     mission: str
#     demographics: Optional[str]
#     past_methods: Optional[str]
#     fundraising_goals: Optional[str]
#     service_tags: str
#     sustainability_practices: Optional[str]

#     class Config:
#         from_attributes = True

# # ---------------------- STRATEGY ----------------------

# class StrategyRequest(BaseModel):
#     profile_id: int
#     query: str

# class StrategyOut(BaseModel):
#     id: int
#     title: str
#     content: str

#     class Config:
#         from_attributes = True

# # ---------------------- OUTREACH ----------------------

# class OutreachRequest(BaseModel):
#     profile_id: int
#     goal: str

# class OutreachOut(BaseModel):
#     id: int
#     title: str
#     content: str
#     class Config:
#         orm_mode = True

# # ---------------------- QUESTION ANSWER SECTION----------------------


# class QuestionCreate(BaseModel):
#     user_id: int
#     title: str
#     content: str
#     tags: Optional[str] = None

# class AnswerCreate(BaseModel):
#     question_id: int
#     user_id: int
#     content: str

# class QuestionOut(BaseModel):
#     id: int
#     title: str
#     content: str
#     user_id: int
#     tags: Optional[str]

#     class Config:
#         orm_mode = True

# class AnswerOut(BaseModel):
#     id: int
#     content: str
#     user_id: int
#     question_id: int

#     class Config:
#         orm_mode = True

# class PointsOut(BaseModel):
#     user_id: int
#     score: int

#     class Config:
#         orm_mode = True

# class MentorProfileCreate(BaseModel):
#     user_id: int
#     bio: str
#     expertise: str

# class MentorProfileOut(BaseModel):
#     id: int
#     user_id: int
#     bio: str
#     expertise: str
#     is_available: bool

#     class Config:
#         from_attributes = True

# class MessageCreate(BaseModel):
#     sender_id: int
#     receiver_id: int
#     message: str

# class MessageOut(BaseModel):
#     id: int
#     sender_id: int
#     receiver_id: int
#     message: str
#     timestamp: datetime

#     class Config:
#         from_attributes = True
from datetime import datetime
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
    profile_id: Optional[int] = None
    is_mentor: Optional[bool] = None

    class Config:
        from_attributes = True

# ---------------------- NONPROFIT PROFILE ----------------------

class NonProfitProfileCreate(BaseModel):
    user_id: int
    name: str
    mission: str
    demographics: Optional[str] = None
    past_methods: Optional[str] = None
    fundraising_goals: Optional[str] = None
    service_tags: List[str] = []
    sustainability_practices: Optional[str] = None
    operating_years: Optional[int] = None  # Made optional to match DB model

class NonProfitProfileOut(BaseModel):
    id: int
    user_id: int  # Added this - it's in the DB model
    name: str
    mission: str
    demographics: Optional[str]
    past_methods: Optional[str]
    fundraising_goals: Optional[str]
    service_tags: str  # This stays as string since it's stored as comma-separated
    sustainability_practices: Optional[str]
    operating_years: Optional[int]  # Added this field

    class Config:
        from_attributes = True

# ---------------------- STRATEGY ----------------------

class StrategyRequest(BaseModel):
    profile_id: int
    query: str

class StrategyOut(BaseModel):
    id: int
    title: str
    content: str
    audio_url: str | None  # NEW

    class Config:
        from_attributes = True

# ---------------------- OUTREACH ----------------------

class OutreachRequest(BaseModel):
    profile_id: int
    goal: str

class OutreachOut(BaseModel):
    id: int
    title: str
    content: str
    class Config:
        orm_mode = True

# ---------------------- QUESTION ANSWER SECTION----------------------

class QuestionCreate(BaseModel):
    user_id: int
    title: str
    content: str
    tags: Optional[str] = None

class AnswerCreate(BaseModel):
    question_id: int
    user_id: int
    content: str

class QuestionOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    tags: Optional[str]

    class Config:
        orm_mode = True

class AnswerOut(BaseModel):
    id: int
    content: str
    user_id: int
    question_id: int
    upvotes: int 

    class Config:
        orm_mode = True

class PointsOut(BaseModel):
    user_id: int
    score: int

    class Config:
        orm_mode = True

class MentorProfileCreate(BaseModel):
    user_id: int
    bio: str
    expertise: str

class MentorProfileOut(BaseModel):
    id: int
    user_id: int
    bio: str
    expertise: str
    is_available: bool

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    message: str

class MessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True