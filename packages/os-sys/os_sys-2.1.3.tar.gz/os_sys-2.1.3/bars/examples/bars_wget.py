"""An example of wrapping manual bars updates for urllib reporthook.

# urllib.urlretrieve documentation
> If present, the hook function will be called once
> on establishment of the network connection and once after each block read
> thereafter. The hook will be passed three arguments; a count of blocks
> bransferred so far, a block size in bytes, and the total size of the file.

Usage:
    bars_wget.py [options]

Options:
-h, --help
    Print this help message and exit
-u URL, --url URL  : string, optional
    The url to fetch.
    [default: https://caspersci.uk.to/matryoshka.zip]
-o FILE, --output FILE  : string, optional
    The local file path in which to save the url [default: /dev/null].
"""

import urllib
from os import devnull
from bars import bars
from docopt import docopt


def my_hook(t):
    """Wraps bars instance.

    Don't forget to close() or __exit__()
    the bars instance once you're done with it (easiest using `with` syntax).

    Example
    -------

    >>> with bars(...) as t:
    ...     reporthook = my_hook(t)
    ...     urllib.urlretrieve(..., reporthook=reporthook)

    """
    last_b = [0]

    def update_to(b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks bransferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in bars units) [default: 1].
        tsize  : int, optional
            Total size (in bars units). If [default: None] or -1,
            remains unchanged.
        """
        if tsize not in (None, -1):
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b

    return update_to


class BarsUpTo(bars):
    """Alternative Class-based version of the above.

    Provides `update_to(n)` which uses `bars.update(delta_n)`.

    Inspired by [twine#242](https://github.com/pypa/twine/pull/242),
    [here](https://github.com/pypa/twine/commit/42e55e06).
    """

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks bransferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in bars units) [default: 1].
        tsize  : int, optional
            Total size (in bars units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


opts = docopt(__doc__)

eg_link = opts['--url']
eg_file = eg_link.replace('/', ' ').split()[-1]
eg_out = opts['--output'].replace("/dev/null", devnull)
# with bars(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
#           desc=eg_file) as t:  # all optional kwargs
#     urllib.urlretrieve(eg_link, filename=eg_out,
#                        reporthook=my_hook(t), data=None)
with BarsUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
              desc=eg_file) as t:  # all optional kwargs
    urllib.urlretrieve(eg_link, filename=eg_out, reporthook=t.update_to,
                       data=None)
