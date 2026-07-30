"""Write models.py content to a readable file"""
import ast, sys

with open('D:/test_ai/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

with open('D:/test_ai/_models_dump.txt', 'w', encoding='utf-8') as out:
    out.write(content)

with open('D:/test_ai/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

with open('D:/test_ai/_app_dump.txt', 'w', encoding='utf-8') as out:
    out.write(content)

with open('D:/test_ai/config.py', 'r', encoding='utf-8') as f:
    content = f.read()

with open('D:/test_ai/_config_dump.txt', 'w', encoding='utf-8') as out:
    out.write(content)

with open('D:/test_ai/templates/login.html', 'r', encoding='utf-8') as f:
    content = f.read()

with open('D:/test_ai/_login_dump.txt', 'w', encoding='utf-8') as out:
    out.write(content)

with open('D:/test_ai/templates/register.html', 'r', encoding='utf-8') as f:
    content = f.read()

with open('D:/test_ai/_register_dump.txt', 'w', encoding='utf-8') as out:
    out.write(content)

print("Done dumping files")
