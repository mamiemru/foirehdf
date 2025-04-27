import os
import re


def extract_strings_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all occurrences of _('string') or _("string")
    matches = re.findall(r'_\(\s*[\'"](.+?)[\'"]\s*\)', content)
    return matches


def save_to_po_format(strings, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for s in strings:
            f.write('msgid "{}"\n'.format(s.replace('"', '\\"')))
            f.write('msgstr ""\n\n')


def iterate_folder(folder_path, output_file):
    all_strings = set()
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                strings = extract_strings_from_file(file_path)
                all_strings.update(strings)

    save_to_po_format(sorted(all_strings), output_file)


if __name__ == "__main__":
    folder_to_scan = "./pages"  # <-- Change this
    output_po_file = "extracted_translations.po"  # or "messages.po" if you prefer

    iterate_folder(folder_to_scan, output_po_file)
    print(f"Extraction completed. Strings saved in {output_po_file}")
