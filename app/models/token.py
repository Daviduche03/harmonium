# app/models/token.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Token(Base):
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, index=True)
    token_type = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="tokens")