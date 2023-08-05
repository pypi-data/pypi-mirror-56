import datetime
from robotpt_common_utils import math_tools

NUM_DAYS_IN_A_WEEK = 7


def subtract_days(start_date, end_date):

    if (
            not (type(start_date) == type(end_date) == datetime.date)
            and not (type(start_date) == type(end_date) == datetime.datetime)
    ):
        raise TypeError("Inputs must be datetimes")

    return (end_date - start_date).days


def subtract_weeks(start_date, end_date, is_full_weeks_only=True):

    weeks_difference = subtract_days(start_date, end_date) / NUM_DAYS_IN_A_WEEK
    if is_full_weeks_only:
        return int(weeks_difference)
    else:
        return weeks_difference


def get_date_range(
        start_date,
        end_date,
        increment_days=1,
        output_format=None
):
    if not math_tools.is_int(increment_days):
        raise ValueError("'increment_days' must be an int")

    if increment_days < 0:
        raise ValueError("'increment_days' must be nonnegative")

    if start_date > end_date:
        raise IOError("'start_date' must be less than 'end_date'")

    date = start_date
    date_range = []
    while date < end_date:
        date_range.append(date)
        date += datetime.timedelta(days=increment_days)
    if output_format is None:
        return date_range
    elif type(output_format) is str:
        return [
            datetime.datetime.strftime(date, output_format)
            for date in date_range
        ]


def subtract_times(t1, t2):

    if type(t1) is not datetime.time or type(t2) is not datetime.time:
        raise ValueError

    dt1 = _time_from_0(t1)
    dt2 = _time_from_0(t2)
    days = dt2.days - dt1.days
    seconds = dt2.seconds - dt1.seconds
    if abs(seconds) == 24*60*60:
        seconds = 0
    elif abs(seconds) == 12*60*60:
        seconds = 12*60*60
        days = -1
    elif seconds > 12*60*60 and days == 0:
        seconds = -(seconds - 12*60*60)
        days = 0
    return datetime.timedelta(days=days, seconds=seconds)


def _time_from_0(t):
    t_dt = datetime.datetime.now().replace(hour=t.hour, minute=t.minute, second=t.second, microsecond=t.microsecond)
    midnight = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dt = t_dt - midnight
    if dt.seconds == 24*60*60:
        dt = datetime.timedelta()
    if dt.seconds >= 12*60*60:
        dt = datetime.timedelta(seconds=dt.seconds - 24*60*60)
    return dt
