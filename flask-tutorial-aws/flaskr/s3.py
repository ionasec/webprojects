
import os
from flask import Flask, flash, request, redirect, url_for
from flask import current_app, g
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_image_folder():
    if 'image_folder' not in g:
        g.image_folder = current_app.config['IMAGE_FOLDER'],

    return g.image_folder