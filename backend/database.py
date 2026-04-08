from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use SQLite by default, can switch to PostgreSQL via DATABASE_URL env var
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/tracker.db")

# Ensure the directory exists
db_dir = os.path.dirname(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", ""))
if SQLALCHEMY_DATABASE_URL.startswith("sqlite") and db_dir:
    os.makedirs(db_dir, exist_ok=True)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
