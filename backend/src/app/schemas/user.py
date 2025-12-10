from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    learning_level: str = "beginner"
    interests: List[str] = []
    preferred_language: str = "en"

class UserPreferences(BaseModel):
    learning_level: Optional[str] = "beginner"  # beginner, intermediate, advanced
    interests: Optional[List[str]] = []  # e.g., ["technical", "practical", "hobbyist"]
    preferred_language: Optional[str] = "en"  # en, ur for English, Urdu
    content_format_preference: Optional[str] = "balanced"  # technical, simplified, balanced

class UserProgressUpdate(BaseModel):
    completed_sections: List[str]
    progress_percentage: int

class BookmarkCreate(BaseModel):
    content_id: str
    content_title: str
    module: str
    notes: Optional[str] = None

class InteractionLog(BaseModel):
    interaction_type: str  # "chat", "content_view", "bookmark", etc.
    content_id: Optional[str] = None
    content_title: Optional[str] = None
    query_text: Optional[str] = None
    response_text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class UserProgressResponse(BaseModel):
    progress: int
    completed_sections: List[str]
    last_accessed: Optional[datetime] = None

class BookmarkResponse(BaseModel):
    id: int
    content_id: str
    content_title: str
    module: str
    notes: Optional[str]
    created_at: datetime

class RecommendedContentItem(BaseModel):
    title: str
    module: str
    type: str
    relevance_score: float
    last_interaction: Optional[datetime] = None

class RecommendedContentResponse(BaseModel):
    recommendations: List[RecommendedContentItem]
    user_profile: Dict[str, Any]