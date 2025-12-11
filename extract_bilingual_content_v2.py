import re
import os

def extract_module4_content():
    with open('frontend/docs/module4_bilingual.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content into lines
    lines = content.split('\n')

    # Find frontmatter
    frontmatter_match = re.search(r'^(---.*?---)', content, re.DOTALL)
    if not frontmatter_match:
        print("No frontmatter found in module4_bilingual.md")
        return

    frontmatter = frontmatter_match.group(1)

    # Modify frontmatter for English version
    eng_frontmatter = re.sub(r'title: \".*?/.*?\"', 'title: \"Module 4: AI Reasoning & Applications in Robotics\"', frontmatter)
    eng_frontmatter = re.sub(r'description: \".*?/.*?\"', 'description: \"Understanding how artificial intelligence enhances robotic capabilities and enables intelligent behavior\"', eng_frontmatter)
    eng_frontmatter = re.sub(r'sidebar_label: \".*?/.*?\"', 'sidebar_label: \"AI Reasoning & Applications in Robotics\"', eng_frontmatter)

    # Modify frontmatter for Urdu version
    urdu_frontmatter = re.sub(r'title: \".*?/.*?\"', 'title: \"ماڈیول 4: روبوٹکس میں مصنوعی ذہانت کا تجزیہ اور اطلاق\"', frontmatter)
    urdu_frontmatter = re.sub(r'description: \".*?/.*?\"', 'description: \"مصنوعی ذہانت کو سمجھنا جو روبوٹک صلاحیتوں کو بڑھاتی ہے اور ذہین رویہ کو فعال کرتی ہے\"', urdu_frontmatter)
    urdu_frontmatter = re.sub(r'sidebar_label: \".*?/.*?\"', 'sidebar_label: \"روبوٹکس میں مصنوعی ذہانت کا تجزیہ اور اطلاق\"', urdu_frontmatter)

    # Extract content sections
    eng_lines = []
    urdu_lines = []
    current_section = None  # None, 'eng', or 'urdu'

    for line in lines:
        # Skip frontmatter
        if line.strip() == '---' and len(eng_lines) == 0 and len(urdu_lines) == 0:
            continue
        if 'title:' in line and 'description:' in line and len(eng_lines) == 0:
            continue

        # Check if line is in English (basic heuristic: contains more English letters than Arabic/Persian)
        eng_chars = sum(1 for c in line if c.isalpha() and ord(c) < 256)
        urdu_chars = sum(1 for c in line if ord(c) >= 0x600 and ord(c) <= 0x6FF or ord(c) >= 0x200C and ord(c) <= 0x200D)

        # Process headers that have both languages
        if line.strip().startswith('#'):
            # Split by common separator '/'
            parts = line.split('/')
            if len(parts) >= 2:
                eng_part = parts[0].strip()
                urdu_part = parts[1].strip() if len(parts) > 1 else ""

                eng_lines.append(eng_part)
                urdu_lines.append(urdu_part)
            else:
                eng_lines.append(line)
                urdu_lines.append(line)
        elif '## English Version' in line:
            current_section = 'eng'
        elif '## Urdu Version' in line:
            current_section = 'urdu'
        elif current_section == 'eng':
            eng_lines.append(line)
        elif current_section == 'urdu':
            urdu_lines.append(line)
        else:
            # For mixed format like Module 4, use character detection
            if eng_chars > urdu_chars * 2:  # More English than Urdu characters
                eng_lines.append(line)
            elif urdu_chars > 0:  # Contains Urdu characters
                urdu_lines.append(line)
            else:
                # If it's a common line, add to both
                eng_lines.append(line)
                urdu_lines.append(line)

    # Join lines and clean up
    eng_content = '\n'.join(eng_lines).replace('# ماڈیول', '#').replace('# Module', '#').replace('## تعارف', '').replace('## Introduction', '## Introduction').replace('## AI Reasoning & Applications in Robotics', '## AI Reasoning & Applications in Robotics').replace('## روبوٹکس میں مصنوعی ذہانت کا تجزیہ اور اطلاق', '')
    urdu_content = '\n'.join(urdu_lines).replace('# Module', '#').replace('# ماڈیول', '#').replace('## Introduction', '').replace('## تعارف', '## تعارف').replace('## AI Reasoning & Applications in Robotics', '').replace('## روبوٹکس میں مصنوعی ذہانت کا تجزیہ اور اطلاق', '## روبوٹکس میں مصنوعی ذہانت کا تجزیہ اور اطلاق')

    # Clean up empty sections
    eng_content = re.sub(r'\n\s*\n\s*\n', '\n\n', eng_content)  # Remove extra blank lines
    urdu_content = re.sub(r'\n\s*\n\s*\n', '\n\n', urdu_content)  # Remove extra blank lines

    # Create final files
    eng_file_content = eng_frontmatter + '\n\n' + eng_content
    urdu_file_content = urdu_frontmatter + '\n\n' + urdu_content

    with open('frontend/docs/module4_en.md', 'w', encoding='utf-8') as f:
        f.write(eng_file_content)

    with open('frontend/docs/module4_ur.md', 'w', encoding='utf-8') as f:
        f.write(urdu_file_content)

def extract_standard_module(module_num):
    with open(f'frontend/docs/module{module_num}_bilingual.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the frontmatter
    frontmatter_match = re.search(r'^(---.*?---)', content, re.DOTALL)
    if not frontmatter_match:
        print(f"No frontmatter found in module{module_num}_bilingual.md")
        return

    frontmatter = frontmatter_match.group(1)

    # Extract English content
    english_match = re.search(r'## English Version / انگریزی ورژن(.*?)(?=## Urdu Version|$)', content, re.DOTALL)
    if english_match:
        eng_content = english_match.group(1).strip()

        # Modify frontmatter for English version
        eng_title = f'Module {module_num}: Foundations of Physical AI' if module_num == 1 else f'Module {module_num}: Sensing and Perception in Physical AI' if module_num == 2 else f'Module {module_num}: Control and Locomotion Systems' if module_num == 3 else f'Module {module_num}: AI Reasoning & Applications in Robotics'
        eng_desc = 'Understanding the fundamental principles of Physical AI and embodied intelligence' if module_num == 1 else 'Understanding sensing and perception systems in Physical AI and humanoid robotics' if module_num == 2 else 'Understanding control and locomotion systems in humanoid robotics' if module_num == 3 else 'Understanding how artificial intelligence enhances robotic capabilities and enables intelligent behavior'

        eng_frontmatter = re.sub(r'title: \".*?/.*?\"', f'title: \"{eng_title}\"', frontmatter)
        eng_frontmatter = re.sub(r'description: \".*?/.*?\"', f'description: \"{eng_desc}\"', eng_frontmatter)
        eng_frontmatter = re.sub(r'sidebar_label: \".*?/.*?\"', f'sidebar_label: \"{eng_title}\"', eng_frontmatter)

        eng_file_content = eng_frontmatter + f'\n\n# {eng_title}\n\n' + eng_content

        with open(f'frontend/docs/module{module_num}_en.md', 'w', encoding='utf-8') as f:
            f.write(eng_file_content)

    # Extract Urdu content
    urdu_match = re.search(r'## Urdu Version / اردو ورژن(.*?)(?=## English Version|$)', content, re.DOTALL)
    if urdu_match:
        urdu_content = urdu_match.group(1).strip()

        # Modify frontmatter for Urdu version
        urdu_title = f'ماڈیول {module_num}: جسمانی مصنوعی ذہانت کی بنیادیں' if module_num == 1 else f'ماڈیول {module_num}: جسمانی مصنوعی ذہانت میں حس اور ادراک' if module_num == 2 else f'ماڈیول {module_num}: کنٹرول اور حرکت کے سسٹم' if module_num == 3 else f'ماڈیول {module_num}: روبوٹکس میں مصنوعی ذہانت کا تجزیہ اور اطلاق'
        urdu_desc = 'جسمانی مصنوعی ذہانت اور جسمانی ذہانت کے بنیادی اصولوں کو سمجھنا' if module_num == 1 else 'جسمانی مصنوعی ذہانت اور انسان نما روبوٹکس میں حس اور ادراک کے سسٹم کو سمجھنا' if module_num == 2 else 'ہیومنوائڈ روبوٹکس میں کنٹرول اور حرکت کے سسٹم کو سمجھنا' if module_num == 3 else 'مصنوعی ذہانت کو سمجھنا جو روبوٹک صلاحیتوں کو بڑھاتی ہے اور ذہین رویہ کو فعال کرتی ہے'

        urdu_frontmatter = re.sub(r'title: \".*?/.*?\"', f'title: \"{urdu_title}\"', frontmatter)
        urdu_frontmatter = re.sub(r'description: \".*?/.*?\"', f'description: \"{urdu_desc}\"', urdu_frontmatter)
        urdu_frontmatter = re.sub(r'sidebar_label: \".*?/.*?\"', f'sidebar_label: \"{urdu_title}\"', urdu_frontmatter)

        urdu_file_content = urdu_frontmatter + f'\n\n# {urdu_title}\n\n' + urdu_content

        with open(f'frontend/docs/module{module_num}_ur.md', 'w', encoding='utf-8') as f:
            f.write(urdu_file_content)

# Process module 4 specifically
extract_module4_content()

# Process other modules if needed
for i in range(1, 5):
    if not os.path.exists(f'frontend/docs/module{i}_en.md') or not os.path.exists(f'frontend/docs/module{i}_ur.md'):
        extract_standard_module(i)
        print(f"Processed module {i}")
    else:
        print(f"Module {i} files already exist")