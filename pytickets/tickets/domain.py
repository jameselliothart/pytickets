import uuid
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timedelta, timezone


def as_cst(t: datetime):
    return t.astimezone(timezone(timedelta(hours=-5)))


def now_utc():
    return datetime.now().astimezone(timezone.utc)


@dataclass(frozen=True)
class _Metadata():
    updated_on: datetime = None
    created_on: datetime = now_utc()
    id: uuid.uuid4 = uuid.uuid4()


@dataclass(frozen=True)
class Details():
    summary: str
    description: str = None


@dataclass(frozen=True)
class Resolution():
    resolution: str = None
    completed_on: datetime = None


@dataclass(frozen=True)
class Ticket(_Metadata, Resolution, Details):
    pass


@dataclass(frozen=True)
class InProgress(Ticket):
    pass


@dataclass(frozen=True)
class Completed(Ticket):
    pass


@dataclass(frozen=True)
class TicketCompleted():
    item: Completed


def new(details: Details):
    return Ticket(**asdict(details))


def not_started(item: Ticket):
    return replace(Ticket(**asdict(item)), updated_on = now_utc(), completed_on = None)


def in_progress(item: Ticket):
    return replace(InProgress(**asdict(item)), updated_on = now_utc(), completed_on = None)


def complete(item: Ticket):
    return replace(Completed(**asdict(item)), completed_on = now_utc())


if __name__ == '__main__':
    d = Details('do something')
    ticket = new(d)
    prog = complete(ticket)
    print(prog)
