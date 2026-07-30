import sys
with open('D:/test_ai/app.py', 'rb') as f:
    data = f.read()
with open('D:/test_ai/app_decoded.txt', 'wb') as f:
    f.write(data)
print('Written', len(data), 'bytes')
