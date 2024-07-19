# app/models/bot.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Bot(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    unique_id = Column(String, unique=True, index=True)
    web_search = Column(Boolean, index=True)
    instruction = Column(String, index=True)
    # user_id = Column(Integer, ForeignKey("user.id"))

    # user = relationship("User", back_populates="bots")
    embeddings = relationship("Embedding", back_populates="bot")