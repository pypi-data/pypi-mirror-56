from bvr.logger import Logger


def bvr_try(arg=None, logger_class=None, exception_type=Exception, should_raise=True, custom_exception=None, custom_message=None):

    if not logger_class:
        logger_class = Logger()

    if not hasattr(logger_class, 'error'):
        # TODO: test
        raise AttributeError("logger_class argument must have attribute error to properly log error")

    if not isinstance(exception_type, Exception.__class__):
        # TODO: test
        raise TypeError("{} argument must be of type {} ".format("exception_type", Exception.__class__))

    if not isinstance(should_raise, bool):
        # TODO: test
        raise TypeError("{} argument must be of type {} ".format("should_raise", bool.__class__))

    if not isinstance(custom_exception, Exception.__class__) or custom_exception is not None:
        # TODO: test
        raise TypeError("{} argument must be of type {} ".format("custom_exception", Exception.__class__))

    if not isinstance(custom_message, str) or custom_message is not None:
        # TODO: test
        raise TypeError("{} argument must be of type {} ".format("custom_message", str.__class__))

    def bvr_try_decorator(func):

        def bvr_try_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_type as exception:  # pylint: disable=broad-except

                msg = ("ERROR: Caught Exception | "
                       "FUNCTION: {} | "
                       "BASE_EXCEPTION: {} | "
                       "EXCEPTION: {} | "
                       "MESSAGE: {} | "
                       "RAISE: {} ").format(func.__name__,
                                            exception_type.__name__,
                                            type(exception).__name__,
                                            exception,
                                            should_raise)

                logger_class.error(msg)

                if should_raise is True:
                    if custom_exception:
                        raise custom_exception(msg) from exception

                    if not custom_exception:
                        raise

        return bvr_try_wrapper

    if callable(arg):
        return bvr_try_decorator(arg)

    return bvr_try_decorator
