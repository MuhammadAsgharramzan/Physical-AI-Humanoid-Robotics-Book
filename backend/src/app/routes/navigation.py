from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
import logging

from ..services.navigation_service import navigation_service, LearningObjective, NavigationStyle, UserLearningProfile

router = APIRouter(prefix="/api/navigation", tags=["navigation-path"])

logger = logging.getLogger(__name__)

@router.get("/standard-paths")
async def get_standard_paths():
    """
    Get all available standard navigation paths
    """
    try:
        standard_paths = []
        for path_type, path in navigation_service.standard_paths.items():
            standard_paths.append({
                "path_id": path.path_id,
                "name": path.name,
                "description": path.description,
                "modules": path.modules,
                "sections": path.sections,
                "estimated_duration": path.estimated_duration,
                "difficulty_level": path.difficulty_level,
                "learning_objectives": [obj.value for obj in path.learning_objectives],
                "navigation_style": path.navigation_style.value
            })

        return {"standard_paths": standard_paths}

    except Exception as e:
        logger.error(f"Get standard paths error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve standard paths")

@router.post("/customize-path")
async def customize_path(
    user_id: Optional[int] = None,
    learning_objectives: List[str] = [],
    technical_background: str = "beginner",
    time_availability: str = "flexible",
    interests: List[str] = [],
    preferred_style: str = "linear"
):
    """
    Customize a navigation path based on user profile
    """
    try:
        # Validate learning objectives
        validated_objectives = []
        for obj in learning_objectives:
            try:
                validated_objectives.append(LearningObjective(obj.lower()))
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid learning objective: {obj}. Supported: {[lo.value for lo in LearningObjective]}"
                )

        # Validate navigation style
        try:
            nav_style = NavigationStyle(preferred_style.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid navigation style: {preferred_style}. Supported: {[ns.value for ns in NavigationStyle]}"
            )

        # Validate technical background
        valid_backgrounds = ["beginner", "intermediate", "advanced"]
        if technical_background.lower() not in valid_backgrounds:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid technical background: {technical_background}. Supported: {valid_backgrounds}"
            )

        # Validate time availability
        valid_time_availability = ["limited", "moderate", "extensive", "flexible"]
        if time_availability.lower() not in valid_time_availability:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid time availability: {time_availability}. Supported: {valid_time_availability}"
            )

        # Create user profile
        user_profile = UserLearningProfile(
            user_id=user_id,
            learning_objectives=validated_objectives,
            preferred_navigation_style=nav_style,
            technical_background=technical_background.lower(),
            time_availability=time_availability.lower(),
            interests=interests
        )

        # Customize path
        customized_path = await navigation_service.customize_path_for_user(user_profile)

        return {
            "path_id": customized_path.path_id,
            "name": customized_path.name,
            "description": customized_path.description,
            "modules": customized_path.modules,
            "sections": customized_path.sections,
            "estimated_duration": customized_path.estimated_duration,
            "difficulty_level": customized_path.difficulty_level,
            "learning_objectives": [obj.value for obj in customized_path.learning_objectives],
            "navigation_style": customized_path.navigation_style.value,
            "customized_for_user": customized_path.customized_for_user
        }

    except Exception as e:
        logger.error(f"Path customization error: {str(e)}")
        raise HTTPException(status_code=500, detail="Path customization failed")

@router.post("/get-recommendations")
async def get_navigation_recommendations(
    user_id: Optional[int] = None,
    learning_objectives: List[str] = [],
    technical_background: str = "beginner",
    time_availability: str = "flexible",
    interests: List[str] = [],
    preferred_style: str = "linear"
):
    """
    Get recommendations for navigation path customization
    """
    try:
        # Validate learning objectives
        validated_objectives = []
        for obj in learning_objectives:
            try:
                validated_objectives.append(LearningObjective(obj.lower()))
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid learning objective: {obj}. Supported: {[lo.value for lo in LearningObjective]}"
                )

        # Validate navigation style
        try:
            nav_style = NavigationStyle(preferred_style.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid navigation style: {preferred_style}. Supported: {[ns.value for ns in NavigationStyle]}"
            )

        # Create user profile
        user_profile = UserLearningProfile(
            user_id=user_id,
            learning_objectives=validated_objectives,
            preferred_navigation_style=nav_style,
            technical_background=technical_background.lower(),
            time_availability=time_availability.lower(),
            interests=interests
        )

        recommendations = await navigation_service.get_navigation_recommendations(user_profile)

        return recommendations

    except Exception as e:
        logger.error(f"Navigation recommendations error: {str(e)}")
        raise HTTPException(status_code=500, detail="Navigation recommendations failed")

@router.post("/validate-path")
async def validate_path(
    modules: List[str],
    sections: List[str],
    learning_objectives: List[str] = []
):
    """
    Validate a navigation path for consistency and completeness
    """
    try:
        # Create a temporary path for validation
        from ..services.navigation_service import NavigationPath

        temp_path = NavigationPath(
            path_id="validation",
            name="Validation Path",
            description="Path for validation purposes",
            modules=modules,
            sections=sections,
            estimated_duration=0,
            difficulty_level="beginner",
            learning_objectives=[LearningObjective(obj.lower()) for obj in learning_objectives if obj],
            navigation_style=NavigationStyle.LINEAR
        )

        validation_result = await navigation_service.validate_path(temp_path)

        return validation_result

    except Exception as e:
        logger.error(f"Path validation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Path validation failed")

@router.get("/supported-objectives")
async def get_supported_learning_objectives():
    """
    Get list of supported learning objectives
    """
    return {
        "supported_objectives": [
            {
                "objective": lo.value,
                "description": lo.name.lower().replace('_', ' ')
            }
            for lo in LearningObjective
        ]
    }

@router.get("/supported-styles")
async def get_supported_navigation_styles():
    """
    Get list of supported navigation styles
    """
    return {
        "supported_styles": [
            {
                "style": ns.value,
                "description": ns.name.lower().replace('_', ' ')
            }
            for ns in NavigationStyle
        ]
    }