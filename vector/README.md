# Vector Database for Physical AI & Humanoid Robotics Book RAG System

## Overview
This directory contains the vector database for the RAG (Retrieval-Augmented Generation) system. The vector database stores embedded chunks of the book content to enable semantic search and contextual question answering.

## Architecture
- **Database**: ChromaDB (persistent vector store)
- **Embeddings**: OpenAI text-embedding-ada-002
- **Chunking Strategy**: Recursive character splitting with overlap
- **Storage**: Local persistent storage (can be moved to cloud in production)

## Configuration
The vector database is configured through environment variables in the backend:

- `VECTOR_DB_PATH`: Path to the vector database (default: "./vector_db")
- `COLLECTION_NAME`: Name of the collection (default: "book_content")
- `MAX_CHUNK_SIZE`: Maximum size of text chunks (default: 1000 characters)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200 characters)

## Implementation Details
- Book content is automatically loaded from the `content/` directory
- Documents are split into chunks to maintain context while enabling efficient retrieval
- Each chunk is embedded using OpenAI's embedding model
- The vector store is initialized on first API request
- Content is processed in markdown format, preserving structural information

## Performance Considerations
- Vector database is optimized for semantic search of book content
- Retrieval uses similarity search to find relevant content chunks
- Top-k retrieval (default k=4) balances relevance and performance
- The system handles both general questions and selected-text queries

## Maintenance
The vector database will automatically update when new content is added to the `content/` directory. Simply restart the backend service to reprocess all content.