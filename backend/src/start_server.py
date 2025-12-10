#!/usr/bin/env python3
"""
Start script for the Physical AI & Humanoid Robotics Book RAG Chatbot
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the app directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings

def main():
    print("Starting Physical AI & Humanoid Robotics Book RAG Chatbot...")
    print(f"Host: {settings.host}")
    print(f"Port: {settings.port}")
    print(f"API Version: {settings.app_version}")
    print(f"Content Directory: {settings.content_directory}")
    print(f"Vector DB Path: {settings.vector_db_path}")

    # Run the server
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,  # Set to False in production
        log_level="info"
    )

if __name__ == "__main__":
    main()