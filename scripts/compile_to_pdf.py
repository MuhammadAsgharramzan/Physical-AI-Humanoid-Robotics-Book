#!/usr/bin/env python3
"""
Script to compile the Physical AI & Humanoid Robotics book to PDF format
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def collect_book_content():
    """Collect all book content from the content directory"""
    content_dir = Path("content")
    book_parts = []

    # Add the main index
    main_index = content_dir / "index.md"
    if main_index.exists():
        with open(main_index, 'r', encoding='utf-8') as f:
            book_parts.append({
                'title': 'Physical AI & Humanoid Robotics',
                'content': f.read(),
                'path': 'index.md'
            })

    # Add all modules
    for module_dir in sorted(content_dir.glob("module*")):
        if module_dir.is_dir():
            module_index = module_dir / "index.md"
            if module_index.exists():
                with open(module_index, 'r', encoding='utf-8') as f:
                    module_content = f.read()
                    # Extract title from the first heading
                    lines = module_content.split('\n')
                    title = 'Untitled'
                    for line in lines:
                        if line.startswith('# '):
                            title = line[2:].strip()
                            break

                    book_parts.append({
                        'title': title,
                        'content': module_content,
                        'path': f"{module_dir.name}/index.md"
                    })

    return book_parts

def convert_markdown_to_html(book_parts):
    """Convert collected markdown content to HTML"""
    html_parts = []

    # Start HTML document with proper structure
    html_parts.append("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Physical AI & Humanoid Robotics</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        h1 {
            font-size: 2em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            font-size: 1.5em;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
        }
        p {
            margin-bottom: 16px;
        }
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 10px;
            overflow-x: auto;
            margin-bottom: 16px;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: monospace;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin: 0 0 16px 0;
            padding: 0 16px;
            color: #7f8c8d;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .page-break {
            page-break-before: always;
        }
    </style>
</head>
<body>
    """)

    # Add each part to the HTML
    for i, part in enumerate(book_parts):
        if i > 0:
            html_parts.append('<div class="page-break"></div>')

        # Convert markdown to HTML
        md_html = markdown.markdown(part['content'], extensions=['tables', 'fenced_code'])

        # Add section header
        html_parts.append(f'<h1>{part["title"]}</h1>')
        html_parts.append(f'<div class="content">{md_html}</div>')

    # Close HTML document
    html_parts.append("""
</body>
</html>
    """)

    return ''.join(html_parts)

def compile_to_pdf(output_path="Physical_AI_Humanoid_Robotics_Book.pdf"):
    """Compile the book content to PDF format"""
    print("Collecting book content...")
    book_parts = collect_book_content()

    print("Converting to HTML...")
    html_content = convert_markdown_to_html(book_parts)

    print(f"Generating PDF: {output_path}...")

    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(html_content)
        temp_html_path = temp_file.name

    try:
        # Convert HTML to PDF using weasyprint
        html = HTML(temp_html_path)
        font_config = FontConfiguration()

        # Define custom CSS for PDF
        css = CSS(string="""
            @page {
                margin: 2cm;
                @bottom-right {
                    content: counter(page);
                }
                @bottom-left {
                    content: "Physical AI & Humanoid Robotics Book";
                }
            }
            body {
                font-family: Arial, sans-serif;
                font-size: 12pt;
                line-height: 1.4;
                color: #000;
            }
            h1 {
                font-size: 1.5em;
                color: #000;
                break-after: avoid;
            }
            h2 {
                font-size: 1.3em;
                color: #333;
                break-after: avoid;
            }
            h3 {
                font-size: 1.1em;
                color: #555;
                break-after: avoid;
            }
            code, pre {
                font-family: "Courier New", monospace;
                font-size: 0.9em;
            }
            pre {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                padding: 8px;
                overflow-x: auto;
            }
        """, font_config=font_config)

        html.write_pdf(output_path, stylesheets=[css], font_config=font_config)
        print(f"PDF successfully generated: {output_path}")

    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return False
    finally:
        # Clean up temporary file
        os.unlink(temp_html_path)

    return True

def main():
    """Main function to compile the book to PDF"""
    print("Compiling Physical AI & Humanoid Robotics Book to PDF...")

    # Check if required packages are available
    try:
        import markdown
        import weasyprint
    except ImportError as e:
        print(f"Required package not installed: {e}")
        print("Please install required packages with: pip install markdown weasyprint")
        return 1

    # Generate PDF
    success = compile_to_pdf()

    if success:
        print("Book compilation completed successfully!")
        return 0
    else:
        print("Book compilation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())