"""
Context retrieval precision validation for the RAG system
This script validates that the system retrieves relevant content for queries
"""

import asyncio
from typing import List, Dict, Tuple
from langchain.docstore.document import Document

class RetrievalValidator:
    """Class to validate the precision of context retrieval"""

    def __init__(self, vector_store):
        self.vector_store = vector_store

    async def validate_single_retrieval(self, query: str, expected_content_keywords: List[str]) -> Dict:
        """Validate retrieval precision for a single query"""
        try:
            # Retrieve relevant documents
            docs = self.vector_store.similarity_search(query, k=4)

            # Check how many retrieved docs contain expected keywords
            relevant_docs = 0
            total_keywords_found = 0

            retrieval_results = []

            for i, doc in enumerate(docs):
                doc_content = doc.page_content.lower()
                doc_keywords_found = []

                for keyword in expected_content_keywords:
                    if keyword.lower() in doc_content:
                        doc_keywords_found.append(keyword)
                        total_keywords_found += 1

                is_relevant = len(doc_keywords_found) > 0
                if is_relevant:
                    relevant_docs += 1

                retrieval_results.append({
                    "doc_rank": i + 1,
                    "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata,
                    "keywords_found": doc_keywords_found,
                    "is_relevant": is_relevant
                })

            # Calculate precision metrics
            precision_at_k = relevant_docs / len(docs) if docs else 0
            keyword_coverage = total_keywords_found / len(expected_content_keywords) if expected_content_keywords else 0

            # Calculate average relevance score
            avg_keyword_density = total_keywords_found / len(docs) if docs else 0

            result = {
                "query": query,
                "expected_keywords": expected_content_keywords,
                "retrieved_docs_count": len(docs),
                "relevant_docs_count": relevant_docs,
                "precision_at_k": precision_at_k,
                "keyword_coverage": keyword_coverage,
                "avg_keyword_density": avg_keyword_density,
                "retrieval_results": retrieval_results,
                "passed": precision_at_k >= 0.5,  # Consider passed if 50%+ of retrieved docs are relevant
                "quality_score": min(1.0, precision_at_k + keyword_coverage) / 2  # Average of both metrics
            }

            return result

        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "passed": False,
                "quality_score": 0.0
            }

    async def run_retrieval_validation(self) -> Dict:
        """Run comprehensive retrieval validation tests"""

        # Test queries with expected content keywords
        validation_tests = [
            {
                "query": "What is Physical AI and embodied cognition?",
                "expected_keywords": ["physical ai", "embodied", "intelligence", "body", "environment", "interaction"]
            },
            {
                "query": "Explain the sensorimotor loop in robotics",
                "expected_keywords": ["sensorimotor", "loop", "sensing", "processing", "acting", "cycle"]
            },
            {
                "query": "How do humanoid robots maintain balance?",
                "expected_keywords": ["balance", "zmp", "stability", "control", "bipedal", "walking"]
            },
            {
                "query": "What is morphological computation?",
                "expected_keywords": ["morphological", "computation", "physical", "form", "intelligence", "body"]
            },
            {
                "query": "Explain the symbol grounding problem",
                "expected_keywords": ["symbol", "grounding", "problem", "abstract", "reality", "connection"]
            },
            {
                "query": "How does perception work in robotics?",
                "expected_keywords": ["perception", "sensing", "sensors", "environment", "awareness"]
            },
            {
                "query": "What are the key principles of Physical AI?",
                "expected_keywords": ["principles", "physical ai", "embodied", "interaction", "intelligence"]
            },
            {
                "query": "How do robots learn from physical interaction?",
                "expected_keywords": ["learning", "physical", "interaction", "experience", "adaptation"]
            }
        ]

        results = {
            "total_tests": len(validation_tests),
            "passed_tests": 0,
            "failed_tests": 0,
            "average_precision": 0.0,
            "average_quality_score": 0.0,
            "detailed_results": []
        }

        total_precision = 0
        total_quality = 0

        print("Running Context Retrieval Validation Tests...")

        for i, test in enumerate(validation_tests):
            print(f"Validating retrieval {i+1}/{len(validation_tests)}: '{test['query']}'")

            result = await self.validate_single_retrieval(
                test["query"],
                test["expected_keywords"]
            )

            results["detailed_results"].append(result)

            if result["passed"]:
                results["passed_tests"] += 1
                total_precision += result["precision_at_k"]
                total_quality += result["quality_score"]
                print(f"  ✓ PASSED (Precision: {result['precision_at_k']:.2f}, Quality: {result['quality_score']:.2f})")
            else:
                results["failed_tests"] += 1
                print(f"  ✗ FAILED (Precision: {result['precision_at_k']:.2f}, Quality: {result['quality_score']:.2f})")

        # Calculate overall metrics
        if results["passed_tests"] > 0:
            results["average_precision"] = total_precision / results["passed_tests"]
            results["average_quality_score"] = total_quality / results["passed_tests"]
        else:
            results["average_precision"] = 0
            results["average_quality_score"] = 0

        # Overall success if majority of tests pass and average precision is acceptable
        results["overall_passed"] = (
            results["passed_tests"] >= results["total_tests"] * 0.6 and  # 60%+ tests pass
            results["average_precision"] >= 0.5  # Average precision >= 50%
        )

        print(f"\nRetrieval Validation Summary:")
        print(f"  Total Tests: {results['total_tests']}")
        print(f"  Passed: {results['passed_tests']}")
        print(f"  Failed: {results['failed_tests']}")
        print(f"  Average Precision: {results['average_precision']:.2f}")
        print(f"  Average Quality Score: {results['average_quality_score']:.2f}")
        print(f"  Overall Status: {'✓ PASSED' if results['overall_passed'] else '✗ FAILED'}")

        return results

async def main():
    """Main function to run retrieval validation"""
    print("Starting Context Retrieval Precision Validation...")

    # Import required modules
    from app.config import settings
    from langchain.vectorstores import Chroma
    from langchain.embeddings import OpenAIEmbeddings

    try:
        # Initialize vector store
        embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
        vector_store = Chroma(
            persist_directory=settings.vector_db_path,
            collection_name=settings.collection_name,
            embedding_function=embeddings
        )

        # Create validator and run tests
        validator = RetrievalValidator(vector_store)
        results = await validator.run_retrieval_validation()

        # Save results to file
        import json
        with open("retrieval_validation_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\nValidation results saved to retrieval_validation_results.json")

        return results["overall_passed"]

    except Exception as e:
        print(f"Error running retrieval validation: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)