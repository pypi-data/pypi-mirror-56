

def to_int(v, default=None):

    try:
        return int(v)

    except Exception as e:
        return default
