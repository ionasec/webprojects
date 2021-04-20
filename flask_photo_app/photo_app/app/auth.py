import sys
import functools
from jose import jwt
import flask_login
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from flask_login import login_user
from . import util

#from config import PREFIX
import requests
from requests.auth import HTTPBasicAuth

from flask import (
    Blueprint, flash, g, redirect, render_template, render_template_string, request, session, url_for, jsonify, current_app, g
)

    ### load and cache cognito JSON Web Key (JWK)
# https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html


#bp = Blueprint('auth', __name__, url_prefix=f"{PREFIX}/auth")
bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route("/login")
def login():
    
    print(request)
    """Login route"""
    # http://docs.aws.amazon.com/cognito/latest/developerguide/login-endpoint.html
    session['csrf_state'] = util.random_hex_bytes(8)
    cognito_login = ("https://%s/"
                     "login?response_type=code&client_id=%s"
                     "&redirect_uri=%s/auth/callback"
                     "&state=%s"
                     "&scope=email+openid+profile"
                      %
                     (current_app.config['AWS_COGNITO_DOMAIN'],
                     current_app.config['AWS_COGNITO_CLIENT_ID'],
                     current_app.config['BASE_URL'],
                     session['csrf_state']))
    print(cognito_login)
    
    return redirect(cognito_login)


@bp.route("/logout")
def logout():
    """Logout route"""
    # http://docs.aws.amazon.com/cognito/latest/developerguide/logout-endpoint.html
    flask_login.logout_user()
    cognito_logout = ("https://%s/"
                      "logout?client_id=%s"
                      "&logout_uri=%s" %
                      (current_app.config['AWS_COGNITO_DOMAIN'],
                     current_app.config['AWS_COGNITO_CLIENT_ID'],
                     current_app.config['BASE_URL']))
    print(cognito_logout)
    g.pop('user', None)
    return redirect(cognito_logout)

@bp.route("/callback")
def callback():
    """Exchange the 'code' for Cognito tokens"""
    #http://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
    csrf_state = request.args.get('state')
    code = request.args.get('code')
    request_parameters = {'grant_type': 'authorization_code',
                          'client_id': current_app.config['AWS_COGNITO_CLIENT_ID'],
                          'code': code,
                          "redirect_uri" : current_app.config['BASE_URL'] + "/auth/callback"}

    response = requests.post("https://%s/oauth2/token" % current_app.config['AWS_COGNITO_DOMAIN'],
                             data=request_parameters,
                             auth=HTTPBasicAuth(current_app.config['AWS_COGNITO_CLIENT_ID'],
                             current_app.config['AWS_COGNITO_CLIENT_SECRET']))
  
    print(response.status_code)
    print(requests.codes.ok)
    print(csrf_state)
    print(session['csrf_state'])
    # the response:
    # http://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html
    if response.status_code == requests.codes.ok and csrf_state == session['csrf_state']:
        print(response.status_code)
        verify(response.json()["access_token"])
        id_token = verify(response.json()["id_token"], response.json()["access_token"])

        user = User()
        user.id = id_token["cognito:username"]
        session['nickname'] = user.id
        session['expires'] = id_token["exp"]
        session['refresh_token'] = response.json()["refresh_token"]
        flask_login.login_user(user, remember=True)
        return redirect(url_for('blog.index'))

    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <p>Something went wrong</p>
        {% endblock %}""")

def verify(token, access_token=None):
    JWKS_URL = ("https://cognito-idp.%s.amazonaws.com/%s/.well-known/jwks.json" % (current_app.config['AWS_REGION'], current_app.config['AWS_COGNITO_POOL_ID']))
    JWKS = requests.get(JWKS_URL).json()["keys"]

    """Verify a cognito JWT"""
    # get the key id from the header, locate it in the cognito keys
    # and verify the key
    header = jwt.get_unverified_header(token)
    key = [k for k in JWKS if k["kid"] == header['kid']][0]
    id_token = jwt.decode(token, key, audience=current_app.config['AWS_COGNITO_CLIENT_ID'], access_token=access_token)
    return id_token



class User(flask_login.UserMixin):
    """Standard flask_login UserMixin"""
    pass

