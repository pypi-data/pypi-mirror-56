import functools
import time


def bvr_time(arg=None):
    def bvr_time_decorator(func):
        @functools.wraps(func)  # Just Keeps Identity of Function that is Decorated
        def bvr_time_wrapper(*args, **kwargs):
            start_time = time.time()

            return_value = func(*args, **kwargs)

            end_time = time.time()
            elapsed_time = end_time - start_time

            msg = ("TIME: {} second(s) | "
                   "FUNCTION: {} | "
                   "ARGS: {} | "
                   "KWARGS: {} ").format(elapsed_time,
                                         func.__name__,
                                         args,
                                         kwargs)

            print(msg)

            return return_value
        return bvr_time_wrapper

    if callable(arg):
        return bvr_time_decorator(arg)

    return bvr_time_decorator
