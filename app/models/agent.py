# app/models/bot.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class AgentModel(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    goal = Column(String)
    backstory = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))