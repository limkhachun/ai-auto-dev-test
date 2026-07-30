import subprocess, sys
r = subprocess.run([sys.executable, 'D:/test_ai/_tmp_show.py'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout)
if r.stderr:
    print('STDERR:', r.stderr[:2000])
