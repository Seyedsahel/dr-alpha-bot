from datetime import datetime, timedelta, date, time


FRIDAY = 4


def generate_weekly_slots(start_time_str, end_time_str, interval_minutes=20, working_days=7):

    start_hour, start_minute = (int(part) for part in start_time_str.strip().split(":"))
    end_hour, end_minute = (int(part) for part in end_time_str.strip().split(":"))

    start_time = time(start_hour, start_minute)
    end_time = time(end_hour, end_minute)

    if start_time >= end_time:
        raise ValueError("ساعت شروع باید قبل از ساعت پایان باشد")

    generated = []

    current_date = date.today()
    collected_days = 0

    while collected_days < working_days:

        if current_date.weekday() != FRIDAY:

            day_cursor = datetime.combine(current_date, start_time)
            day_end = datetime.combine(current_date, end_time)

            while day_cursor < day_end:
                generated.append(day_cursor)
                day_cursor += timedelta(minutes=interval_minutes)

            collected_days += 1

        current_date += timedelta(days=1)

    return generated