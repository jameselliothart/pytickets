from pytickets.tickets.handlers.sql import new_complete_ticket_handler, new_create_ticket_handler
from pytickets.config import get_datebase_uri
from pytickets.adapters.orm import new_session_factory
from flask import Blueprint
from flask.templating import render_template
from pytickets import oidc

bp = Blueprint('tickets', __name__, template_folder='templates',
               url_prefix='/tickets')

session_factory = new_session_factory(get_datebase_uri())

create_ticket_handler = new_create_ticket_handler(session_factory)
complete_ticket_handler = new_complete_ticket_handler(session_factory)


@bp.route('/dashboard')
@oidc.require_login
def dashboard():
    return render_template('dashboard.html')
