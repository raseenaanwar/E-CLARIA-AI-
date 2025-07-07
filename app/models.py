from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)

# class NonProfitProfile(Base):
#     __tablename__ = "nonprofit_profiles"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     name = Column(String)
#     mission = Column(Text)
#     demographics = Column(Text, nullable=True)
#     past_methods = Column(Text, nullable=True)
#     fundraising_goals = Column(Text, nullable=True)
#     service_tags = Column(String, nullable=True)
#     sustainability_practices = Column(Text, nullable=True)
#     strategies = relationship("Strategy", back_populates="profile")
#     operating_years = Column(Integer, nullable=True)

class NonProfitProfile(Base):
    __tablename__ = "nonprofit_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    mission = Column(Text)
    demographics = Column(Text, nullable=True)
    past_methods = Column(Text, nullable=True)
    fundraising_goals = Column(Text, nullable=True)
    service_tags = Column(String, nullable=True)
    sustainability_practices = Column(Text, nullable=True)
    strategies = relationship("Strategy", back_populates="profile")
    operating_years = Column(Integer, nullable=True)

class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("nonprofit_profiles.id"))
    title = Column(String, nullable=True)       # optional, can store short description
    content = Column(Text, nullable=False)      # the generated strategy text
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("NonProfitProfile", back_populates="strategies")


class OutreachDraft(Base):
    __tablename__ = "outreach_drafts"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("nonprofit_profiles.id"))
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    tags = Column(String, nullable=True)

    user = relationship("User")
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    upvotes = Column(Integer, default=0)
    question = relationship("Question", back_populates="answers")
    user = relationship("User")

class Points(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, default=0)

    user = relationship("User")


class MentorProfile(Base):
    __tablename__ = "mentor_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    bio = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)
    expertise = Column(String, nullable=True)

    user = relationship("User")

class MentorshipMessage(Base):
    __tablename__ = "mentorship_messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
