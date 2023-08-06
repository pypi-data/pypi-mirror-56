import pandas as pd
import pytz


def utc(dt):
    return pytz.utc.localize(dt)


def load_dataframe(dataframe, train="train", code="code", start="start", end="end", mask=None):
    dataframe.sort(by=[train, code, start, end])

    trains = dataframe[train].unique()
    codes = dataframe[code].unique()

    fleet = dict()

    for _train in trains:
        if _train not in fleet.keys():
            fleet[_train] = dict()
        for _code in codes:
            if _code not in fleet[_train].keys():
                fleet[_train][_code] = None


if __name__ == "__main__":
    import datetime as dt

    df = pd.DataFrame(
        [
            dict(
                train="001",
                code="a",
                start=utc(dt.datetime(2019, 1, 1, 8)),
                end=utc(dt.datetime(2019, 1, 1, 8, 30)),
            ),
            dict(
                train="002",
                code="a",
                start=utc(dt.datetime(2019, 1, 1, 8)),
                end=utc(dt.datetime(2019, 1, 1, 8, 30)),
            ),
            dict(
                train="003",
                code="a",
                start=utc(dt.datetime(2019, 1, 1, 8)),
                end=utc(dt.datetime(2019, 1, 1, 8, 30)),
            ),
            dict(
                train="001",
                code="b",
                start=utc(dt.datetime(2019, 1, 1, 8, 30)),
                end=utc(dt.datetime(2019, 1, 1, 8, 45)),
            ),
            dict(
                train="001",
                code="a",
                start=utc(dt.datetime(2019, 1, 1, 9, 30)),
                end=utc(dt.datetime(2019, 1, 1, 9, 45)),
            ),
            dict(
                train="001",
                code="c",
                start=utc(dt.datetime(2019, 1, 1, 8)),
                end=utc(dt.datetime(2019, 1, 1, 9, 45)),
            ),
            dict(
                train="002",
                code="b",
                start=utc(dt.datetime(2019, 1, 1, 8, 30)),
                end=utc(dt.datetime(2019, 1, 1, 8, 45)),
            ),
            dict(
                train="001",
                code="a",
                start=utc(dt.datetime(2019, 1, 1, 12)),
                end=utc(dt.datetime(2019, 1, 1, 14, 30)),
            ),
        ]
    )
