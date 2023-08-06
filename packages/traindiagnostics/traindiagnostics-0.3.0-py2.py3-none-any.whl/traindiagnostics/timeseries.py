import ticts
from datetime import timedelta
import operator
from functools import singledispatch
from .event import Event
from .report import Report
from .errors import DuplicateDateTimeError
from .types import ValueVar, TimeStampVar
from typing import Dict


class TimeSeries(ticts.TimeSeries):

    def __init__(self,
                 data: Dict[TimeStampVar, ValueVar] = None,
                 default: ValueVar = 0,
                 name: str = "value",
                 permissive: bool = True,
                 tz: str = "UTC") -> None:

        super().__init__(data=data,
                         default=default,
                         name=name,
                         permissive=permissive,
                         tz=tz)

    def __matmul__(self, other):
        return self.search(other)

    def __rshift__(self, other):
        return self.search(other)

    def __lshift__(self, other):
        return other.search(self)

    @classmethod
    def from_events(cls, events):
        if events:
            new_data = {}
            name = events[0].name
            keys = set()
            for e in events:
                if e.t in keys:
                    raise DuplicateDateTimeError
                new_data[e.t] = e.value
            return cls(new_data, name=name)
        return cls()

    @classmethod
    def from_reports(cls, reports):
        if reports:
            name = reports[0].name
            data = {}
            keys = set()
            for report in reports:
                if keys & {report.t0, report.te}:
                    raise DuplicateDateTimeError
                data[report.t0] = 1
                data[report.te] = 0
                keys.add(report.t0)
                keys.add(report.te)
            return cls(data, name=name)
        return cls()

    def to_reports(self):
        raise NotImplementedError

    def to_events(self):
        for key, value in self.items():
            yield Event(key, value, self.name)

    def timedeltas(self):
        for t1, t2 in zip(self.index[:-1], self.index[1:]):
            yield t2 - t1
        yield timedelta()

    def timerule(self, duration, value_threshold=1, method=operator.ge):
        new_data = {}
        for delta, (index, value) in zip(self.timedeltas(), self.items()):
            if value >= value_threshold:
                if method(delta, duration):
                    new_data[index] = value
            else:
                new_data[index] = value

        return type(self)(new_data, self.name)

    def repeatrule(self, duration, repeat_threshold, value_threshold=1):
        data_new = {}
        latest_end = None
        for key, value in self.items():
            if value >= value_threshold:
                mask = slice(key, key + duration)
                occurrences = sum(self[mask].values())
                if occurrences >= repeat_threshold * value_threshold:
                    if latest_end is not None:
                        if key < latest_end:
                            data_new.pop(latest_end)
                    data_new[key] = value
                    data_new[key + duration] = 0
                    latest_end = key + duration
            else:
                if data_new.keys():
                    if max(data_new.keys()) <= key:
                        data_new[key] = value
                else:
                    data_new[key] = value

        return type(self)(data_new, self.name)

    @singledispatch
    def search(self, by, value_threshold=1):
        new_data = {}
        for start, end in self.iter_active(value_threshold):
            mask = slice(start, end)
            occurrences = self.default
            occurrences += by[start]
            occurrences += sum(by[mask].values())
            if occurrences >= value_threshold:
                new_data[start] = self[start]
                new_data[end] = self[end]
        return type(self)(new_data, name=self.name)

    @search.register
    def _(self, by: Report):
        raise NotImplementedError

    def iter_active(self, value_threshold=1):
        iterator = iter(self.items())
        try:
            while True:
                value_activate = self.default
                while value_activate < value_threshold:
                    key_activate, value_activate = next(iterator)
                key_deactivate, value_deactivate = next(iterator)
                yield key_activate, key_deactivate
        except StopIteration:
            pass
