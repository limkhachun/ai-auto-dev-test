import sys
sys.path.insert(0, 'D:/test_ai')

# Read models.py
with open('D:/test_ai/models.py', 'r', encoding='utf-8') as f:
    print("=== models.py ===")
    print(f.read())

print("\n\n")

# Read app.py
with open('D:/test_ai/app.py', 'r', encoding='utf-8') as f:
    print("=== app.py ===")
    print(f.read())

print("\n\n")

# Read config.py
with open('D:/test_ai/config.py', 'r', encoding='utf-8') as f:
    print("=== config.py ===")
    print(f.read())

print("\n\n")

# Read login.html
with open('D:/test_ai/templates/login.html', 'r', encoding='utf-8') as f:
    print("=== login.html ===")
    print(f.read())

print("\n\n")

# Read register.html
with open('D:/test_ai/templates/register.html', 'r', encoding='utf-8') as f:
    print("=== register.html ===")
    print(f.read())

print("\n\n")

# Read init.sql
try:
    with open('D:/test_ai/init.sql', 'r', encoding='utf-8') as f:
        print("=== init.sql ===")
        print(f.read())
except:
    print("init.sql not readable")

print("\n\n")

# Read style.css
try:
    with open('D:/test_ai/static/css/style.css', 'r', encoding='utf-8') as f:
        print("=== style.css ===")
        print(f.read())
except:
    print("style.css not readable")
