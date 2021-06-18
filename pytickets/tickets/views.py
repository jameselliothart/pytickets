import uuid
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from pytickets.tickets.domain import CompleteTicket, CreateTicket, now_utc
from .forms import CompleteTicketForm, CreateTicketForm
from pytickets.adapters.orm import new_session_factory
from pytickets.tickets.handlers.queries import get_open
from pytickets.tickets.handlers.sql import complete_ticket_handler, create_ticket_handler
from pytickets.config import get_datebase_uri
from flask import Blueprint
from flask.templating import render_template
from pytickets import oidc
from functools import partial

bp = Blueprint('tickets', __name__, template_folder='templates',
               url_prefix='/tickets')

session_factory = new_session_factory(get_datebase_uri())

create_ticket_handler = partial(create_ticket_handler, session_factory)
complete_ticket_handler = partial(complete_ticket_handler, session_factory)


@bp.route('/')
@oidc.require_login
def dashboard():
    tickets = get_open(session_factory)
    complete_form = CompleteTicketForm()
    return render_template('dashboard.html', tickets=tickets, complete_form=complete_form)


@bp.route('/new', methods=['GET', 'POST'])
@oidc.require_login
def new():
    form = CreateTicketForm()
    if form.validate_on_submit():
        create_ticket = CreateTicket(form.summary.data, form.description.data)
        ticket_created = create_ticket_handler(create_ticket)
        flash('Ticket created!')
        return redirect(url_for('tickets.dashboard'))
    return render_template('new_ticket.html', form=form)


@bp.post('/complete/<ticket_id>')
@oidc.require_login
def complete(ticket_id):
    form = CompleteTicketForm()
    if form.validate_on_submit():
        complete_ticket = CompleteTicket(
            uuid.UUID(ticket_id), form.resolution.data, now_utc())
        print(f'{complete_ticket=}')
        ticket_completed = complete_ticket_handler(complete_ticket)
        flash('Ticket completed!')
        return redirect(url_for('tickets.dashboard'))
