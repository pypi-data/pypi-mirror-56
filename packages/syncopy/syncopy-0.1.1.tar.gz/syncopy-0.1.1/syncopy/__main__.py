from docopt import docopt

from . import settings
from .sync import sync
from .util import printe

USAGE = """\
{name} - syncronize two driectories

Usage:
    {name} [options] SOURCEDIR TARGETDIR
""".format(name=__package__)

if __name__ == '__main__':
    args = docopt(str(USAGE), version=settings.__version__)
    try:
        sync(args['SOURCEDIR'], args['TARGETDIR'])
    except KeyboardInterrupt:
        pass
    except (OSError, Exception) as e:
        printe(e)
        raise
