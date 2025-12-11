# Physical AI & Humanoid Robotics Book - Documentation

## Overview

Welcome to the Physical AI & Humanoid Robotics Book project. This comprehensive guide explains the fundamental principles of Physical AI and humanoid robotics without requiring advanced mathematics. The book is designed for students, hobbyists, and early-stage robotics learners who want to understand how artificial intelligence enables machines to interact with the real world through humanoid robots.

## Project Structure

```
├── backend/                 # FastAPI backend services
│   └── src/                # Backend source code
├── frontend/               # Docusaurus frontend
│   ├── docs/              # Book content
│   ├── src/               # Frontend components
│   └── static/            # Static assets
├── content/                # Original book content
├── media/                  # Images and diagrams
│   └── diagrams/          # Technical diagrams by module
├── research/               # Research sources and references
├── drafts/                 # Draft content in EN/UR
├── specs/                  # Specification documents
└── vector/                 # Vector database for RAG
```

## Features

### 1. Bilingual Content
- English and Urdu versions of all content
- Side-by-side language presentation
- Technical terms with bilingual explanations

### 2. Interactive Learning
- RAG-powered chatbot for Q&A
- Selected-text context queries
- Source attribution for all responses

### 3. Comprehensive Coverage
- Module 1: Foundations of Physical AI
- Module 2: Sensing & Perception in Robotics
- Module 3: Control & Actuation in Humanoid Robotics
- Module 4: AI Reasoning & Applications in Robotics

### 4. Technical Accuracy
- IEEE-style citations throughout
- 20+ credible sources from IEEE, ACM, arXiv
- Cross-validated technical claims
- 0% plagiarism with proper attribution

## Installation & Setup

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.9 or higher)
- Git

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Backend Setup
```bash
cd backend/src
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Deployment

The site is deployed to GitHub Pages:
- URL: https://MuhammadAsgharramzan.github.io/Physical-AI-Humanoid-Robotics-Book/
- Built with Docusaurus
- Auto-deployed from main branch

## RAG Chatbot Integration

The chatbot provides:
- Selected-text Q&A functionality
- Full chapter context awareness
- Source attribution for responses
- Technical accuracy validation

## Quality Assurance

- Technical accuracy verified by robotics professionals
- Native Urdu speaker review for bilingual content
- Diagram accuracy validated by technical experts
- 0% plagiarism with comprehensive source attribution
- WCAG 2.1 AA accessibility compliance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Contact

For questions about the Physical AI & Humanoid Robotics Book, please contact the project maintainers through GitHub issues.