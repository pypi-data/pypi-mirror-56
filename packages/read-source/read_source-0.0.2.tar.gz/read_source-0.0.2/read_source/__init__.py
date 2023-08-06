import re
import itertools

_pattern = re.compile(rb'^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)')


def get_encoding(file_path: str):
    with open(file_path, 'rb') as f:
        # get first line in file
        source_lines = itertools.islice(f.readlines(), 2)
    for line in source_lines:
        # line = line.decode('ascii')
        result = _pattern.search(line)
        if result:
            return result.groups()[0].decode('ascii')

    # fall back to default encoding
    return 'utf-8'


def read(path: str, mode='r'):
    return open(
        path,
        mode=mode,
        encoding=get_encoding(path),
    )
