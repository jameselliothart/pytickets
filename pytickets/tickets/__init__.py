from pytickets.tickets.handlers.sql import complete_ticket_handler, create_ticket_handler
from pytickets.config import get_datebase_uri
from pytickets.adapters.orm import new_session_factory
from flask import Blueprint
from flask.templating import render_template
from pytickets import oidc
from functools import partial

bp = Blueprint('tickets', __name__, template_folder='templates',
               url_prefix='/tickets')

session_factory = new_session_factory(get_datebase_uri())

create_ticket_handler =  partial(create_ticket_handler,session_factory)
complete_ticket_handler = partial(complete_ticket_handler,session_factory)


@bp.route('/dashboard')
@oidc.require_login
def dashboard():
    return render_template('dashboard.html')
