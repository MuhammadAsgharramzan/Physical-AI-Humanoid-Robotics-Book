from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
import logging

from ..services.example_service import example_service, Example, ExampleType, UserInterest

router = APIRouter(prefix="/api/examples", tags=["example-selection"])

logger = logging.getLogger(__name__)

@router.post("/select-for-user")
async def select_examples_for_user(
    user_interests: List[str] = Query(..., description="List of user interests"),
    learning_level: str = Query("beginner", description="User learning level: beginner, intermediate, or advanced"),
    module: Optional[str] = Query(None, description="Optional module filter"),
    count: int = Query(3, description="Number of examples to return")
):
    """
    Select examples based on user interests and profile
    """
    try:
        result = await example_service.select_examples_for_user(
            user_interests=user_interests,
            learning_level=learning_level,
            module=module,
            count=count
        )

        return {
            "selected_examples": [
                {
                    "id": ex.id,
                    "title": ex.title,
                    "description": ex.description,
                    "content": ex.content,
                    "example_type": ex.example_type.value,
                    "module": ex.module,
                    "difficulty_level": ex.difficulty_level,
                    "tags": ex.tags,
                    "relevance_score": ex.relevance_score
                }
                for ex in result.selected_examples
            ],
            "selection_reasoning": result.selection_reasoning,
            "user_profile_match": result.user_profile_match
        }

    except Exception as e:
        logger.error(f"Example selection error: {str(e)}")
        raise HTTPException(status_code=500, detail="Example selection failed")

@router.get("/by-type/{example_type}")
async def get_examples_by_type(
    example_type: str,
    count: int = Query(5, description="Number of examples to return")
):
    """
    Get examples of a specific type
    """
    try:
        # Validate example type
        try:
            ex_type = ExampleType(example_type.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid example type. Supported types: {[et.value for et in ExampleType]}"
            )

        examples = await example_service.get_examples_by_type(ex_type, count)

        return [
            {
                "id": ex.id,
                "title": ex.title,
                "description": ex.description,
                "content": ex.content,
                "example_type": ex.example_type.value,
                "module": ex.module,
                "difficulty_level": ex.difficulty_level,
                "tags": ex.tags
            }
            for ex in examples
        ]

    except Exception as e:
        logger.error(f"Get examples by type error: {str(e)}")
        raise HTTPException(status_code=500, detail="Get examples by type failed")

@router.get("/search")
async def search_examples(
    query: str = Query(..., description="Search query for examples"),
    count: int = Query(5, description="Number of examples to return")
):
    """
    Search examples by keyword
    """
    try:
        examples = await example_service.search_examples(query, count)

        return [
            {
                "id": ex.id,
                "title": ex.title,
                "description": ex.description,
                "content": ex.content,
                "example_type": ex.example_type.value,
                "module": ex.module,
                "difficulty_level": ex.difficulty_level,
                "tags": ex.tags
            }
            for ex in examples
        ]

    except Exception as e:
        logger.error(f"Example search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Example search failed")

@router.get("/supported-types")
async def get_supported_example_types():
    """
    Get list of supported example types
    """
    return {
        "supported_types": [
            {
                "type": et.value,
                "description": et.name.lower().replace('_', ' ')
            }
            for et in ExampleType
        ]
    }

@router.get("/supported-interests")
async def get_supported_user_interests():
    """
    Get list of supported user interests
    """
    return {
        "supported_interests": [
            {
                "interest": ui.value,
                "description": ui.name.lower().replace('_', ' ')
            }
            for ui in UserInterest
        ]
    }