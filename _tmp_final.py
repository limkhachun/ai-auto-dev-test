import subprocess, sys
result = subprocess.run([sys.executable, '_tmp_show.py'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd='D:/test_ai')
# Just print directly
sys.stdout.reconfigure(encoding='utf-8')
sys.stdout.write(result.stdout[:5000])
if result.stderr:
    sys.stdout.write('\n---STDERR---\n')
    sys.stdout.write(result.stderr[:2000])
