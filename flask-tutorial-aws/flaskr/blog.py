from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.s3 import allowed_file, upload_file_to_s3, create_presigned_post
from flask import current_app, g

import os

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, image_file, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/download/<resource>')
def download_image(resource):
    """ resource: name of the file to download"""
    print("resources for download " + resource)
    url = create_presigned_post(resource,current_app.config["S3_BUCKET"])
    print("url is " + url)
    return redirect(url, code=302)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
  #      image_file = request.form['image_file']

        error = None

        if 'image_file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        image_file = request.files['image_file']

        if image_file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if image_file and allowed_file(image_file.filename):
            image_file.filename = str(g.user['id']) + '.' + secure_filename(image_file.filename)
            upload_file_to_s3(image_file, current_app.config["S3_BUCKET"])
            
   #     print(image_file.filename)  
   #     full_filename =  os.path.join(current_app.config['IMAGE_FOLDER'], filename)
   #     image_file.save(filename)
        

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, image_file, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, image_file.filename, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, image_file, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))