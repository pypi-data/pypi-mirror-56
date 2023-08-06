import functools


def bvr_end(arg=None):
    def bvr_end_decorator(func):
        @functools.wraps(func)  # Just Keeps Identity of Function that is Decorated
        def bvr_end_wrapper(*args, **kwargs):
            return_value = func(*args, **kwargs)
            msg = ("ENDED | "
                   "FUNCTION: {} | "
                   "ARGS: {} | "
                   "KWARGS: {} ").format(func.__name__,
                                         args,
                                         kwargs)

            print(msg)

            return return_value
        return bvr_end_wrapper

    if callable(arg):
        return bvr_end_decorator(arg)

    return bvr_end_decorator
