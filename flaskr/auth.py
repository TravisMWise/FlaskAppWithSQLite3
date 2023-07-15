import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """
    Require Authentication in Other Views
    Creating, editing, and deleting blog posts will require a user to be logged in. 
    A decorator can be used to check this for each view it's applied to.

    This decorator returns a new view function that wraps the original view it's applied to. 
    The new function checks if a user is loaded and redirects to the login page otherwise. 
    If a user is loaded the original view is called and continues normally. 
    Use this decorator when writing the blog views.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login')) # Redirect if not logged in.

        # Continue if logged in
        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        db = get_db()
        error = None
        
        MIN_LENGTH = 3
        def passwordIsComplex(password):
            if len(password) < MIN_LENGTH:
                return (False, f'Password must be more than {MIN_LENGTH} characters.')
            return (True, "")

        def usernameIsComplex(username):
            if len(username) < MIN_LENGTH:
                return (False, f'Username must be more than {MIN_LENGTH} characters.')
            if not username[0].isalpha():
                return (False, f'Username must start with an alphanumeric character.')
            return (True, "")

        if not username:
            error = 'Username required.'
        elif not password:
            error = 'Password required.'
        elif password != confirm_password:
            error = f'Passwords do not match. {password} | {confirm_password}'
        usernameComplexity = usernameIsComplex(username)
        if not usernameComplexity[0]:
            error = usernameComplexity[1]
        passwordComplexity = passwordIsComplex(password)
        if not passwordComplexity[0]:
            error = passwordComplexity[1]
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?,?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
        
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,) 
        ).fetchone() # fetchone() == Fetch one row
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
    

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
