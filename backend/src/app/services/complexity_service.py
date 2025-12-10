import asyncio
import logging
from typing import Dict, List, Optional, Union
from enum import Enum
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

class ComplexityLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class ComplexityAdjustment:
    original_content: str
    adjusted_content: str
    original_complexity: ComplexityLevel
    target_complexity: ComplexityLevel
    adjustment_confidence: float

class ComplexityAdjustmentService:
    """Service for adjusting content complexity based on user profile"""

    def __init__(self):
        # Define complexity indicators and their mappings
        self.technical_terms = {
            # Beginner-friendly alternatives for advanced terms
            "morphological computation": {
                "beginner": "how a robot's physical form helps it think",
                "intermediate": "how body structure contributes to intelligence",
                "advanced": "morphological computation"
            },
            "sensorimotor loop": {
                "beginner": "the cycle of sensing, thinking, and acting",
                "intermediate": "sensory-motor feedback cycle",
                "advanced": "sensorimotor loop"
            },
            "embodied cognition": {
                "beginner": "how thinking happens through body interaction",
                "intermediate": "body-based cognition",
                "advanced": "embodied cognition"
            },
            "symbol grounding problem": {
                "beginner": "how words connect to real experiences",
                "intermediate": "symbol-reality connection challenge",
                "advanced": "symbol grounding problem"
            },
            "zero moment point": {
                "beginner": "balance point for walking robots",
                "intermediate": "ZMP for stability control",
                "advanced": "zero moment point (ZMP)"
            }
        }

        # Define sentence complexity patterns
        self.complexity_patterns = {
            "beginner": {
                "sentence_structure": r".*[,;].*[,:].*",  # Complex sentences with multiple clauses
                "technical_density": 0.3,  # Max percentage of technical terms
                "average_sentence_length": 15  # Max words per sentence
            },
            "intermediate": {
                "sentence_structure": r".*[,;].*",  # Moderate complexity
                "technical_density": 0.5,
                "average_sentence_length": 25
            },
            "advanced": {
                "sentence_structure": r".*",  # Any structure
                "technical_density": 0.8,
                "average_sentence_length": 50
            }
        }

    async def adjust_content_complexity(
        self,
        content: str,
        user_complexity_level: ComplexityLevel
    ) -> ComplexityAdjustment:
        """
        Adjust content complexity based on user profile
        """
        original_complexity = self.estimate_content_complexity(content)

        if original_complexity == user_complexity_level:
            # No adjustment needed
            return ComplexityAdjustment(
                original_content=content,
                adjusted_content=content,
                original_complexity=original_complexity,
                target_complexity=user_complexity_level,
                adjustment_confidence=1.0
            )

        # Apply complexity adjustment
        adjusted_content = await self._apply_complexity_adjustment(
            content,
            original_complexity,
            user_complexity_level
        )

        return ComplexityAdjustment(
            original_content=content,
            adjusted_content=adjusted_content,
            original_complexity=original_complexity,
            target_complexity=user_complexity_level,
            adjustment_confidence=0.8  # Confidence in adjustment
        )

    def estimate_content_complexity(self, content: str) -> ComplexityLevel:
        """
        Estimate the complexity level of content
        """
        # Analyze content for complexity indicators
        technical_term_count = 0
        total_words = len(content.split())

        for term in self.technical_terms.keys():
            if term.lower() in content.lower():
                technical_term_count += 1

        # Calculate technical density
        technical_density = technical_term_count / max(total_words / 100, 1)  # Terms per 100 words

        # Estimate complexity based on technical density and sentence structure
        if technical_density < 0.2:
            return ComplexityLevel.BEGINNER
        elif technical_density < 0.5:
            return ComplexityLevel.INTERMEDIATE
        else:
            return ComplexityLevel.ADVANCED

    async def _apply_complexity_adjustment(
        self,
        content: str,
        original_complexity: ComplexityLevel,
        target_complexity: ComplexityLevel
    ) -> str:
        """
        Apply the actual complexity adjustment to content
        """
        adjusted_content = content

        # Adjust based on direction (simplifying vs. making more complex)
        if target_complexity == ComplexityLevel.BEGINNER:
            # Simplify content
            adjusted_content = await self._simplify_content(adjusted_content)
        elif target_complexity == ComplexityLevel.ADVANCED:
            # Make content more complex/technical
            adjusted_content = await self._complexify_content(adjusted_content)
        else:
            # Intermediate - balance technical and accessible
            adjusted_content = await self._balance_content(adjusted_content)

        return adjusted_content

    async def _simplify_content(self, content: str) -> str:
        """
        Simplify content by replacing technical terms with simpler explanations
        """
        adjusted = content

        # Replace technical terms with beginner-friendly alternatives
        for term, alternatives in self.technical_terms.items():
            if term.lower() in adjusted.lower():
                replacement = alternatives.get("beginner", term)
                # Use case-insensitive replacement
                adjusted = re.sub(
                    re.escape(term),
                    replacement,
                    adjusted,
                    flags=re.IGNORECASE
                )

        # Break down complex sentences
        adjusted = self._break_down_sentences(adjusted)

        # Add explanations for technical concepts
        adjusted = self._add_simple_explanations(adjusted)

        return adjusted

    async def _complexify_content(self, content: str) -> str:
        """
        Make content more complex by using technical terminology
        """
        adjusted = content

        # Replace simplified terms with technical equivalents
        for term, alternatives in self.technical_terms.items():
            # Look for simplified versions and replace with technical ones
            simplified_version = alternatives.get("beginner", term)
            if simplified_version.lower() in adjusted.lower():
                adjusted = re.sub(
                    re.escape(simplified_version),
                    term,
                    adjusted,
                    flags=re.IGNORECASE
                )

            # Also check intermediate versions
            intermediate_version = alternatives.get("intermediate", term)
            if intermediate_version.lower() in adjusted.lower():
                adjusted = re.sub(
                    re.escape(intermediate_version),
                    term,
                    adjusted,
                    flags=re.IGNORECASE
                )

        return adjusted

    async def _balance_content(self, content: str) -> str:
        """
        Balance content between technical and accessible
        """
        adjusted = content

        # Replace terms with intermediate alternatives
        for term, alternatives in self.technical_terms.items():
            if term.lower() in adjusted.lower():
                replacement = alternatives.get("intermediate", term)
                adjusted = re.sub(
                    re.escape(term),
                    replacement,
                    adjusted,
                    flags=re.IGNORECASE
                )

        return adjusted

    def _break_down_sentences(self, content: str) -> str:
        """
        Break down complex sentences into simpler ones
        """
        # This is a simplified implementation
        # In a real system, this would use NLP techniques
        sentences = re.split(r'[.!?]+', content)
        simplified_sentences = []

        for sentence in sentences:
            if len(sentence.split()) > 30:  # If sentence is too long
                # Try to break it at natural clause boundaries
                sub_sentences = re.split(r'[,;]', sentence)
                for sub in sub_sentences:
                    if sub.strip():
                        simplified_sentences.append(sub.strip())
            else:
                if sentence.strip():
                    simplified_sentences.append(sentence.strip())

        return '. '.join(simplified_sentences) + '.'

    def _add_simple_explanations(self, content: str) -> str:
        """
        Add simple explanations for technical concepts
        """
        # Add simple explanations for common technical terms
        explanations = {
            "algorithm": "(a step-by-step procedure for solving problems)",
            "sensor": "(a device that detects and measures physical properties)",
            "actuator": "(a device that moves or controls a mechanism)",
            "feedback": "(information about the result of an action)"
        }

        adjusted = content
        for term, explanation in explanations.items():
            pattern = r'\b(' + re.escape(term) + r')\b'
            adjusted = re.sub(
                pattern,
                f"{term} {explanation}",
                adjusted,
                flags=re.IGNORECASE
            )

        return adjusted

    async def get_complexity_recommendations(
        self,
        content: str,
        user_complexity_level: ComplexityLevel
    ) -> Dict[str, any]:
        """
        Get recommendations for content complexity adjustments
        """
        original_complexity = self.estimate_content_complexity(content)

        recommendations = {
            "current_complexity": original_complexity.value,
            "user_complexity_level": user_complexity_level.value,
            "needs_adjustment": original_complexity != user_complexity_level,
            "recommendation": "No adjustment needed" if original_complexity == user_complexity_level else "Adjust content complexity",
            "suggested_terms_to_replace": [],
            "suggested_sentence_modifications": []
        }

        if original_complexity != user_complexity_level:
            # Identify specific terms that could be adjusted
            for term in self.technical_terms.keys():
                if term.lower() in content.lower():
                    alternatives = self.technical_terms[term]
                    target_alternative = alternatives.get(user_complexity_level.value, term)
                    if target_alternative != term:
                        recommendations["suggested_terms_to_replace"].append({
                            "original": term,
                            "suggestion": target_alternative
                        })

        return recommendations

# Global instance of the complexity adjustment service
complexity_service = ComplexityAdjustmentService()