import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    app_name: str = "Physical AI & Humanoid Robotics Book RAG Chatbot"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api"

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./book_content.db")

    # Vector database settings
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "./vector_db")
    collection_name: str = os.getenv("COLLECTION_NAME", "book_content")

    # OpenAI settings
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # Content settings
    content_directory: str = os.getenv("CONTENT_DIR", "../../../content")
    max_chunk_size: int = int(os.getenv("MAX_CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Server settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # CORS settings
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    class Config:
        env_file = ".env"

settings = Settings()