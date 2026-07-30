import subprocess, sys, os
os.chdir('D:/test_ai')
r = subprocess.run([sys.executable, '_tmp_show.py'], capture_output=True, text=True, encoding='utf-8', errors='replace')
with open('test_output.txt', 'w', encoding='utf-8') as f:
    f.write(r.stdout)
    if r.stderr:
        f.write('\nSTDERR:\n' + r.stderr[:3000])
print("Written to test_output.txt")
print("First 200 chars:", r.stdout[:200])
