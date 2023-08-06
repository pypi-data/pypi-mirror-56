"""Redirecting writing

If using a library that can print messages to the console, editing the library
by  replacing `print()` with `bars.write()` may not be desirable.
In that case, redirecting `sys.stdout` to `bars.write()` is an option.

To redirect `sys.stdout`, create a file-like class that will write
any input string to `bars.write()`, and supply the arguments
`file=sys.stdout, dynamic_ncols=True`.

A reusable canonical example is given below:
"""
from __future__ import print_function
from time import sleep
import contextlib
import sys
from bars import bars


class DummyBarsFile(object):
    """Dummy file-like that will write to bars"""
    file = None

    def __init__(self, file):
        self.file = file

    def write(self, x):
        # Avoid print() second call (useless \n)
        if len(x.rstrip()) > 0:
            bars.write(x, file=self.file)

    def flush(self):
        return getattr(self.file, "flush", lambda: None)()


@contextlib.contextmanager
def std_out_err_redirect_bars():
    orig_out_err = sys.stdout, sys.stderr
    try:
        # sys.stdout = sys.stderr = DummyBarsFile(orig_out_err[0])
        sys.stdout, sys.stderr = map(DummyBarsFile, orig_out_err)
        yield orig_out_err[0]
    # Relay exceptions
    except Exception as exc:
        raise exc
    # Always restore sys.stdout/err if necessary
    finally:
        sys.stdout, sys.stderr = orig_out_err


def some_fun(i):
    print("Fee, fi, fo,".split()[i])


# Redirect stdout to bars.write()
with std_out_err_redirect_bars() as orig_stdout:
    # bars needs the original stdout
    # and dynamic_ncols=True to autodetect console width
    for i in bars(range(3), file=orig_stdout, dynamic_ncols=True):
        # order of the following two lines should not matter
        some_fun(i)
        sleep(.5)

# After the `with`, printing is restored
print("Done!")
