

def bvr_compose(arg=None, *decorators):
    def bvr_compose_decorator(func):
        for decorator in decorators:
            print("ONE")
            print(decorator.__name__)
            func = decorator(func)
        return func

    if callable(arg):
        return bvr_compose_decorator(arg)

    return bvr_compose_decorator

# TODO: could this be a thing
from bvr.bvr_hi import bvr_hi
from bvr.bvr_start import bvr_start
from bvr.bvr_end import bvr_end
from bvr.bvr_rest import bvr_rest


@bvr_compose(bvr_end, bvr_rest(seconds=4), bvr_start)
def do_hello():
    print("hello")


do_hello()
