from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from .config import settings

# Create base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Profile preferences
    learning_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    interests = Column(JSON, default=lambda: [])  # e.g., ["technical", "practical", "hobbyist"]
    preferred_language = Column(String, default="en")  # en, ur for English, Urdu
    content_format_preference = Column(String, default="balanced")  # technical, simplified, balanced

class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Foreign key to users table
    interaction_type = Column(String, nullable=False)  # "chat", "content_view", "bookmark", etc.
    content_id = Column(String)  # ID or path of the content interacted with
    content_title = Column(String)  # Title of the content
    query_text = Column(Text)  # For chat interactions
    response_text = Column(Text)  # For chat interactions
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)  # Additional metadata about the interaction

class UserBookmark(Base):
    __tablename__ = "user_bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Foreign key to users table
    content_id = Column(String, nullable=False)  # ID or path of the bookmarked content
    content_title = Column(String, nullable=False)
    module = Column(String)  # Module this content belongs to
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)  # User's notes about this bookmark

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Foreign key to users table
    module = Column(String, nullable=False)  # Module identifier
    completed_sections = Column(JSON, default=lambda: [])  # List of completed section IDs
    progress_percentage = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    time_spent_seconds = Column(Integer, default=0)

# Database setup
def get_database_url():
    """Get database URL from settings"""
    # For Neon DB, the URL would typically be provided via environment variable
    database_url = os.getenv("DATABASE_URL", settings.database_url)

    # If using Neon DB specifically, ensure the URL is properly formatted
    if "neon" in database_url.lower():
        # Ensure SSL is enabled for Neon
        if "?" not in database_url:
            database_url += "?sslmode=require"
        else:
            database_url += "&sslmode=require"

    return database_url

# Create engine
engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    # Create tables when this module is run directly
    create_tables()
    print("Database tables created successfully!")