"""
Decorators for route protection: login_required and role_required.
"""
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """Require a valid user session to access the route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """
    Require the user to have one of the specified roles.
    Usage: @role_required('staff', 'superadmin')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('role') not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('shop.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
