from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ..models.database import get_db, UserInteraction
from ..models.user_service import UserService
from ..schemas.user import UserCreate, UserResponse, UserPreferences, UserProgressUpdate, BookmarkCreate, InteractionLog
from ..utils.security import create_access_token
from ..middleware.auth import get_current_user

router = APIRouter(prefix="/api/personalization", tags=["personalization"])

logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user_service = UserService(db)

    # Check if user already exists
    existing_user = user_service.get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    existing_email = user_service.get_user_by_email(user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    user = user_service.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name
    )

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        learning_level=user.learning_level,
        interests=user.interests,
        preferred_language=user.preferred_language
    )

@router.post("/login")
async def login_user(username: str, password: str, db: Session = Depends(get_db)):
    """Login user and return access token"""
    user_service = UserService(db)
    user = user_service.authenticate_user(username, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/preferences", response_model=UserPreferences)
async def get_preferences(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user preferences for personalization"""
    user_service = UserService(db)
    preferences = user_service.get_user_preferences(current_user.id)

    return UserPreferences(**preferences)

@router.put("/preferences", response_model=UserPreferences)
async def update_preferences(
    preferences: UserPreferences,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user preferences for personalization"""
    user_service = UserService(db)
    updated_user = user_service.update_user_preferences(current_user.id, preferences.dict())

    return UserPreferences(
        learning_level=updated_user.learning_level,
        interests=updated_user.interests,
        preferred_language=updated_user.preferred_language,
        content_format_preference=updated_user.content_format_preference
    )

@router.post("/progress/{module}")
async def update_progress(
    module: str,
    progress_data: UserProgressUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user progress for a specific module"""
    user_service = UserService(db)
    progress = user_service.update_user_progress(
        current_user.id,
        module,
        progress_data.completed_sections,
        progress_data.progress_percentage
    )

    return {"message": "Progress updated successfully", "progress": progress.progress_percentage}

@router.get("/progress/{module}")
async def get_progress(
    module: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user progress for a specific module"""
    user_service = UserService(db)
    progress = user_service.get_user_progress(current_user.id, module)

    if not progress:
        return {"progress": 0, "completed_sections": []}

    return {
        "progress": progress.progress_percentage,
        "completed_sections": progress.completed_sections,
        "last_accessed": progress.last_accessed
    }

@router.post("/bookmarks", status_code=status.HTTP_201_CREATED)
async def add_bookmark(
    bookmark_data: BookmarkCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a bookmark for the user"""
    user_service = UserService(db)
    bookmark = user_service.add_bookmark(
        user_id=current_user.id,
        content_id=bookmark_data.content_id,
        content_title=bookmark_data.content_title,
        module=bookmark_data.module,
        notes=bookmark_data.notes
    )

    return {"message": "Bookmark added successfully", "bookmark_id": bookmark.id}

@router.get("/bookmarks", response_model=List[dict])
async def get_bookmarks(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all bookmarks for the user"""
    user_service = UserService(db)
    bookmarks = user_service.get_user_bookmarks(current_user.id)

    return [
        {
            "id": b.id,
            "content_id": b.content_id,
            "content_title": b.content_title,
            "module": b.module,
            "notes": b.notes,
            "created_at": b.created_at
        }
        for b in bookmarks
    ]

@router.delete("/bookmarks/{content_id}")
async def remove_bookmark(
    content_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a bookmark for the user"""
    user_service = UserService(db)
    success = user_service.remove_bookmark(current_user.id, content_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )

    return {"message": "Bookmark removed successfully"}

@router.post("/interactions")
async def log_interaction(
    interaction_data: InteractionLog,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a user interaction for personalization"""
    user_service = UserService(db)
    interaction = user_service.log_interaction(
        user_id=current_user.id,
        interaction_type=interaction_data.interaction_type,
        content_id=interaction_data.content_id,
        content_title=interaction_data.content_title,
        query_text=interaction_data.query_text,
        response_text=interaction_data.response_text,
        metadata=interaction_data.metadata
    )

    return {"message": "Interaction logged successfully", "interaction_id": interaction.id}

@router.get("/recommended-content")
async def get_recommended_content(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized content recommendations based on user profile and interactions"""
    user_service = UserService(db)
    preferences = user_service.get_user_preferences(current_user.id)

    # This is a simplified recommendation algorithm
    # In a full implementation, this would use more sophisticated ML models
    interests = preferences.get('interests', [])
    learning_level = preferences.get('learning_level', 'beginner')

    recommendations = []

    # Generate recommendations based on user preferences
    if 'technical' in interests:
        recommendations.append({
            "title": "Technical Implementation Details",
            "module": "Module 4",
            "type": "advanced_content",
            "relevance_score": 0.9
        })

    if 'practical' in interests:
        recommendations.append({
            "title": "Real-World Applications",
            "module": "Module 3",
            "type": "case_studies",
            "relevance_score": 0.85
        })

    # Add more recommendations based on learning level
    if learning_level == 'advanced':
        recommendations.append({
            "title": "Advanced Control Systems",
            "module": "Module 3",
            "type": "advanced",
            "relevance_score": 0.8
        })
    elif learning_level == 'beginner':
        recommendations.append({
            "title": "Introduction to Physical AI",
            "module": "Module 1",
            "type": "foundational",
            "relevance_score": 0.9
        })

    # Get recently interacted content
    recent_interactions = db.query(UserInteraction).filter(
        UserInteraction.user_id == current_user.id
    ).order_by(UserInteraction.timestamp.desc()).limit(5).all()

    # Add recommendations based on recent activity
    for interaction in recent_interactions[:2]:  # Top 2 recent interactions
        if interaction.content_id and interaction.content_title:
            recommendations.append({
                "title": f"Continue: {interaction.content_title}",
                "module": interaction.content_id.split('/')[0] if '/' in str(interaction.content_id) else "Unknown",
                "type": "continue_reading",
                "relevance_score": 0.7,
                "last_interaction": interaction.timestamp
            })

    return {
        "recommendations": recommendations,
        "user_profile": {
            "learning_level": learning_level,
            "interests": interests
        }
    }