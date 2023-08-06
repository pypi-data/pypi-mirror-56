import re

pattern = re.compile(r'^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)')


def read(file_path: str):
    with open(file_path, 'rb') as f:
        lines = f.readlines()
        if len(lines) >= 2:
            first, second, *_ = lines
        length = len(f.readlines())
        first = f.readline()
