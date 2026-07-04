from datetime import datetime, date

import jdatetime


ENGLISH_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")


def gregorian_to_jalali_str(value):

    if not value:
        return "-"

    try:

        if isinstance(value, datetime):
            jalali = jdatetime.datetime.fromgregorian(datetime=value)
            return jalali.strftime("%Y/%m/%d - %H:%M")

        if isinstance(value, date):
            jalali = jdatetime.date.fromgregorian(date=value)
            return jalali.strftime("%Y/%m/%d")

        return str(value)

    except Exception:
        return "-"


def jalali_str_to_gregorian_datetime(jalali_date_str, time_str):

    jalali_date_str = jalali_date_str.strip().translate(ENGLISH_DIGITS).replace("-", "/")

    year, month, day = (int(part) for part in jalali_date_str.split("/"))
    hour, minute = (int(part) for part in time_str.strip().split(":"))

    gregorian_date = jdatetime.date(year, month, day).togregorian()

    return datetime(
        gregorian_date.year,
        gregorian_date.month,
        gregorian_date.day,
        hour,
        minute
    )