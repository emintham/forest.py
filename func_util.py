import types


def func_copy(f, name, bind=False):
    """
    Returns a new copy of the function passed in.
    """
    if (not isinstance(f, types.FunctionType) and
        not isinstance(f, types.MethodType)):
        raise TypeError('Expecting a function type, got {}'.format(type(f)))
    else:
        if not name:
            name = f.__name__

        new_f = types.FunctionType(
                    f.__code__,
                    f.__globals__,
                    name=name,
                    argdefs=f.__defaults__,
                    closure=f.__closure__
                )
        new_f.__dict__.update(f.__dict__)

        if bind:
            return new_f
        else:
            bound_new_f = types.MethodType(new_f, 
