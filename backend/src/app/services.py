import os
import logging
from typing import List, Dict, Any
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
import asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from .config import settings

logger = logging.getLogger(__name__)

class ContentProcessor:
    """Service for processing and indexing book content"""

    def __init__(self):
        self.content_dir = Path(settings.content_directory)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.max_chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

    async def load_content_from_markdown(self) -> List[Document]:
        """Load and parse all markdown content from the book"""
        documents = []

        # Find all markdown files in content directory
        for md_file in self.content_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Convert markdown to plain text for better processing
                html = markdown.markdown(content)
                text = BeautifulSoup(html, 'html.parser').get_text()

                # Create document
                doc = Document(
                    page_content=text,
                    metadata={
                        "source": str(md_file.relative_to(self.content_dir)),
                        "title": md_file.name,
                        "module": str(md_file.parent.relative_to(self.content_dir))
                    }
                )
                documents.append(doc)

                logger.info(f"Loaded document: {md_file}")

            except Exception as e:
                logger.error(f"Error loading document {md_file}: {str(e)}")

        return documents

    async def create_vector_store(self) -> Chroma:
        """Create and populate vector store with book content"""
        try:
            # Load content
            documents = await self.load_content_from_markdown()

            # Split documents
            texts = self.text_splitter.split_documents(documents)

            # Create vector store
            vector_store = Chroma.from_documents(
                texts,
                self.embeddings,
                persist_directory=settings.vector_db_path,
                collection_name=settings.collection_name
            )

            logger.info(f"Created vector store with {len(texts)} chunks")
            return vector_store

        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise

class RAGService:
    """Service for RAG (Retrieval-Augmented Generation) functionality"""

    def __init__(self, vector_store: Chroma):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            model_name=settings.openai_model,
            temperature=0.3,
            openai_api_key=settings.openai_api_key
        )

        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(
                search_kwargs={"k": 4}  # Retrieve top 4 relevant chunks
            ),
            return_source_documents=True
        )

        # Custom prompt template for book content
        self.custom_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            You are an expert assistant for the Physical AI & Humanoid Robotics book.
            Use the following context to answer the question.
            If the context doesn't contain the answer, say so.

            Context: {context}

            Question: {question}

            Answer concisely with references to the book content where possible:
            """
        )

    async def answer_question(self, question: str, selected_text: str = None) -> Dict[str, Any]:
        """Answer a question using the RAG system"""
        try:
            # Prepare the query - if there's selected text, include it
            query = question
            if selected_text:
                query = f"Regarding '{selected_text}', {question.lower()}"

            # Get response from QA chain
            response = self.qa_chain({"query": query})

            # Extract answer and sources
            answer = response["result"]
            source_docs = response.get("source_documents", [])

            # Extract source information
            sources = []
            for doc in source_docs:
                source_info = doc.metadata.get("source", "Unknown")
                if source_info not in sources:
                    sources.append(source_info)

            # Calculate confidence based on source relevance
            confidence = min(0.9, 0.5 + len(source_docs) * 0.1)

            # Check if the answer seems to indicate lack of knowledge in the book content
            # If so, implement fallback to general knowledge
            if (len(source_docs) == 0 or
                "I don't have specific information about this in the book" in answer or
                "not mentioned in the provided context" in answer.lower() or
                "not found in the book content" in answer.lower()):

                # Fallback to general knowledge using the LLM directly
                fallback_prompt = f"""
                You are an AI assistant for the Physical AI & Humanoid Robotics book.
                The user asked: "{question}"

                Although this specific information wasn't found in the book content,
                please provide a helpful response based on general knowledge about
                robotics, AI, and humanoid systems. Keep your response relevant to
                the book's topics when possible.
                """

                from langchain import LLMChain
                from langchain.prompts import PromptTemplate

                fallback_prompt_template = PromptTemplate(
                    input_variables=["question"],
                    template=fallback_prompt
                )

                # Create a simple chain for fallback
                fallback_chain = LLMChain(
                    llm=self.llm,
                    prompt=fallback_prompt_template
                )

                fallback_response = await fallback_chain.arun(question=question)

                return {
                    "answer": f"{answer} Additionally, based on general knowledge: {fallback_response}",
                    "sources": ["General knowledge fallback"],
                    "confidence": 0.3  # Lower confidence for fallback responses
                }

            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence
            }

        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {
                "answer": "I encountered an error processing your question. Please try again.",
                "sources": [],
                "confidence": 0.0
            }