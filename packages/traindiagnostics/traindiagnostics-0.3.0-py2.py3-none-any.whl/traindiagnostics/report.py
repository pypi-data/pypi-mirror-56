from .errors import ChronologicalError
from ticts.utils import timestamp_converter
from .types import TimeStampVar


class Report(object):
    def __init__(self, t0: TimeStampVar, te: TimeStampVar, name: str = "") -> None:
        self.t0 = timestamp_converter(t0)
        self.te = timestamp_converter(te)
        self.name = name

        if not self._is_chronological():
            raise ChronologicalError(
                "te ({}) can't be before t0! ({})".format(self.te, self.t0)
            )

    def _is_chronological(self) -> bool:
        return self.te < self.t0

    def __repr__(self) -> str:
        return "Report(t0={}, te={}, name={})".format(
            *map(repr, [self.t0, self.te, self.name])
        )

    @property
    def duration(self) -> float:
        return self.te - self.t0

    def overlap(self, other) -> bool:
        return (self.t0 <= other.te) | (other.t0 <= self.te)
