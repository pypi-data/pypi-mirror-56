from bvr.bvr_time import bvr_time


def test_bvr_time_end_called_as_decorator(capsys):

    @bvr_time
    def time():
        return 2

    return_value = time()

    system_output = capsys.readouterr().out

    assert return_value == 2
    assert "TIME: " in system_output
    assert " | FUNCTION: time | ARGS: () | KWARGS: {}" in system_output
    assert time.__name__ == "time"  # Important for decorators to not override method name


def test_bvr_time_called_as_callable_returning_decorator(capsys):

    @bvr_time()
    def time():
        return 2

    return_value = time()
    system_output = capsys.readouterr().out

    assert return_value == 2
    assert "TIME: " in system_output
    assert " | FUNCTION: time | ARGS: () | KWARGS: {}" in system_output
    assert time.__name__ == "time"  # Important for decorators to not override method name


def test_bvr_time_called_as_decorator_with_function_args(capsys):

    @bvr_time
    def time(msg):
        print(msg)
        return 2

    return_value = time("Hello")
    system_output = capsys.readouterr().out

    assert return_value == 2
    assert "Hello\nTIME: " in system_output
    assert " | FUNCTION: time | ARGS: ('Hello',) | KWARGS: {}" in system_output
    assert time.__name__ == "time"  # Important for decorators to not override method name


def test_bvr_time_called_as_decorator_with_function_kwargs(capsys):

    @bvr_time
    def time(msg):
        print(msg)
        return 2

    return_value = time(msg="Hello")
    system_output = capsys.readouterr().out

    assert return_value == 2
    assert "Hello\nTIME: " in system_output
    assert " | FUNCTION: time | ARGS: () | KWARGS: {'msg': 'Hello'}" in system_output
    assert time.__name__ == "time"  # Important for decorators to not override method name


def test_bvr_time_called_as_callable_returning_decorator_with_function_args(capsys):

    @bvr_time()
    def time(msg):
        print(msg)
        return 2

    return_value = time("Hello")
    system_output = capsys.readouterr().out

    assert return_value == 2
    assert "Hello\nTIME: " in system_output
    assert " | FUNCTION: time | ARGS: ('Hello',) | KWARGS: {}" in system_output
    assert time.__name__ == "time"  # Important for decorators to not override method name


def test_bvr_time_called_as_callable_returning_decorator_with_function_kwargs(capsys):

    @bvr_time()
    def time(msg):
        print(msg)
        return 2

    return_value = time(msg="Hello")
    system_output = capsys.readouterr().out

    assert return_value == 2
    assert "Hello\nTIME: " in system_output
    assert " | FUNCTION: time | ARGS: () | KWARGS: {'msg': 'Hello'}" in system_output
    assert time.__name__ == "time"  # Important for decorators to not override method name
