import functools


def bvr_hi(arg=None):
    def bvr_hi_decorator(func):
        @functools.wraps(func)  # Just Keeps Identity of Function that is Decorated
        def bvr_hi_wrapper(*args, **kwargs):
            print("Hi")
            return_value = func(*args, **kwargs)
            print("Hi")
            return return_value
        return bvr_hi_wrapper

    if callable(arg):
        return bvr_hi_decorator(arg)

    return bvr_hi_decorator
