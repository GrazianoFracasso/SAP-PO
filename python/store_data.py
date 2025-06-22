from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_FILE
from models import Base
# --- Database Setup ---

engine = create_engine(f"sqlite:///{DB_FILE}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)