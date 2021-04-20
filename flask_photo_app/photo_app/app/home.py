import functools
from flask_login import login_required, current_user

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify,render_template_string
)
#from config import PREFIX

#bp = Blueprint('home', __name__,  url_prefix=f"{PREFIX}")
bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.nickname)

