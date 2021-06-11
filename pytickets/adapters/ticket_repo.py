from dataclasses import asdict
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import pytickets.tickets.domain as ticket


def new_session_factory(url, **kwagrs):
    return sessionmaker(create_engine(url, **kwagrs))


def get(session: Session, id: uuid4):
    return session.query(ticket.Ticket).filter_by(id=id).first()


def add(session: Session, ticket: ticket.Ticket):
    session.add(ticket)


def update(session: Session, id: uuid4, details: ticket.Details):
    session.query(ticket.Ticket).filter_by(
        id=id).update(asdict(details))


def delete(session: Session, id: uuid4):
    session.query(ticket.Ticket).filter_by(id=id).delete()


def commit(session: Session):
    session.commit()


def to_in_progress(session: Session, ticket: ticket.InProgress):
    delete(session, ticket.id)
    add(session, ticket)


def to_complete(session: Session, ticket: ticket.Completed):
    delete(session, ticket.id)
    add(session, ticket)
