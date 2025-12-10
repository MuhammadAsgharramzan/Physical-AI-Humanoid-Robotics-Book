from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
import logging

from ..services.citation_service import citation_service, Citation, VerificationResult

router = APIRouter(prefix="/api/citation", tags=["citation-verification"])

logger = logging.getLogger(__name__)

@router.post("/verify-content")
async def verify_content_citations(
    content: str,
    bibliography: Dict[str, str]  # Simple dict of citation_id -> citation_text for now
):
    """
    Verify all citations in content against the provided bibliography
    """
    try:
        # Convert bibliography dict to Citation objects
        bibliography_objects = {}
        for cid, text in bibliography.items():
            bibliography_objects[cid] = Citation(
                id=cid,
                text=text,
                url=None  # URL would be extracted from the citation text if available
            )

        report = await citation_service.verify_content_citations(content, bibliography_objects)

        return report

    except Exception as e:
        logger.error(f"Citation verification error: {str(e)}")
        raise HTTPException(status_code=500, detail="Citation verification failed")

@router.post("/verify-citations")
async def verify_citations(
    text: str,
    bibliography: Dict[str, str]
):
    """
    Verify specific citations in text against bibliography
    """
    try:
        # Convert bibliography dict to Citation objects
        bibliography_objects = {}
        for cid, text_citation in bibliography.items():
            bibliography_objects[cid] = Citation(
                id=cid,
                text=text_citation
            )

        results = await citation_service.verify_citations_in_text(text, bibliography_objects)

        return {
            "verification_results": [
                {
                    "citation_id": result.citation_id,
                    "is_valid": result.is_valid,
                    "confidence": result.confidence,
                    "notes": result.verification_notes
                }
                for result in results
            ]
        }

    except Exception as e:
        logger.error(f"Citation verification error: {str(e)}")
        raise HTTPException(status_code=500, detail="Citation verification failed")

@router.post("/get-suggestions")
async def get_citation_suggestions(
    content: str,
    bibliography: Dict[str, str]
):
    """
    Get suggestions for missing citations in content
    """
    try:
        # Convert bibliography dict to Citation objects
        bibliography_objects = {}
        for cid, text in bibliography.items():
            bibliography_objects[cid] = Citation(
                id=cid,
                text=text
            )

        suggestions = await citation_service.get_citation_suggestions(content, bibliography_objects)

        return {"suggestions": suggestions}

    except Exception as e:
        logger.error(f"Citation suggestions error: {str(e)}")
        raise HTTPException(status_code=500, detail="Citation suggestions failed")

@router.get("/extract-citations")
async def extract_citations(text: str = Query(..., description="Text to extract citations from")):
    """
    Extract citation references from text
    """
    try:
        citations = await citation_service.extract_citations(text)
        return {"citations": citations}
    except Exception as e:
        logger.error(f"Citation extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Citation extraction failed")