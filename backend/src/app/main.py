from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
import asyncio
from .config import settings
from .services import ContentProcessor, RAGService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for services
vector_store = None
rag_service = None

app = FastAPI(
    title="Physical AI & Humanoid Robotics Book RAG Chatbot",
    description="Retrieval-Augmented Generation chatbot for interactive learning experience",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    context: Optional[str] = None
    selected_text: Optional[str] = None
    max_tokens: Optional[int] = 500

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

class ChatHistoryItem(BaseModel):
    question: str
    answer: str
    timestamp: str

async def get_rag_service():
    """Dependency to get the RAG service, initializing if needed"""
    global vector_store, rag_service

    if rag_service is None:
        # Initialize content processor
        processor = ContentProcessor()

        # Create or load vector store
        try:
            # Try to load existing vector store
            from langchain_chroma import Chroma
            from langchain_openai import OpenAIEmbeddings

            embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
            vector_store = Chroma(
                persist_directory=settings.vector_db_path,
                collection_name=settings.collection_name,
                embedding_function=embeddings
            )

            # Check if collection is empty
            if len(vector_store._collection.get()['ids']) == 0:
                logger.info("Vector store is empty, creating from content...")
                vector_store = await processor.create_vector_store()
        except:
            # If loading fails, create new vector store from content
            logger.info("Creating new vector store from content...")
            vector_store = await processor.create_vector_store()

        # Initialize RAG service
        rag_service = RAGService(vector_store)

    return rag_service

@app.get("/")
async def root():
    return {"message": "Physical AI & Humanoid Robotics Book RAG Chatbot API"}

@app.post("/api/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest, rag_svc: RAGService = Depends(get_rag_service)):
    """
    Answer a question based on the book content using RAG
    """
    try:
        logger.info(f"Received question: {request.question}")

        # Get answer from RAG service
        result = await rag_svc.answer_question(request.question)

        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"]
        )
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing question")

@app.post("/api/selected-text-ask", response_model=AnswerResponse)
async def ask_about_selected_text(request: QuestionRequest, rag_svc: RAGService = Depends(get_rag_service)):
    """
    Answer a question specifically about selected text in the book
    """
    try:
        logger.info(f"Received selected text question: {request.question} about '{request.selected_text}'")

        # Get answer from RAG service with selected text context
        result = await rag_svc.answer_question(request.question, selected_text=request.selected_text)

        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"]
        )
    except Exception as e:
        logger.error(f"Error processing selected text question: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing selected text question")

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "RAG Chatbot API"}

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting up RAG chatbot service...")
    # Services will be initialized on first request

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)