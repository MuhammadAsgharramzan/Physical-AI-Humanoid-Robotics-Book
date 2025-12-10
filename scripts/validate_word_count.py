#!/usr/bin/env python3
"""
Script to validate that book content remains within 25,000–40,000 words range
"""

import os
import sys
from pathlib import Path
import re

def count_words_in_file(file_path):
    """Count words in a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove markdown formatting and count words
        # Remove headers, code blocks, links, etc. to count only prose
        text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)  # Code blocks
        text = re.sub(r'~~~.*?~~~', '', text, flags=re.DOTALL)    # Alternative code blocks
        text = re.sub(r'`[^`]*`', '', text)  # Inline code
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)  # Headers
        text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # Links
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Images
        text = re.sub(r'>\s*', '', text)  # Blockquotes
        text = re.sub(r'\*\*.*?\*\*', '', text)  # Bold
        text = re.sub(r'\*.*?\*', '', text)  # Italic
        text = re.sub(r'_{2}.*?_{2}', '', text)  # Bold with underscores
        text = re.sub(r'_.+?_', '', text)  # Italic with underscores

        # Count remaining words
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return 0

def count_words_in_directory(directory):
    """Count words in all markdown files in a directory"""
    total_words = 0
    file_counts = {}

    for md_file in Path(directory).rglob("*.md"):
        word_count = count_words_in_file(md_file)
        total_words += word_count
        file_counts[str(md_file)] = word_count
        print(f"  {md_file}: {word_count} words")

    return total_words, file_counts

def validate_word_count():
    """Validate that book content is within the required range"""
    content_dir = Path("content")

    if not content_dir.exists():
        print(f"Content directory {content_dir} does not exist!")
        return False

    print("Counting words in book content...")
    total_words, file_counts = count_words_in_directory(content_dir)

    print(f"\nTotal word count: {total_words:,}")
    print(f"Required range: 25,000–40,000 words")

    min_words = 25000
    max_words = 40000

    if min_words <= total_words <= max_words:
        print(f"SUCCESS: Word count is within the required range ({min_words:,}-{max_words:,})")
        return True
    else:
        if total_words < min_words:
            print(f"FAILURE: Word count is below minimum (need {min_words - total_words:,} more words)")
        else:
            print(f"FAILURE: Word count exceeds maximum by {total_words - max_words:,} words")

        # Provide suggestions for adjustment
        if total_words < min_words:
            print("\nSuggested actions:")
            print("- Add more detailed explanations in existing sections")
            print("- Include additional examples and case studies")
            print("- Expand on technical implementation details")
            print("- Add more content to underdeveloped modules")
        else:
            print("\nSuggested actions:")
            print("- Condense lengthy explanations while preserving key concepts")
            print("- Remove redundant content or examples")
            print("- Streamline technical details that are too verbose")
            print("- Consider moving some content to appendices")

        return False

def main():
    """Main function to validate word count"""
    print("Validating Physical AI & Humanoid Robotics Book word count...")

    success = validate_word_count()

    if success:
        print("\nSUCCESS: Word count validation passed!")
        return 0
    else:
        print("\nFAILURE: Word count validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())