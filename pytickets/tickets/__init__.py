from flask import Blueprint
from flask.templating import render_template
from pytickets import oidc

bp = Blueprint('tickets', __name__, template_folder='templates', url_prefix='/tickets')

@bp.route('/dashboard')
@oidc.require_login
def dashboard():
    return render_template('dashboard.html')

