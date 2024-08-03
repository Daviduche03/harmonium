from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, index=True)
    token_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))  

    user = relationship("User", back_populates="tokens")