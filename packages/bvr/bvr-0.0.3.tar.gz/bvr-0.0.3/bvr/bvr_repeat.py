import functools


def bvr_repeat(arg=None, times=2):
    def bvr_repeat_decorator(func):
        @functools.wraps(func)  # Just Keeps Identity of Function that is Decorated
        def bvr_repeat_wrapper(*args, **kwargs):
            for i in range(times):
                msg = ("REPEAT | {}/{} "
                       "FUNCTION: {} | "
                       "ARGS: {} | "
                       "KWARGS: {} ").format(i + 1,
                                             times,
                                             func.__name__,
                                             args,
                                             kwargs)

                print(msg)
                return_value = func(*args, **kwargs)

            return return_value

        return bvr_repeat_wrapper

    if callable(arg):
        return bvr_repeat_decorator(arg)

    return bvr_repeat_decorator
