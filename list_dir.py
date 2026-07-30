import os
for root, dirs, files in os.walk("D:/test_ai"):
    for f in files:
        print(os.path.join(root, f))
    for d in dirs:
        print(os.path.join(root, d) + "/")
