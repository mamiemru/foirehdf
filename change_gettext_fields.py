import os
import re
from datetime import datetime

OUTPUT_FILE = 'messages.po'

def is_snake_case(text):
    return bool(re.match(r'^[A-Z0-9_]+$', text)) and '_' in text

def to_snake_case(text):
    return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_').upper()

def process_file(filepath, collected_strings):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def replacer(match):
        quote, original = match.group(1), match.group(2)
        if is_snake_case(original):
            collected_strings.add(original)
            return match.group(0)
        if ' ' in original:
            base = os.path.splitext(os.path.basename(filepath))[0]
            new_text = f"{to_snake_case(base)}_{to_snake_case(original)}"
            collected_strings.add(new_text)
            return f"_({quote}{new_text}{quote})"
        collected_strings.add(original)
        return match.group(0)

    pattern = re.compile(r'_\(\s*(["\'])(.*?)\1\s*\)')
    new_content = pattern.sub(replacer, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def walk_and_process_files(source_dir):
    collected_strings = set()
    for root, _, files in os.walk(source_dir):
        for filename in files:
            if filename.endswith('.py'):
                process_file(os.path.join(root, filename), collected_strings)
    return sorted(collected_strings)

def write_po_file(messages, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for msg in messages:
            f.write('msgid "{}"\n'.format(msg.replace('"', '\"')))
            f.write('msgstr ""\n\n')

def main():
    messages = walk_and_process_files('.')  # Adjust directory as needed
    write_po_file(messages, OUTPUT_FILE)
    print(f"Updated source files and wrote {len(messages)} messages to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
