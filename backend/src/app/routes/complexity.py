from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from ..services.complexity_service import complexity_service, ComplexityLevel, ComplexityAdjustment

router = APIRouter(prefix="/api/complexity", tags=["complexity-adjustment"])

logger = logging.getLogger(__name__)

@router.post("/adjust-content", response_model=Dict[str, Any])
async def adjust_content_complexity(
    content: str,
    target_level: str  # "beginner", "intermediate", or "advanced"
):
    """
    Adjust content complexity based on user profile
    """
    try:
        # Validate complexity level
        try:
            user_complexity_level = ComplexityLevel(target_level.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid complexity level. Supported levels: {[level.value for level in ComplexityLevel]}"
            )

        result = await complexity_service.adjust_content_complexity(
            content,
            user_complexity_level
        )

        return {
            "original_content": result.original_content,
            "adjusted_content": result.adjusted_content,
            "original_complexity": result.original_complexity.value,
            "target_complexity": result.target_complexity.value,
            "adjustment_confidence": result.adjustment_confidence
        }

    except Exception as e:
        logger.error(f"Complexity adjustment error: {str(e)}")
        raise HTTPException(status_code=500, detail="Complexity adjustment failed")

@router.post("/estimate-complexity")
async def estimate_content_complexity(content: str):
    """
    Estimate the complexity level of content
    """
    try:
        complexity_level = complexity_service.estimate_content_complexity(content)
        return {"complexity_level": complexity_level.value}
    except Exception as e:
        logger.error(f"Complexity estimation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Complexity estimation failed")

@router.post("/get-recommendations")
async def get_complexity_recommendations(
    content: str,
    target_level: str
):
    """
    Get recommendations for content complexity adjustments
    """
    try:
        # Validate complexity level
        try:
            user_complexity_level = ComplexityLevel(target_level.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid complexity level. Supported levels: {[level.value for level in ComplexityLevel]}"
            )

        recommendations = await complexity_service.get_complexity_recommendations(
            content,
            user_complexity_level
        )

        return recommendations

    except Exception as e:
        logger.error(f"Complexity recommendations error: {str(e)}")
        raise HTTPException(status_code=500, detail="Complexity recommendations failed")

@router.get("/supported-levels")
async def get_supported_complexity_levels():
    """
    Get list of supported complexity levels
    """
    return {
        "supported_levels": [
            {
                "level": level.value,
                "description": level.name.lower()
            }
            for level in ComplexityLevel
        ]
    }