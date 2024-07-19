# app/models/embedding.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Embedding(Base):
    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, unique=True, index=True)
    unique_id = Column(String, unique=True, index=True)
    bot_id = Column(Integer, ForeignKey("bot.id"))

    bot = relationship("Bot", back_populates="embeddings")