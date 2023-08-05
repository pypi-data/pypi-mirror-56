import errno
import shutil
import hashlib
from pathlib import Path
from datetime import timedelta
from timeit import default_timer as timer
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

from .util import printe, prints, short_path

BLOCK_SIZE = 64 * 1024

executor = PoolExecutor(max_workers=2)

EXCLUDES = [
    '.tox',
    # '__pycache__',
    # '*.py[co]',
    # '*.photoslibrary',
    # '**/resources/recovery/**/*',
    # '**/MojavePhotosLibrary.photoslibrary/*',
    # '**/MojavePhotosLibrary.photoslibrary/**/*',
]


@dataclass
class Progress:
    start = timer()
    bytes = 0

    @property
    def elapsed(self):
        return timer() - self.start

    def update(self, bytes):
        self.bytes += bytes

    def print(self, *args, **kwargs):
        s = prints(*args, **kwargs)
        s = (s[-68:] + ' ' * 80)[:72]
        bytes_s = self.bytes / self.elapsed
        printe(
            timedelta(seconds=round(self.elapsed)),
            '%10.1f MiB/s' % (bytes_s / 2**20),
            s,
            end='\r',
            **kwargs
        )


def sync(source, target):
    source = Path(source).resolve()
    target = Path(target).resolve()

    if not source.is_dir():
        raise ValueError(f'Source "{source}" must be an existing directory')

    if target.exists() and not target.is_dir():
        raise ValueError(f'Target "{target}" must be an directory if it exists')

    printe(f'Will sync "{source}" with "{target}"')

    p = Progress()
    for s, t in files_to_sync(p, source, target):
        copy_file(p, s, t)

    printe()


def files_to_sync(p, source, target, current=None):
    if current is None:
        current = source
    for sourcefile in sorted(current.glob('*')):
        if any(sourcefile.match(e) for e in EXCLUDES):
            continue
        elif sourcefile.is_dir():
            yield from files_to_sync(p, source, target, current=sourcefile)
        else:
            path = sourcefile.relative_to(source)
            try:
                p.update(sourcefile.stat().st_size)

                targetfile = target / path
                p.print(short_path(targetfile))

                should_copy = (
                    not targetfile.exists() or
                    (
                        targetfile.stat().st_mtime < sourcefile.stat().st_mtime and
                        checksums_differ(sourcefile, targetfile)
                    )
                )
            except FileNotFoundError:
                continue
            except OSError as e:
                if e.errno != errno.EMLINK:
                    printe(e)
                continue

            if not should_copy:
                continue

            yield sourcefile, targetfile


def checksum(filepath):
    hash_md5 = hashlib.md5()
    with filepath.open('rb') as f:
        while b := f.read(BLOCK_SIZE):
            hash_md5.update(b)
    return hash_md5.digest()


def checksums_differ(*filepaths):
    sums = list(executor.map(checksum, filepaths))
    return not sums or any(s != sums[0] for s in sums[1:])


# FIXME: not used, no support for symlinks
def copy3(sourcefile, targetfile):
    with sourcefile.open(mode='rb') as s, targetfile.open(mode='wb') as t:
        while b := s.read(BLOCK_SIZE):
            t.write(b)
    shutil.copystat(sourcefile, targetfile)


def copy_file(p: Progress, sourcefile, targetfile):
    if not targetfile.parent.is_dir():
        p.print(short_path(targetfile.parent), '\n')
        targetfile.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(sourcefile, targetfile, follow_symlinks=False)
        p.print(short_path(targetfile))
    except Exception as e:
        printe(e)
