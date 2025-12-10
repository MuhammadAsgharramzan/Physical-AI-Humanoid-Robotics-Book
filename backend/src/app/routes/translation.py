from fastapi import APIRouter, HTTPException
from typing import List, Union
import logging

from ..services.translation_service import translation_service, Language, TranslationResult

router = APIRouter(prefix="/api/translation", tags=["translation"])

logger = logging.getLogger(__name__)

@router.post("/translate", response_model=TranslationResult)
async def translate_text(
    text: str,
    source_lang: str = "en",
    target_lang: str = "ur"
):
    """
    Translate text from source language to target language
    """
    try:
        # Validate language codes
        try:
            source_language = Language(source_lang.lower())
            target_language = Language(target_lang.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid language code. Supported languages: {[lang.value for lang in Language]}"
            )

        result = await translation_service.translate_text(
            text, source_language, target_language
        )

        return result

    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation failed")

@router.post("/translate-content")
async def translate_content(
    content: Union[str, List[str]],
    source_lang: str = "en",
    target_lang: str = "ur"
):
    """
    Translate content (string or list of strings) from source language to target language
    """
    try:
        # Validate language codes
        try:
            source_language = Language(source_lang.lower())
            target_language = Language(target_lang.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid language code. Supported languages: {[lang.value for lang in Language]}"
            )

        result = await translation_service.translate_content(
            content, source_language, target_language
        )

        return {"translated_content": result}

    except Exception as e:
        logger.error(f"Content translation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Content translation failed")

@router.post("/batch-translate")
async def batch_translate(
    texts: List[str],
    source_lang: str = "en",
    target_lang: str = "ur"
):
    """
    Translate multiple texts from source language to target language
    """
    try:
        # Validate language codes
        try:
            source_language = Language(source_lang.lower())
            target_language = Language(target_lang.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid language code. Supported languages: {[lang.value for lang in Language]}"
            )

        results = await translation_service.batch_translate(
            texts, source_language, target_language
        )

        return {
            "translations": [
                {
                    "source_text": r.source_text,
                    "translated_text": r.translated_text,
                    "confidence": r.confidence
                }
                for r in results
            ]
        }

@router.get("/supported-languages")
async def get_supported_languages():
    """
    Get list of supported languages for translation
    """
    return {
        "supported_languages": [
            {
                "code": lang.value,
                "name": lang.name
            }
            for lang in Language
        ]
    }