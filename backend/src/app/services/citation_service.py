import asyncio
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import re
from urllib.parse import urlparse
import aiohttp

logger = logging.getLogger(__name__)

@dataclass
class Citation:
    id: str
    text: str
    url: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    year: Optional[int] = None
    verified: bool = False
    verification_details: Optional[Dict] = None

@dataclass
class VerificationResult:
    citation_id: str
    is_valid: bool
    confidence: float
    verification_notes: List[str]

class CitationVerificationService:
    """Service for verifying citations and references in the book content"""

    def __init__(self):
        self.citation_pattern = r'\[(\d+)\]'  # Matches [1], [2], etc.
        self.url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.verified_citations = {}  # Cache of verified citations

    async def extract_citations(self, text: str) -> List[str]:
        """Extract citation references from text"""
        citations = re.findall(self.citation_pattern, text)
        return list(set(citations))  # Return unique citations

    async def verify_single_citation(
        self,
        citation_id: str,
        bibliography: Dict[str, Citation]
    ) -> VerificationResult:
        """Verify a single citation against the bibliography"""
        if citation_id in self.verified_citations:
            return self.verified_citations[citation_id]

        notes = []
        is_valid = False
        confidence = 0.0

        if citation_id not in bibliography:
            notes.append(f"Citation [{citation_id}] not found in bibliography")
        else:
            citation = bibliography[citation_id]
            is_valid = True
            confidence = 1.0
            notes.append(f"Citation [{citation_id}] found in bibliography")

            # Verify URL if present
            if citation.url:
                url_valid = await self._verify_url(citation.url)
                if url_valid:
                    notes.append(f"URL for citation [{citation_id}] is accessible")
                    confidence = 0.9
                else:
                    notes.append(f"URL for citation [{citation_id}] is not accessible")
                    is_valid = False
                    confidence = 0.3

        result = VerificationResult(
            citation_id=citation_id,
            is_valid=is_valid,
            confidence=confidence,
            verification_notes=notes
        )

        self.verified_citations[citation_id] = result
        return result

    async def _verify_url(self, url: str) -> bool:
        """Verify that a URL is accessible"""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url) as response:
                    return response.status == 200
        except Exception as e:
            logger.warning(f"URL verification failed for {url}: {str(e)}")
            return False

    async def verify_citations_in_text(
        self,
        text: str,
        bibliography: Dict[str, Citation]
    ) -> List[VerificationResult]:
        """Verify all citations found in a text against the bibliography"""
        citation_ids = await self.extract_citations(text)
        results = []

        # Process citations concurrently for better performance
        tasks = [
            self.verify_single_citation(cid, bibliography)
            for cid in citation_ids
        ]

        results = await asyncio.gather(*tasks)
        return results

    async def build_bibliography_from_files(self, bibliography_paths: List[str]) -> Dict[str, Citation]:
        """Build a bibliography dictionary from bibliography files"""
        bibliography = {}

        for path in bibliography_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse citations from bibliography file
                # This is a simplified parser - a real implementation would be more sophisticated
                lines = content.split('\n')
                for line in lines:
                    # Look for patterns like [1], [2], etc.
                    match = re.match(r'\[(\d+)\]\s*(.*)', line.strip())
                    if match:
                        citation_id = match.group(1)
                        citation_text = match.group(2)

                        # Extract URL if present
                        urls = re.findall(self.url_pattern, citation_text)
                        url = urls[0] if urls else None

                        bibliography[citation_id] = Citation(
                            id=citation_id,
                            text=citation_text,
                            url=url
                        )

            except Exception as e:
                logger.error(f"Error reading bibliography file {path}: {str(e)}")

        return bibliography

    async def verify_content_citations(
        self,
        content: str,
        bibliography: Dict[str, Citation]
    ) -> Dict[str, any]:
        """Verify all citations in content and return comprehensive report"""
        # Extract all citations from content
        citation_ids = await self.extract_citations(content)

        # Verify each citation
        verification_results = await self.verify_citations_in_text(content, bibliography)

        # Calculate overall statistics
        total_citations = len(citation_ids)
        valid_citations = sum(1 for result in verification_results if result.is_valid)
        avg_confidence = sum(result.confidence for result in verification_results) / len(verification_results) if verification_results else 0

        report = {
            "total_citations_found": total_citations,
            "valid_citations": valid_citations,
            "invalid_citations": total_citations - valid_citations,
            "verification_success_rate": valid_citations / total_citations if total_citations > 0 else 0,
            "average_confidence": avg_confidence,
            "detailed_results": [
                {
                    "citation_id": result.citation_id,
                    "is_valid": result.is_valid,
                    "confidence": result.confidence,
                    "notes": result.verification_notes
                }
                for result in verification_results
            ],
            "content_has_issues": (total_citations - valid_citations) > 0
        }

        return report

    async def get_citation_suggestions(
        self,
        text: str,
        bibliography: Dict[str, Citation]
    ) -> List[Dict[str, any]]:
        """Provide suggestions for missing citations in text"""
        citation_ids = await self.extract_citations(text)
        suggestions = []

        # Find technical terms that might need citations
        technical_terms = [
            "Physical AI", "embodied AI", "sensorimotor loop", "morphological computation",
            "symbol grounding", "embodied cognition", "humanoid robotics", "balance control"
        ]

        for term in technical_terms:
            if term.lower() in text.lower():
                # Check if there's a relevant citation in the bibliography
                relevant_citations = [
                    cid for cid, citation in bibliography.items()
                    if term.lower() in citation.text.lower()
                ]

                if not relevant_citations:
                    suggestions.append({
                        "term": term,
                        "suggestion": f"The term '{term}' might benefit from a citation",
                        "type": "missing_citation"
                    })

        return suggestions

# Global instance of the citation verification service
citation_service = CitationVerificationService()