from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime
from .database import User, UserInteraction, UserBookmark, UserProgress
from ..utils.security import hash_password, verify_password

class UserService:
    """Service for managing user profiles and personalization"""

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, password: str, full_name: Optional[str] = None) -> User:
        """Create a new user with hashed password"""
        hashed_pwd = hash_password(password)

        user = User(
            username=username,
            email=email,
            hashed_password=hashed_pwd,
            full_name=full_name
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = self.get_user_by_username(username)
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]) -> User:
        """Update user preferences for personalization"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # Update user preferences based on provided data
        if 'learning_level' in preferences:
            user.learning_level = preferences['learning_level']

        if 'interests' in preferences:
            user.interests = preferences['interests']

        if 'preferred_language' in preferences:
            user.preferred_language = preferences['preferred_language']

        if 'content_format_preference' in preferences:
            user.content_format_preference = preferences['content_format_preference']

        self.db.commit()
        self.db.refresh(user)

        return user

    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Get user preferences for personalization"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        return {
            'learning_level': user.learning_level,
            'interests': user.interests,
            'preferred_language': user.preferred_language,
            'content_format_preference': user.content_format_preference
        }

    def log_interaction(self, user_id: int, interaction_type: str, content_id: Optional[str] = None,
                       content_title: Optional[str] = None, query_text: Optional[str] = None,
                       response_text: Optional[str] = None, metadata: Optional[Dict] = None) -> UserInteraction:
        """Log a user interaction for personalization"""
        interaction = UserInteraction(
            user_id=user_id,
            interaction_type=interaction_type,
            content_id=content_id,
            content_title=content_title,
            query_text=query_text,
            response_text=response_text,
            metadata=metadata
        )

        self.db.add(interaction)
        self.db.commit()
        self.db.refresh(interaction)

        return interaction

    def add_bookmark(self, user_id: int, content_id: str, content_title: str, module: str, notes: Optional[str] = None) -> UserBookmark:
        """Add a bookmark for a user"""
        bookmark = UserBookmark(
            user_id=user_id,
            content_id=content_id,
            content_title=content_title,
            module=module,
            notes=notes
        )

        self.db.add(bookmark)
        self.db.commit()
        self.db.refresh(bookmark)

        return bookmark

    def get_user_bookmarks(self, user_id: int) -> List[UserBookmark]:
        """Get all bookmarks for a user"""
        return self.db.query(UserBookmark).filter(UserBookmark.user_id == user_id).all()

    def remove_bookmark(self, user_id: int, content_id: str) -> bool:
        """Remove a bookmark for a user"""
        bookmark = self.db.query(UserBookmark).filter(
            UserBookmark.user_id == user_id,
            UserBookmark.content_id == content_id
        ).first()

        if bookmark:
            self.db.delete(bookmark)
            self.db.commit()
            return True

        return False

    def update_user_progress(self, user_id: int, module: str, completed_sections: List[str],
                           progress_percentage: int) -> UserProgress:
        """Update user progress for a module"""
        progress = self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.module == module
        ).first()

        if progress:
            # Update existing progress
            progress.completed_sections = completed_sections
            progress.progress_percentage = progress_percentage
            progress.last_accessed = datetime.utcnow()
        else:
            # Create new progress record
            progress = UserProgress(
                user_id=user_id,
                module=module,
                completed_sections=completed_sections,
                progress_percentage=progress_percentage
            )
            self.db.add(progress)

        self.db.commit()
        self.db.refresh(progress)

        return progress

    def get_user_progress(self, user_id: int, module: str) -> Optional[UserProgress]:
        """Get user progress for a specific module"""
        return self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.module == module
        ).first()

    def get_all_user_progress(self, user_id: int) -> List[UserProgress]:
        """Get user progress for all modules"""
        return self.db.query(UserProgress).filter(UserProgress.user_id == user_id).all()