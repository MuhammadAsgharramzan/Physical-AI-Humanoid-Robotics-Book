#!/usr/bin/env python3
"""
Script to compile the Physical AI & Humanoid Robotics book to ePub format
"""

import os
import sys
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
import markdown

def create_epub_structure():
    """Create the basic structure for an ePub file"""
    # ePub is essentially a ZIP file with specific structure
    epub_structure = {
        'mimetype': 'application/epub+zip',
        'META-INF/container.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>''',
        'OEBPS/content.opf': '''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="BookId">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>Physical AI & Humanoid Robotics</dc:title>
    <dc:creator opf:role="aut">AI Book Project</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>AI Book Project</dc:publisher>
    <dc:date>{date}</dc:date>
    <dc:identifier id="BookId">physical-ai-humanoid-robotics-book</dc:identifier>
    <dc:description>A comprehensive guide to Physical AI and Humanoid Robotics for students, hobbyists, and early-stage robotics learners</dc:description>
  </metadata>
  <manifest>
    <item id="toc" properties="nav" href="toc.xhtml" media-type="application/xhtml+xml"/>
    {manifest_items}
  </manifest>
  <spine toc="ncx">
    {spine_items}
  </spine>
</package>''',
        'OEBPS/toc.ncx': '''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="physical-ai-humanoid-robotics-book"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>Physical AI & Humanoid Robotics</text>
  </docTitle>
  <navMap>
    {nav_points}
  </navMap>
</ncx>''',
        'OEBPS/toc.xhtml': '''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>Table of Contents</title>
  </head>
  <body>
    <nav epub:type="toc">
      <ol>
        {nav_items}
      </ol>
    </nav>
  </body>
</html>'''
    }
    return epub_structure

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
                'path': 'index.md',
                'filename': 'index.xhtml'
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
                        'path': f"{module_dir.name}/index.md",
                        'filename': f"{module_dir.name}.xhtml"
                    })

    return book_parts

def convert_markdown_to_xhtml(markdown_content, title):
    """Convert markdown content to XHTML format for ePub"""
    # Convert markdown to HTML
    html = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])

    # Wrap in XHTML structure
    xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <h1>{title}</h1>
    {html}
</body>
</html>'''

    return xhtml

def compile_to_epub(output_path="Physical_AI_Humanoid_Robotics_Book.epub"):
    """Compile the book content to ePub format"""
    print("Collecting book content...")
    book_parts = collect_book_content()

    print("Creating ePub structure...")

    # Create temporary directory for ePub files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create basic structure
        epub_structure = create_epub_structure()

        # Write basic files
        for filename, content in epub_structure.items():
            file_path = temp_path / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if filename == 'OEBPS/content.opf':
                # This will be generated later with dynamic content
                continue
            elif filename == 'OEBPS/toc.ncx':
                # This will be generated later with dynamic content
                continue
            elif filename == 'OEBPS/toc.xhtml':
                # This will be generated later with dynamic content
                continue
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

        # Create XHTML files for each part
        xhtml_files = []
        for part in book_parts:
            xhtml_content = convert_markdown_to_xhtml(part['content'], part['title'])
            xhtml_file = temp_path / f"OEBPS/{part['filename']}"
            xhtml_file.parent.mkdir(parents=True, exist_ok=True)
            with open(xhtml_file, 'w', encoding='utf-8') as f:
                f.write(xhtml_content)
            xhtml_files.append(part['filename'])

        # Create CSS file
        css_content = '''body {
    font-family: serif;
    line-height: 1.4;
    margin: 2em;
    color: #000;
}

h1, h2, h3, h4, h5, h6 {
    color: #333;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

h1 {
    font-size: 1.5em;
    text-align: center;
}

h2 {
    font-size: 1.3em;
}

p {
    margin-bottom: 0.8em;
    text-align: justify;
}

pre {
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    padding: 1em;
    overflow-x: auto;
    font-size: 0.9em;
    font-family: monospace;
}

code {
    font-family: monospace;
    background-color: #f8f8f8;
    padding: 0.2em;
}

blockquote {
    margin: 1em 0;
    padding-left: 1em;
    border-left: 4px solid #ddd;
    color: #666;
}

img {
    max-width: 100%;
    height: auto;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}

th {
    background-color: #f2f2f2;
}'''
        css_file = temp_path / "OEBPS/style.css"
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)

        # Generate dynamic content for OPF file
        manifest_items = []
        spine_items = []
        nav_points = []
        nav_items = []

        for i, part in enumerate(book_parts):
            # Manifest items
            media_type = "application/xhtml+xml"
            manifest_items.append(f'    <item id="{part["filename"][:-6]}" href="{part["filename"]}" media-type="{media_type}"/>')

            # Spine items
            spine_items.append(f'    <itemref idref="{part["filename"][:-6]}"/>')

            # NCX navigation points
            nav_points.append(f'''    <navPoint id="navpoint-{i}" playOrder="{i}">
      <navLabel>
        <text>{part["title"]}</text>
      </navLabel>
      <content src="{part["filename"]}"/>
    </navPoint>''')

            # XHTML TOC items
            nav_items.append(f'      <li><a href="{part["filename"]}">{part["title"]}</a></li>')

        # Complete the OPF file
        opf_content = epub_structure['OEBPS/content.opf'].format(
            date=datetime.now().strftime("%Y-%m-%d"),
            manifest_items='\n    '.join(manifest_items),
            spine_items='\n    '.join(spine_items)
        )

        opf_file = temp_path / "OEBPS/content.opf"
        with open(opf_file, 'w', encoding='utf-8') as f:
            f.write(opf_content)

        # Complete the NCX file
        ncx_content = epub_structure['OEBPS/toc.ncx'].format(
            nav_points='\n    '.join(nav_points)
        )

        ncx_file = temp_path / "OEBPS/toc.ncx"
        with open(ncx_file, 'w', encoding='utf-8') as f:
            f.write(ncx_content)

        # Complete the TOC XHTML file
        toc_content = epub_structure['OEBPS/toc.xhtml'].format(
            nav_items='\n    '.join(nav_items)
        )

        toc_file = temp_path / "OEBPS/toc.xhtml"
        with open(toc_file, 'w', encoding='utf-8') as f:
            f.write(toc_content)

        # Create the ePub file (which is a ZIP file with specific structure)
        print(f"Generating ePub: {output_path}...")

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as epub_file:
            # Add mimetype file first (without compression)
            epub_file.writestr("mimetype", epub_structure['mimetype'], compress_type=zipfile.ZIP_STORED)

            # Add all other files
            for root, dirs, files in os.walk(temp_path):
                for file in files:
                    file_path = Path(root) / file
                    # Get relative path from temp directory
                    relative_path = file_path.relative_to(temp_path)
                    epub_file.write(file_path, relative_path)

        print(f"ePub successfully generated: {output_path}")

    return True

def main():
    """Main function to compile the book to ePub"""
    print("Compiling Physical AI & Humanoid Robotics Book to ePub...")

    # Check if required packages are available
    try:
        import markdown
    except ImportError as e:
        print(f"Required package not installed: {e}")
        print("Please install required packages with: pip install markdown")
        return 1

    # Generate ePub
    success = compile_to_epub()

    if success:
        print("Book ePub compilation completed successfully!")
        return 0
    else:
        print("Book ePub compilation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())