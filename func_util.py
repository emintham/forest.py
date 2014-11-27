import types


def func_copy(f):
    """
    Returns a new copy of the function passed in.
    """
    new_f = types.FunctionType(
                f.__code__,
                f.__globals__,
                name=f.__name__,
                argdefs=f.__defaults__,
                closure=f.__closure__
            )
    new_f.__dict__.update(f.__dict__)

    return new_f
