import subprocess, sys
# Run the show script
r = subprocess.run([sys.executable, 'D:/test_ai/_tmp_show.py'], capture_output=True, text=True, encoding='utf-8', errors='replace')
out_path = 'D:/test_ai/test.txt'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(r.stdout)
    if r.stderr:
        f.write('\nSTDERR:\n' + r.stderr)
print('Written to', out_path)
