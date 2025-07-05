from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)

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

# class Strategy(Base):
#     __tablename__ = "strategies"
#     id = Column(Integer, primary_key=True, index=True)
#     profile_id = Column(Integer, ForeignKey("nonprofit_profiles.id"))
#     title = Column(String)
#     content = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)

class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("nonprofit_profiles.id"))
    title = Column(String, nullable=True)       # optional, can store short description
    content = Column(Text, nullable=False)      # the generated strategy text
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("NonProfitProfile", back_populates="strategies")
