---
id: 1
title: Update Physical AI Humanoid Constitution
stage: constitution
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Khursheed Computer
command: /sp.constitution
labels: [constitution,book,physical-ai,humanoid-robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: Book titled "Physical AI & Humanoid Robotics"

Core principles:

Technical accuracy grounded in robotics, AI, biomechanics, and control systems

Clarity for mixed audience (beginners + intermediate robotics learners)

Practical relevance (real-world applications, case studies, and implementation insights)

Safety and ethics awareness in AI-driven physical systems

Balanced bilingual accessibility (English + Urdu explanation clarity)

Key standards:

All scientific or engineering claims must reference credible sources (IEEE, ACM, arXiv, journals, robotics textbooks, manufacturer whitepapers)

Citation format: IEEE style

Source types: at least 40% peer-reviewed or academic publications

Diagrams must be technically correct and labeled

Writing style: simple, structured, and concept-first (Flesch-Kincaid grade 8–10 equivalent for English sections)

Urdu sections must prioritize easy comprehension for new learners

Constraints:

Total book length: 5,000–7,000 words

Minimum 25 credible references

Formats:

Primary: PDF + ePub

Secondary: printable A4 version

Content languages: English (main), Urdu (parallel explanations or footnotes)

All technical illustrations must be original or recreated

Success criteria:

Explanations understandable for readers with basic science/tech background

All robotics and AI concepts presented accurately with traceable references

Zero plagiarism detected

Content validated by LLM + robotics domain reasoning

Book suitable for publication and online distribution
```

## Response snapshot

Updated the constitution file with specific principles for the Physical AI & Humanoid Robotics book project, including core principles of technical accuracy, clarity for mixed audiences, practical relevance, safety and ethics awareness, balanced bilingual accessibility, and credible source verification. Added technical standards and development workflow sections with specific requirements for content length, references, formats, and quality assurance.

## Outcome

- ✅ Impact: Updated constitution file with project-specific principles and requirements
- 🧪 Tests: none
- 📁 Files: Modified .specify/memory/constitution.md
- 🔁 Next prompts: Begin writing book content based on established principles
- 🧠 Reflection: Constitution now properly reflects the specific requirements for the Physical AI & Humanoid Robotics book project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - Constitution properly updated with all specified principles
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin developing book content following constitution guidelines