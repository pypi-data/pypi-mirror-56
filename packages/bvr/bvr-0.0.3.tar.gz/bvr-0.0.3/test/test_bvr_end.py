from bvr.bvr_end import bvr_end


def test_bvr_end_called_as_decorator(capsys):

    @bvr_end
    def end():
        return 2

    return_value = end()

    assert return_value == 2
    assert "ENDED | FUNCTION: end | ARGS: () | KWARGS: {}" in capsys.readouterr().out
    assert end.__name__ == "end"  # Important for decorators to not override method name


def test_bvr_end_called_as_callable_returning_decorator(capsys):

    @bvr_end()
    def end():
        return 2

    return_value = end()
    assert return_value == 2
    assert "ENDED | FUNCTION: end | ARGS: () | KWARGS: {}" in capsys.readouterr().out
    assert end.__name__ == "end"  # Important for decorators to not override method name


def test_bvr_end_called_as_decorator_with_function_args(capsys):

    @bvr_end
    def end(msg):
        print(msg)
        return 2

    return_value = end("Hello")
    assert return_value == 2
    assert "Hello\nENDED | FUNCTION: end | ARGS: ('Hello',) | KWARGS: {}" in capsys.readouterr().out
    assert end.__name__ == "end"  # Important for decorators to not override method name


def test_bvr_end_called_as_decorator_with_function_kwargs(capsys):

    @bvr_end
    def end(msg):
        print(msg)
        return 2

    return_value = end(msg="Hello")
    assert return_value == 2
    assert "Hello\nENDED | FUNCTION: end | ARGS: () | KWARGS: {'msg': 'Hello'}" in capsys.readouterr().out
    assert end.__name__ == "end"  # Important for decorators to not override method name


def test_bvr_end_called_as_callable_returning_decorator_with_function_args(capsys):

    @bvr_end()
    def end(msg):
        print(msg)
        return 2

    return_value = end("Hello")
    assert return_value == 2
    assert "Hello\nENDED | FUNCTION: end | ARGS: ('Hello',) | KWARGS: {}" in capsys.readouterr().out
    assert end.__name__ == "end"  # Important for decorators to not override method name


def test_bvr_end_called_as_callable_returning_decorator_with_function_kwargs(capsys):

    @bvr_end()
    def end(msg):
        print(msg)
        return 2

    return_value = end(msg="Hello")
    assert return_value == 2
    assert "Hello\nENDED | FUNCTION: end | ARGS: () | KWARGS: {'msg': 'Hello'}" in capsys.readouterr().out
    assert end.__name__ == "end"  # Important for decorators to not override method name

