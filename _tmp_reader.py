# Read files with utf-8 encoding
import sys
sys.stdout.reconfigure(encoding='utf-8')

files = [
    'D:/test_ai/app.py',
    'D:/test_ai/models.py',
    'D:/test_ai/config.py',
    'D:/test_ai/decorators.py',
    'D:/test_ai/utils.py',
    'D:/test_ai/admin.py',
    'D:/test_ai/routes/__init__.py',
    'D:/test_ai/routes/auth.py',
    'D:/test_ai/routes/shop.py',
    'D:/test_ai/routes/staff.py',
    'D:/test_ai/routes/admin.py',
]

for f in files:
    print(f"=== {f} ===")
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        print(content)
    except Exception as e:
        print(f"Error: {e}")
    print()
