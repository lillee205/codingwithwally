from flask import session, url_for, redirect
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('isAdmin') is None or session.get('isAdmin') is False:
            return redirect(url_for('wally.index'))
        return f(*args, **kwargs)
    return decorated_function

def contents_required(contents):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if contents == "" or contents == None:
                return redirect(url_for('wally.error'))
            return f(*args, **kwargs)
        return decorated_function 
    return decorator
