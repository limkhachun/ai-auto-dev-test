import subprocess
r = subprocess.run(['python', 'D:/test_ai/_tmp_reader.py'], capture_output=True, text=True, encoding='utf-8', errors='replace')
with open('D:/test_ai/_tmp_output.txt', 'w', encoding='utf-8') as f:
    f.write(r.stdout)
    if r.stderr:
        f.write('\n---STDERR---\n')
        f.write(r.stderr)
print("Done")
