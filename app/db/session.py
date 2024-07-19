
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()  # Load environment variables from .env file

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
SQLALCHEMY_DATABASE_URL_DEV = os.getenv("SQLALCHEMY_DATABASE_URL_DEV")
SQLALCHEMY_DATABASE_URL_PROD = os.getenv("SQLALCHEMY_DATABASE_URL_PROD")

if ENVIRONMENT == "production":
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL_PROD
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, echo=True)
else:
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL_DEV
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)