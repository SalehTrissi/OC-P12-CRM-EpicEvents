import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Retrieve the database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("The DATABASE_URL environment variable is not defined.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

# Create a session to manage transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = SessionLocal()
