import functools
from time import sleep


def bvr_rest(arg=None, seconds=1):
    def bvr_rest_decorator(func):
        @functools.wraps(func)  # Just Keeps Identity of Function that is Decorated
        def bvr_rest_wrapper(*args, **kwargs):
            msg = ("RESTING: {} second(s) | "
                   "FUNCTION: {} | "
                   "ARGS: {} | "
                   "KWARGS: {} ").format(seconds,
                                         func.__name__,
                                         args,
                                         kwargs)

            print(msg)

            sleep(seconds)

            return_value = func(*args, **kwargs)

            return return_value

        return bvr_rest_wrapper

    if callable(arg):
        return bvr_rest_decorator(arg)

    return bvr_rest_decorator
