import contextlib
import inspect
import os


@contextlib.contextmanager
def contents():
    frame_records = inspect.stack()[2]
    calling_module = inspect.getmodulename(frame_records[1])
    with open(os.path.join("inputs", f"{calling_module}.txt"), "r") as fp:
        yield fp.read()
