from flask import (
    Blueprint, flash, g, redirect, render_template, render_template_string, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime


#from flaskr.s3 import allowed_file, upload_file_to_s3, create_presigned_post
from flask import current_app, g
from . import dynamodb, util, s3, dynamodb
import os

#from config import PREFIX

bp = Blueprint('blog', __name__,url_prefix="/blog")
#bp = Blueprint('blog', __name__,url_prefix=f"{PREFIX}/blog")

@bp.route('/test')
def test():
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <p>test path</p>
        {% endblock %}""")

@bp.route('/blog')
def blog():
    return render_template('blog.html')


@bp.route('/index')
@login_required
def index():
    photos = dynamodb.list_user_photos(current_user.nickname)
    for photo in photos:
        print(photo)
        if "image_file" in photo:
            print("presign")
            photo["signed_url"] = s3.create_presigned_post(photo["image_file"],current_app.config["AWS_S3_BUCKET"])
        else:
            photo["signed_url"] = "no photo"
        print(photo)
    return render_template('index.html', posts=photos)

@bp.route('/create_textonly', methods=('GET', 'POST'))
@login_required
def create_textonly():
    print('create_textonly!')
    print(request.get_json())

    if request.method == 'POST':

        print(request.form)
    
        title = request.form['title']
        body = request.form['body'] 
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S")

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
            
        else:
            result = dynamodb.add_photo_textonly(title, body, current_user.nickname,timestampStr)
            print(result)
            return redirect(url_for('blog.index'))

    return render_template('create_textonly.html')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print('create!')
    print(request.get_json())

    if request.method == 'POST':

        print(request.form)
        print(request.files)

        title = request.form['title']
        body = request.form['body'] 

        error = None

        if 'image_file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        image_file = request.files['image_file']


        if image_file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S")

        if image_file and util.allowed_file(image_file.filename):
            image_file.filename = str(current_user.nickname) + '.' + timestampStr + '.' + secure_filename(image_file.filename)
            result = s3.upload_file_to_s3(image_file, current_app.config["AWS_S3_BUCKET"])
            print(result)

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            result = dynamodb.add_photo(title, body, image_file.filename,current_user.nickname,timestampStr)
            print(result)
            return redirect(url_for('blog.index'))

    return render_template('create.html')

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