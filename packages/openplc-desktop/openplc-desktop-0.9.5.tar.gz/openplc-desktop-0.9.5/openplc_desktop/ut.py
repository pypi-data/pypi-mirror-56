

def to_int(v, default=None):

    try:
        return int(v)

    except Exception as e:
        return default

def read_file(file_path):
    with open(file_path, "r") as xfile:
        return xfile.read()
    return None

def write_file(file_path, content):
    with open(file_path, "w") as xfile:
        xfile.write(content)
    return None

