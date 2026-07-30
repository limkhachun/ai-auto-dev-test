# This file will just re-export models content to see error messages
import sys
sys.path.insert(0, 'D:/test_ai')

# Read and print models.py content
with open('D:/test_ai/models.py', 'r') as f:
    content = f.read()
    # Write to a new file that we can hopefully read
    with open('D:/test_ai/_models_content.txt', 'w') as out:
        out.write(content)

with open('D:/test_ai/app.py', 'r') as f:
    content = f.read()
    with open('D:/test_ai/_app_content.txt', 'w') as out:
        out.write(content)

with open('D:/test_ai/config.py', 'r') as f:
    content = f.read()
    with open('D:/test_ai/_config_content.txt', 'w') as out:
        out.write(content)

print("Done")
