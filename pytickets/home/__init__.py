from flask import Blueprint, redirect, url_for
from flask.templating import render_template
from pytickets import oidc

bp = Blueprint('home', __name__, template_folder='templates')


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route("/login")
@oidc.require_login
def login():
    return redirect(url_for("tickets.dashboard"))


@bp.route('/logout')
def logout():
    oidc.logout()
    return redirect(url_for('home.index'))
