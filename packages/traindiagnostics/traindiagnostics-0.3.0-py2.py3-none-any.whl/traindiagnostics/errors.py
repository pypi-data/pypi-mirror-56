class DiagnosticsError(Exception):
    pass


class DataLossError(DiagnosticsError):
    pass


class ChronologicalError(DiagnosticsError, ValueError):
    pass


class DuplicateDateTimeError(DiagnosticsError, ValueError):
    pass
