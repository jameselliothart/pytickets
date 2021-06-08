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
    _id: uuid.uuid4 = uuid.uuid4()


@dataclass(frozen=True)
class Details():
    summary: str
    description: str = None


@dataclass(frozen=True)
class Resolution():
    resolution: str = None
    completed_on: datetime = None


@dataclass(frozen=True)
class Item(_Metadata, Resolution, Details):
    pass


@dataclass(frozen=True)
class NotStarted(Item):
    pass


@dataclass(frozen=True)
class InProgress(Item):
    pass


@dataclass(frozen=True)
class Completed(Item):
    pass


def new(details: Details):
    return NotStarted(**asdict(details))


def not_started(item: Item):
    return replace(NotStarted(**asdict(item)), updated_on = now_utc(), completed_on = None)


def in_progress(item: Item):
    return replace(InProgress(**asdict(item)), updated_on = now_utc(), completed_on = None)


def complete(item: Item):
    return replace(Completed(**asdict(item)), completed_on = now_utc())


if __name__ == '__main__':
    d = Details('do something')
    ticket = new(d)
    prog = complete(ticket)
    print(prog)
