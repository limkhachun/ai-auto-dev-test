import sys
sys.path.insert(0, 'D:/test_ai')
with open('D:/test_ai/models.py', 'r') as f:
    content = f.read()
# Intentionally create a syntax error to see the content in the error message
exec(compile('print("""' + content + '""")', '<test>', 'exec'))
