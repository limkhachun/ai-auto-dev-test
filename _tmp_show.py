import os
os.chdir('D:/test_ai')
import sys
sys.stdout.reconfigure(encoding='utf-8')

files = [
    'app.py', 'models.py', 'config.py', 'decorators.py', 'utils.py', 'admin.py',
]

for f in files:
    print(f"=== {f} ===")
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            print(fh.read())
    except Exception as e:
        try:
            with open(f, 'r', encoding='latin-1') as fh:
                print(fh.read())
        except Exception as e2:
            print(f"Error: {e2}")
    print("---")
