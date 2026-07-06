def safe_int(value, default=None):

    if value is None or value == "":
        return default

    try:
        return int(value)

    except (ValueError, TypeError):
        return default