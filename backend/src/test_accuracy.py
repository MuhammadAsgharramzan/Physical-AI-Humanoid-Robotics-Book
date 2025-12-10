"""
Accuracy testing for the RAG chatbot system
This script tests the response accuracy with known answers
"""

import asyncio
import json
from typing import List, Dict, Tuple

# Test questions with expected answers based on the book content
TEST_QUESTIONS = [
    {
        "question": "What is Physical AI?",
        "expected_topics": ["embodied AI", "physical interaction", "intelligence"],
        "description": "Tests basic understanding of Physical AI concept"
    },
    {
        "question": "What is the sensorimotor loop?",
        "expected_topics": ["sensing", "processing", "acting", "cycle"],
        "description": "Tests understanding of sensorimotor loop concept"
    },
    {
        "question": "Explain morphological computation",
        "expected_topics": ["physical form", "intelligence", "computation", "body structure"],
        "description": "Tests understanding of morphological computation"
    },
    {
        "question": "What is the symbol grounding problem?",
        "expected_topics": ["symbols", "real-world", "connection", "abstraction"],
        "description": "Tests understanding of symbol grounding problem"
    },
    {
        "question": "How do humanoid robots maintain balance?",
        "expected_topics": ["ZMP", "balance", "stability", "control"],
        "description": "Tests understanding of humanoid balance"
    }
]

class RAGAccuracyTester:
    """Class to test the accuracy of the RAG system"""

    def __init__(self, rag_service):
        self.rag_service = rag_service

    async def test_single_question(self, question: str, expected_topics: List[str]) -> Tuple[bool, Dict]:
        """Test a single question and evaluate response quality"""
        try:
            # Get response from RAG service
            result = await self.rag_service.answer_question(question)

            answer = result.get("answer", "").lower()
            sources = result.get("sources", [])
            confidence = result.get("confidence", 0.0)

            # Check if expected topics are mentioned in the answer
            topic_matches = []
            for topic in expected_topics:
                if topic.lower() in answer:
                    topic_matches.append(topic)

            # Calculate accuracy score based on topic coverage
            accuracy_score = len(topic_matches) / len(expected_topics) if expected_topics else 0

            # Prepare test result
            test_result = {
                "question": question,
                "expected_topics": expected_topics,
                "found_topics": topic_matches,
                "accuracy_score": accuracy_score,
                "confidence": confidence,
                "sources": sources,
                "answer": result.get("answer", ""),
                "passed": accuracy_score >= 0.5,  # Consider test passed if 50%+ topics found
            }

            return test_result["passed"], test_result

        except Exception as e:
            return False, {
                "question": question,
                "error": str(e),
                "passed": False
            }

    async def run_all_tests(self) -> Dict:
        """Run all accuracy tests and return comprehensive results"""
        results = {
            "total_tests": len(TEST_QUESTIONS),
            "passed_tests": 0,
            "failed_tests": 0,
            "details": [],
            "overall_accuracy": 0.0,
            "average_confidence": 0.0
        }

        total_accuracy = 0
        total_confidence = 0

        for i, test in enumerate(TEST_QUESTIONS):
            print(f"Running test {i+1}/{len(TEST_QUESTIONS)}: {test['description']}")

            passed, test_result = await self.test_single_question(
                test["question"],
                test["expected_topics"]
            )

            results["details"].append(test_result)

            if passed:
                results["passed_tests"] += 1
                total_accuracy += test_result["accuracy_score"]
                total_confidence += test_result["confidence"]
                print(f"  ✓ PASSED (Accuracy: {test_result['accuracy_score']:.2f}, Confidence: {test_result['confidence']:.2f})")
            else:
                results["failed_tests"] += 1
                print(f"  ✗ FAILED (Accuracy: {test_result['accuracy_score']:.2f}, Confidence: {test_result['confidence']:.2f})")

        # Calculate overall metrics
        if results["passed_tests"] > 0:
            results["overall_accuracy"] = total_accuracy / results["passed_tests"] if results["passed_tests"] > 0 else 0
            results["average_confidence"] = total_confidence / results["passed_tests"] if results["passed_tests"] > 0 else 0
        else:
            results["overall_accuracy"] = 0
            results["average_confidence"] = 0

        print(f"\nTest Summary:")
        print(f"  Total Tests: {results['total_tests']}")
        print(f"  Passed: {results['passed_tests']}")
        print(f"  Failed: {results['failed_tests']}")
        print(f"  Overall Accuracy: {results['overall_accuracy']:.2f}")
        print(f"  Average Confidence: {results['average_confidence']:.2f}")

        return results

async def main():
    """Main function to run the accuracy tests"""
    print("Starting RAG Chatbot Accuracy Tests...")

    # In a real scenario, we would initialize the actual RAG service
    # For this test, we'll create a mock that simulates the service
    from app.services import ContentProcessor, RAGService
    from langchain.vectorstores import Chroma
    from langchain.embeddings import OpenAIEmbeddings
    from app.config import settings

    try:
        # Initialize content processor
        processor = ContentProcessor()

        # Create or load vector store
        try:
            # Try to load existing vector store
            embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
            vector_store = Chroma(
                persist_directory=settings.vector_db_path,
                collection_name=settings.collection_name,
                embedding_function=embeddings
            )

            # Check if collection is empty
            if len(vector_store._collection.get()['ids']) == 0:
                print("Vector store is empty, creating from content...")
                vector_store = await processor.create_vector_store()
        except:
            # If loading fails, create new vector store from content
            print("Creating new vector store from content...")
            vector_store = await processor.create_vector_store()

        # Initialize RAG service
        rag_service = RAGService(vector_store)

        # Create tester and run tests
        tester = RAGAccuracyTester(rag_service)
        results = await tester.run_all_tests()

        # Save results to file
        with open("accuracy_test_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\nTest results saved to accuracy_test_results.json")

        # Return success if most tests passed
        return results["passed_tests"] >= results["total_tests"] * 0.7  # 70% threshold

    except Exception as e:
        print(f"Error running accuracy tests: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)