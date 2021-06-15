from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from pytickets.tickets.domain import CreateTicket
from .forms import CreateTicketForm
from pytickets.tickets.handlers.queries import get_all
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
    tickets = get_all(session_factory)
    return render_template('dashboard.html', tickets=tickets)


@bp.route('/new', methods=['GET','POST'])
def new():
    form = CreateTicketForm()
    if form.validate_on_submit():
        create_ticket = CreateTicket(form.summary.data, form.description.data)
        ticket_created = create_ticket_handler(create_ticket)
        flash('Ticket created!')
        return redirect(url_for('tickets.dashboard'))
    return render_template('new_ticket.html', form=form)
