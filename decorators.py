from flask import session, url_for, redirect
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('isAdmin') is None or session.get('isAdmin') is False:
            return redirect(url_for('wally.index'))
        return f(*args, **kwargs)
    return decorated_function

