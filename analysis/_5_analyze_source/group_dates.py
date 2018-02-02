from dateutil.parser import parse
from datetime import timedelta


def group_dates(start_date, end_date, list_of_dates):
    start = parse(start_date)
    end = parse(end_date)
    length = (end - start).days + 1
    result = [0] * length
    result_idx = 0
    current = start
    date_idx = 0
    while date_idx < len(list_of_dates):
        if parse(list_of_dates[date_idx]) == current:
            result[result_idx] += 1
            date_idx += 1
        else:
            current += timedelta(days=1)
            result_idx += 1
    return result
