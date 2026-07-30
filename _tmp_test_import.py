"""Test file to understand project structure"""
import sys
sys.path.insert(0, 'D:/test_ai')

# Try to import and inspect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Read models.py content
with open('D:/test_ai/models.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Print first 30 lines for analysis
for i, line in enumerate(lines[:50], 1):
    print(f"{i}: {line}", end='')
