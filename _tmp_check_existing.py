"""
This file tries to read existing project files and output their content.
Run with: python _tmp_check_existing.py
"""
import os

base = 'D:/test_ai'
files_to_read = ['models.py', 'app.py', 'config.py', 'init.sql']
for fname in files_to_read:
    fpath = os.path.join(base, fname)
    if os.path.exists(fpath):
        print(f"=== {fname} ===")
        with open(fpath, 'r', encoding='utf-8') as f:
            print(f.read())
        print()
    else:
        print(f"=== {fname} NOT FOUND ===")

# Check templates
templates_dir = os.path.join(base, 'templates')
if os.path.exists(templates_dir):
    print("=== TEMPLATES ===")
    for fname in os.listdir(templates_dir):
        print(f"  templates/{fname}")
        with open(os.path.join(templates_dir, fname), 'r', encoding='utf-8') as f:
            content = f.read()
            # Print first 20 lines
            lines = content.split('\n')
            for i, line in enumerate(lines[:30], 1):
                print(f"  {i}: {line}")
            print()
