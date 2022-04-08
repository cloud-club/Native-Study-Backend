from datetime import datetime


def time2str(time: datetime, ms=True) -> str:
    str_time = time.strftime("%Y-%m-%d %H:%M:%S.%f")
    if ms:
        return str_time[:-3]
    return str_time


def elapsed(t1: datetime, t2: datetime, ms=True):
    elapsed_time = abs(t1 - t2).total_seconds()
    if ms:
        return round(elapsed_time, 3)
    return elapsed_time
