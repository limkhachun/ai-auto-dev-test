# Direct read test
with open('D:/test_ai/app.py', 'rb') as f:
    raw = f.read()
print("Raw bytes (first 100):", raw[:100])
print("Encoding detection...")
# Try to decode
for enc in ['utf-8', 'utf-16', 'latin-1', 'cp1252']:
    try:
        decoded = raw.decode(enc)
        print(f"  {enc}: OK, first 50 chars: {decoded[:50]!r}")
        break
    except:
        print(f"  {enc}: Failed")
