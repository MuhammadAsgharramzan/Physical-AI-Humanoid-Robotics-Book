import re
import os

def extract_language_content(bilingual_file, module_num):
    with open(bilingual_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the frontmatter
    frontmatter_match = re.search(r'^(---.*?---)', content, re.DOTALL)
    if not frontmatter_match:
        print(f"No frontmatter found in {bilingual_file}")
        return

    frontmatter = frontmatter_match.group(1)

    # Extract English content
    english_match = re.search(r'## English Version / انگریزی ورژن(.*?)(?=## Urdu Version|$)', content, re.DOTALL)
    if english_match:
        eng_content = english_match.group(1).strip()

        # Modify frontmatter for English version
        eng_frontmatter = re.sub(r'title: \".*?/.*?\"', f'title: \"Module {module_num}: Foundations of Physical AI\"', frontmatter)
        eng_frontmatter = re.sub(r'description: \".*?/.*?\"', 'description: \"Understanding the fundamental principles of Physical AI and embodied intelligence\"', eng_frontmatter)
        eng_frontmatter = re.sub(r'sidebar_label: \".*?/.*?\"', f'sidebar_label: \"Module {module_num}: Foundations of Physical AI\"', eng_frontmatter)

        eng_file_content = eng_frontmatter + f'\n\n# Module {module_num}: Foundations of Physical AI\n\n' + eng_content

        with open(f'module{module_num}_en.md', 'w', encoding='utf-8') as f:
            f.write(eng_file_content)

    # Extract Urdu content
    urdu_match = re.search(r'## Urdu Version / اردو ورژن(.*?)(?=## English Version|$)', content, re.DOTALL)
    if urdu_match:
        urdu_content = urdu_match.group(1).strip()

        # Modify frontmatter for Urdu version
        urdu_frontmatter = re.sub(r'title: \".*?/.*?\"', f'title: \"ماڈیول {module_num}: جسمانی مصنوعی ذہانت کی بنیادیں\"', frontmatter)
        urdu_frontmatter = re.sub(r'description: \".*?/.*?\"', 'description: \"جسمانی مصنوعی ذہانت اور جسمانی ذہانت کے بنیادی اصولوں کو سمجھنا\"', urdu_frontmatter)
        urdu_frontmatter = re.sub(r'sidebar_label: \".*?/.*?\"', f'sidebar_label: \"ماڈیول {module_num}: جسمانی مصنوعی ذہانت کی بنیادیں\"', urdu_frontmatter)

        urdu_file_content = urdu_frontmatter + f'\n\n# ماڈیول {module_num}: جسمانی مصنوعی ذہانت کی بنیادیں\n\n' + urdu_content

        with open(f'module{module_num}_ur.md', 'w', encoding='utf-8') as f:
            f.write(urdu_file_content)

# Process all modules
for i in range(1, 5):
    bilingual_file = f'frontend/docs/module{i}_bilingual.md'
    if os.path.exists(bilingual_file):
        extract_language_content(bilingual_file, i)
        print(f"Processed module {i}")
    else:
        print(f"File {bilingual_file} not found")