from bvr.bvr_start_end import bvr_start_end


def test_bvr_start_end_end_called_as_decorator(capsys):

    @bvr_start_end
    def start_end():
        return 2

    return_value = start_end()

    assert return_value == 2
    assert "STARTED | FUNCTION: start_end | ARGS: () | KWARGS: {} \nENDED | FUNCTION: start_end | ARGS: () | KWARGS: {} " in capsys.readouterr().out
    assert start_end.__name__ == "start_end"  # Important for decorators to not override method name


def test_bvr_start_end_called_as_callable_returning_decorator(capsys):

    @bvr_start_end()
    def start_end():
        return 2

    return_value = start_end()
    assert return_value == 2
    assert "STARTED | FUNCTION: start_end | ARGS: () | KWARGS: {} \nENDED | FUNCTION: start_end | ARGS: () | KWARGS: {} " in capsys.readouterr().out
    assert start_end.__name__ == "start_end"  # Important for decorators to not override method name


def test_bvr_start_end_called_as_decorator_with_function_args(capsys):

    @bvr_start_end
    def start_end(msg):
        print(msg)
        return 2

    return_value = start_end("Hello")
    assert return_value == 2
    assert "STARTED | FUNCTION: start_end | ARGS: ('Hello',) | KWARGS: {} \nHello\nENDED | FUNCTION: start_end | ARGS: ('Hello',) | KWARGS: {} " in capsys.readouterr().out
    assert start_end.__name__ == "start_end"  # Important for decorators to not override method name


def test_bvr_start_end_called_as_decorator_with_function_kwargs(capsys):

    @bvr_start_end
    def start_end(msg):
        print(msg)
        return 2

    return_value = start_end(msg="Hello")
    assert return_value == 2
    assert "STARTED | FUNCTION: start_end | ARGS: () | KWARGS: {'msg': 'Hello'} \nHello\nENDED | FUNCTION: start_end | ARGS: () | KWARGS: {'msg': 'Hello'} " in capsys.readouterr().out
    assert start_end.__name__ == "start_end"  # Important for decorators to not override method name


def test_bvr_start_end_called_as_callable_returning_decorator_with_function_args(capsys):

    @bvr_start_end()
    def start_end(msg):
        print(msg)
        return 2

    return_value = start_end("Hello")
    assert return_value == 2
    assert "STARTED | FUNCTION: start_end | ARGS: ('Hello',) | KWARGS: {} \nHello\nENDED | FUNCTION: start_end | ARGS: ('Hello',) | KWARGS: {} " in capsys.readouterr().out
    assert start_end.__name__ == "start_end"  # Important for decorators to not override method name


def test_bvr_start_end_called_as_callable_returning_decorator_with_function_kwargs(capsys):

    @bvr_start_end()
    def start_end(msg):
        print(msg)
        return 2

    return_value = start_end(msg="Hello")
    assert return_value == 2
    assert "STARTED | FUNCTION: start_end | ARGS: () | KWARGS: {'msg': 'Hello'} \nHello\n" in capsys.readouterr().out
    assert start_end.__name__ == "start_end"  # Important for decorators to not override method name
