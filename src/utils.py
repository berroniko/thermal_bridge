def is_nan(value)->bool:
    if isinstance(value, float):
        if value != value:
            return True
        else:
            return False
    if not value:
        return True
    else:
        return False
