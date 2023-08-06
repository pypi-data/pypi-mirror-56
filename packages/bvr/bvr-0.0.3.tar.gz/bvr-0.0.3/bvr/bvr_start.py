import functools


def bvr_start(arg=None):
    def bvr_start_decorator(func):
        @functools.wraps(func)  # Just Keeps Identity of Function that is Decorated
        def bvr_start_wrapper(*args, **kwargs):
            msg = ("STARTED | "
                   "FUNCTION: {} | "
                   "ARGS: {} | "
                   "KWARGS: {} ").format(func.__name__,
                                         args,
                                         kwargs)

            print(msg)

            return_value = func(*args, **kwargs)
            return return_value
        return bvr_start_wrapper

    if callable(arg):
        return bvr_start_decorator(arg)

    return bvr_start_decorator
