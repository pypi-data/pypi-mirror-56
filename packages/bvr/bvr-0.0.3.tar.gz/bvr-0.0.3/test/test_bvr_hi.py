from bvr.bvr_hi import bvr_hi


def test_bvr_hi_called_as_decorator(capsys):

    @bvr_hi
    def hi():
        return 2

    return_value = hi()

    assert return_value == 2
    assert "Hi\nHi\n" in capsys.readouterr().out
    assert hi.__name__ == "hi"  # Important for decorators to not override method name


def test_bvr_hi_called_as_callable_returning_decorator(capsys):

    @bvr_hi()
    def hi():
        return 2

    return_value = hi()

    assert return_value == 2
    assert "Hi\nHi\n" in capsys.readouterr().out
    assert hi.__name__ == "hi"  # Important for decorators to not override method name


def test_bvr_hi_called_as_decorator_with_function_args(capsys):

    @bvr_hi
    def hi(msg):
        print(msg)
        return msg

    return_value = hi("Hello")

    assert return_value == "Hello"
    assert "Hi\nHello\nHi\n" in capsys.readouterr().out
    assert hi.__name__ == "hi"  # Important for decorators to not override method name


def test_bvr_hi_called_as_callable_returning_decorator_with_function_args(capsys):

    @bvr_hi()
    def hi(msg):
        print(msg)
        return msg

    return_value = hi("Hello")

    assert return_value == "Hello"
    assert "Hi\nHello\nHi\n" in capsys.readouterr().out
    assert hi.__name__ == "hi"  # Important for decorators to not override method name
