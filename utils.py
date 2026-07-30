"""
Utility functions for the application.
"""
import re
from datetime import datetime


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def format_currency(amount):
    """Format a numeric value as currency string."""
    return f'${float(amount):,.2f}'


def format_datetime(dt):
    """Format a datetime object to a human-readable string."""
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return '-'


def is_valid_email(email):
    """Basic email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))
