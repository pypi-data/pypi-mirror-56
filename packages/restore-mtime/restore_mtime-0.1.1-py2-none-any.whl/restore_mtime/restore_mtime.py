#!/usr/bin/env python

import argparse
import os
from tarfile import TarFile, TarInfo
import tarfile

try:
    from typing import BinaryIO, Generator
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(
        description='Restore modification time (mtime) of files from tar '
                    'archive into filesystem if the content matches')
    parser.add_argument('tar', type=file,
                        help='Source archive for mtimes')
    parser.add_argument('--root', type=str,
                        help='Directory to prepend to paths in archive. '
                             'This directory must exist. Defaults to current '
                             'working directory')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress output messages when mtime is restored')
    args = parser.parse_args()
    # Missing files under root are silently ignored:
    #  explicitly assert that root exists.
    assert args.root is None or os.path.isdir(args.root), '--root must exist'
    with tarfile.open(fileobj=args.tar) as tar:
        for info in generate_tarinfo(tar):
            try:
                if not (info.isfile()):
                    continue
                fname = info.name if args.root is None \
                    else os.path.join(args.root, info.name)
                if os.stat(fname).st_size != info.size:
                    continue
                with open(fname, 'rb') as fp:
                    if file_cmp(tar.extractfile(info), fp):
                        os.utime(fname, (info.mtime, info.mtime))
                        if not args.quiet:
                            print('mtime restored: {}'.format(fname))
            except (IOError, OSError) as _:
                pass  # we don't care about files that don't exist


def generate_tarinfo(tar):
    # type: (TarFile) -> Generator[TarInfo]
    """ Generate all members of TarFile. Members are discarded after each iteration """
    while True:
        info = tar.next()
        if info:
            yield info
            tar.members = []
        else:
            return


def file_cmp(fp1, fp2, bufsize=8 * 1024):
    # type: (BinaryIO, BinaryIO, int) -> bool
    """ Like filecmp.cmp except arguments are file-like objects instead of file names """
    while True:
        b1 = fp1.read(bufsize)
        b2 = fp2.read(bufsize)
        if b1 != b2:
            return False
        if not b1:
            return True


if __name__ == '__main__':
    main()
