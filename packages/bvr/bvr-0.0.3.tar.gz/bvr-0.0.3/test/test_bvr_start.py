from bvr.bvr_start import bvr_start


def test_bvr_start_called_as_decorator(capsys):

    @bvr_start
    def start():
        return 2

    return_value = start()

    assert return_value == 2
    assert "STARTED | FUNCTION: start | ARGS: () | KWARGS: {}" in capsys.readouterr().out
    assert start.__name__ == "start"  # Important for decorators to not override method name


def test_bvr_start_called_as_callable_returning_decorator(capsys):

    @bvr_start()
    def start():
        return 2

    return_value = start()
    assert return_value == 2
    assert "STARTED | FUNCTION: start | ARGS: () | KWARGS: {}" in capsys.readouterr().out
    assert start.__name__ == "start"  # Important for decorators to not override method name


def test_bvr_start_called_as_decorator_with_function_args(capsys):

    @bvr_start
    def start(msg):
        print(msg)
        return 2

    return_value = start("Hello")
    assert return_value == 2
    assert "STARTED | FUNCTION: start | ARGS: ('Hello',) | KWARGS: {} \nHello\n" in capsys.readouterr().out
    assert start.__name__ == "start"  # Important for decorators to not override method name


def test_bvr_start_called_as_decorator_with_function_kwargs(capsys):

    @bvr_start
    def start(msg):
        print(msg)
        return 2

    return_value = start(msg="Hello")
    assert return_value == 2
    assert "STARTED | FUNCTION: start | ARGS: () | KWARGS: {'msg': 'Hello'} \nHello\n" in capsys.readouterr().out
    assert start.__name__ == "start"  # Important for decorators to not override method name


def test_bvr_start_called_as_callable_returning_decorator_with_function_args(capsys):

    @bvr_start()
    def start(msg):
        print(msg)
        return 2

    return_value = start("Hello")
    assert return_value == 2
    assert "STARTED | FUNCTION: start | ARGS: ('Hello',) | KWARGS: {} \nHello\n" in capsys.readouterr().out
    assert start.__name__ == "start"  # Important for decorators to not override method name


def test_bvr_start_called_as_callable_returning_decorator_with_function_kwargs(capsys):

    @bvr_start()
    def start(msg):
        print(msg)
        return 2

    return_value = start(msg="Hello")
    assert return_value == 2
    assert "STARTED | FUNCTION: start | ARGS: () | KWARGS: {'msg': 'Hello'} \nHello\n" in capsys.readouterr().out
    assert start.__name__ == "start"  # Important for decorators to not override method name

