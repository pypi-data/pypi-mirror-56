from bvr.bvr_start import bvr_start
from bvr.bvr_end import bvr_end


def bvr_start_end(arg=None):
    def bvr_start_end_decorator(func):
        func = bvr_start(func)
        func = bvr_end(func)

        return func

    if callable(arg):
        return bvr_start_end_decorator(arg)

    return bvr_start_end_decorator
