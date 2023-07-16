from flask import (
    Blueprint, render_template, request, g, flash, redirect, url_for
)
from flaskr.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

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


@bp.route('/updateUsername', methods=('GET', 'POST'))
def updateUsername():
    if request.method == 'POST':
        db = get_db()
        newUsername = request.form['username']
        password = request.form['password']
        
        error = None
        
        user = db.execute(
            f'SELECT * FROM user WHERE id = {g.user["id"]}'
        ).fetchone()
        if not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        print(password, user['password'])
        
        if error is None:
            db.execute(
                'UPDATE user SET username = ? '
                'WHERE id = ?',
                (newUsername, g.user['id'])
            )
            db.commit()
            return redirect(url_for('profile.index'))
       
        flash(error)

    return render_template('profile/updateUsername.html')


@bp.route('/updatePassword', methods=('GET', 'POST'))
def updatePassword():
    if request.method == 'POST':
        oldPassword = request.form["oldPassword"]
        newPassword = request.form["newPassword"]
        confirmNewPassword = request.form["confirmNewPassword"]

        db = get_db()
        user = db.execute(
            f'SELECT * FROM user WHERE id = {g.user["id"]}'
        ).fetchone()
        
        error = None
        if not check_password_hash(user["password"], oldPassword):
            error = "Incorrect Password."
        if newPassword != confirmNewPassword:
            error = "Passwords do not match."
        
        if error is None:
            db.execute(
                'UPDATE user SET password = ? '
                'WHERE id = ?',
                (generate_password_hash(newPassword), g.user["id"])
            )
            db.commit()
            return redirect(url_for('profile.index')) 


    return render_template('profile/updatePassword.html')


@bp.route('/updateMode', methods=('GET', 'POST'))
def updateMode():
    if request.method == 'POST':
        db = get_db()
        response = db.execute(
            'UPDATE user SET mode = ? '
            'WHERE id = ?',
            (request.form['mode'], g.user['id'])
        )
        db.commit()
        return redirect(url_for('profile.index'))
    return render_template('profile/updateMode.html')