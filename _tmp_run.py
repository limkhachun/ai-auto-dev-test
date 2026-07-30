import subprocess
result = subprocess.run(['python', 'D:/test_ai/_tmp_reader.py'], capture_output=True, text=True, encoding='utf-8')
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
