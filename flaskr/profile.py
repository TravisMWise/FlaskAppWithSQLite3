from flask import (
    Blueprint, render_template, request, g
)
from flaskr.db import get_db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' From post p JOIN user u ON p.author_id = u.id'
        f' WHERE author_id = {g.user["id"]}'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('profile/index.html', user_posts=posts)

@bp.route('/update')
def update():
    return render_template('profile/update.html')

@bp.route('/updateUsername')
def updateUsername():
    return render_template('profile/updateUsername.html')
@bp.route('/updatePassword')
def updatePassword():
    return render_template('profile/updatePassword.html')