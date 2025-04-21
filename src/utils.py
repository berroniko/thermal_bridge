from datetime import datetime


def is_nan(value) -> bool:
    if isinstance(value, float):
        if value != value:
            return True
        else:
            return False
    if not value:
        return True
    else:
        return False


def parse_date(date_str: str) -> datetime:
    for fmt in ('%d.%m.%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format not supported: {date_str}")
