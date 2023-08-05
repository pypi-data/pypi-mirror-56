import sys
from io import StringIO
from pathlib import Path


def prints(*args, **kwargs):
    b = StringIO()
    kwargs['file'] = b
    kwargs['end'] = ''
    print(*args, **kwargs)
    return b.getvalue()


def printe(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)


def error(*args, **kwargs):
    printe('ERROR:', *args, **kwargs)


def short_path(path, n=60):
    p = Path(path)
    parts = p.parts
    while parts and len(str(p)) > n:
        parts = parts[1:]
        p = Path('/'.join(parts))
    spath = str(path)
    sp = str(p)
    if len(sp) < len(spath):
        sp = '.../' + sp
    return sp



