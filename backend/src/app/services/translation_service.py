import asyncio
import logging
from typing import List, Dict, Optional, Union
from enum import Enum
from dataclasses import dataclass

from ..config import settings

logger = logging.getLogger(__name__)

class Language(Enum):
    ENGLISH = "en"
    URDU = "ur"

@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Language
    target_language: Language
    confidence: float

class TranslationService:
    """Service for translating content between English and Urdu"""

    def __init__(self):
        # In a real implementation, this would connect to a translation API
        # For now, we'll use a mock implementation with some common terms
        self.translation_cache = {}
        self.common_translations = {
            # Technical terms
            "Physical AI": "جسمانی مصنوعی ذہانت",
            "Embodied AI": "جسمانی مصنوعی ذہانت",
            "Humanoid Robotics": "انسان نما روبوٹکس",
            "Sensorimotor Loop": "حسی-حرکتی حلقہ",
            "Morphological Computation": "جسمانی معلوماتی تکنیک",
            "Symbol Grounding": "علامتی بنیاد",
            "Embodied Cognition": "جسمانی شعور",
            "Human-Robot Interaction": "انسان-روبوٹ تعامل",
            "Balance Control": "توازن کنٹرول",
            "Locomotion": "چلنے کی صلاحیت",

            # Common terms
            "Introduction": "تعارف",
            "Concept": "تصور",
            "Principle": "اصول",
            "System": "سسٹم",
            "Technology": "ٹیکنالوجی",
            "Application": "اطلاق",
            "Implementation": "نافذ کرنا",
            "Development": "تعمیر",
            "Research": "تحقیق",
            "Study": "مطالعہ",
        }

        # Reverse translations
        self.reverse_translations = {v: k for k, v in self.common_translations.items()}

    async def translate_text(
        self,
        text: str,
        source_lang: Language,
        target_lang: Language
    ) -> TranslationResult:
        """
        Translate text from source language to target language
        """
        if source_lang == target_lang:
            return TranslationResult(
                source_text=text,
                translated_text=text,
                source_language=source_lang,
                target_language=target_lang,
                confidence=1.0
            )

        # Check cache first
        cache_key = f"{text}_{source_lang.value}_{target_lang.value}"
        if cache_key in self.translation_cache:
            cached = self.translation_cache[cache_key]
            return TranslationResult(
                source_text=text,
                translated_text=cached,
                source_language=source_lang,
                target_language=target_lang,
                confidence=0.9
            )

        # Perform translation based on direction
        if source_lang == Language.ENGLISH and target_lang == Language.URDU:
            translated = await self._translate_en_to_ur(text)
        elif source_lang == Language.URDU and target_lang == Language.ENGLISH:
            translated = await self._translate_ur_to_en(text)
        else:
            raise ValueError(f"Unsupported translation direction: {source_lang} -> {target_lang}")

        # Cache the result
        self.translation_cache[cache_key] = translated

        return TranslationResult(
            source_text=text,
            translated_text=translated,
            source_language=source_lang,
            target_language=target_lang,
            confidence=0.8  # Confidence based on translation method
        )

    async def _translate_en_to_ur(self, text: str) -> str:
        """
        Translate English text to Urdu
        In a real implementation, this would use an AI translation service
        """
        # First, try to find and replace common terms
        result = text

        # Sort by length (descending) to replace longer phrases first
        sorted_terms = sorted(self.common_translations.items(), key=lambda x: len(x[0]), reverse=True)

        for en_term, ur_term in sorted_terms:
            result = result.replace(en_term, ur_term)

        # For a more sophisticated implementation, we would call an actual translation API
        # This is a simplified version for demonstration
        if settings.openai_api_key:
            # Use OpenAI for translation if available
            try:
                from langchain.chat_models import ChatOpenAI
                from langchain.prompts import ChatPromptTemplate

                llm = ChatOpenAI(
                    model_name=settings.openai_model,
                    temperature=0.3,
                    openai_api_key=settings.openai_api_key
                )

                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a professional translator. Translate the following English text to Urdu. Maintain technical accuracy and use appropriate Urdu terminology for technical concepts."),
                    ("user", text)
                ])

                chain = prompt | llm
                result = await chain.ainvoke({})

                # Extract content from the response
                if hasattr(result, 'content'):
                    result = result.content
                else:
                    result = str(result)

            except Exception as e:
                logger.warning(f"OpenAI translation failed: {e}. Using fallback translation.")
                # Fallback to dictionary-based translation

        return result

    async def _translate_ur_to_en(self, text: str) -> str:
        """
        Translate Urdu text to English
        In a real implementation, this would use an AI translation service
        """
        # First, try to find and replace common terms
        result = text

        # Sort by length (descending) to replace longer phrases first
        sorted_terms = sorted(self.reverse_translations.items(), key=lambda x: len(x[0]), reverse=True)

        for ur_term, en_term in sorted_terms:
            result = result.replace(ur_term, en_term)

        # For a more sophisticated implementation, we would call an actual translation API
        if settings.openai_api_key:
            # Use OpenAI for translation if available
            try:
                from langchain.chat_models import ChatOpenAI
                from langchain.prompts import ChatPromptTemplate

                llm = ChatOpenAI(
                    model_name=settings.openai_model,
                    temperature=0.3,
                    openai_api_key=settings.openai_api_key
                )

                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a professional translator. Translate the following Urdu text to English. Maintain technical accuracy and preserve the original meaning."),
                    ("user", text)
                ])

                chain = prompt | llm
                result = await chain.ainvoke({})

                # Extract content from the response
                if hasattr(result, 'content'):
                    result = result.content
                else:
                    result = str(result)

            except Exception as e:
                logger.warning(f"OpenAI translation failed: {e}. Using fallback translation.")
                # Fallback to dictionary-based translation

        return result

    async def translate_content(
        self,
        content: Union[str, List[str]],
        source_lang: Language,
        target_lang: Language
    ) -> Union[str, List[str]]:
        """
        Translate content which could be a single string or a list of strings
        """
        if isinstance(content, list):
            translated_list = []
            for item in content:
                result = await self.translate_text(item, source_lang, target_lang)
                translated_list.append(result.translated_text)
            return translated_list
        else:
            result = await self.translate_text(content, source_lang, target_lang)
            return result.translated_text

    async def batch_translate(
        self,
        texts: List[str],
        source_lang: Language,
        target_lang: Language
    ) -> List[TranslationResult]:
        """
        Translate multiple texts efficiently
        """
        tasks = [
            self.translate_text(text, source_lang, target_lang)
            for text in texts
        ]
        return await asyncio.gather(*tasks)

# Global instance of the translation service
translation_service = TranslationService()