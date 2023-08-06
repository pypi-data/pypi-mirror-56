from ticts.utils import timestamp_converter
from .types import TimeStampVar, ValueVar


class Event(object):
    def __init__(self, t: TimeStampVar, value: ValueVar, name: str = "") -> None:
        self.value = value
        self.t = timestamp_converter(t)
        self.name = name

    def __repr__(self) -> str:
        return "Event({}, t={}, name={})".format(
            *map(repr, [self.value, self.t, self.name])
        )
