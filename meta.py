from functools import wraps
from inspect import getargspec


class InvalidUse(Exception): pass
class UnknownParam(Exception): pass
class InvalidArgument(Exception): pass
class InvalidDefaultArgument(Exception): pass


def check(*params, **kwparams):
    """
    Decorator for typechecking. Should only be used with kwargs.
    eg.
        @check(foo=int, bar=str)
        def baz(foo, bar):
            print(foo + 1)
            print(bar.reverse)
    """
    if len(params) > 0:
        raise InvalidUse('Decorator should only be used with kwparams')

    print('kwparams: {}'.format(kwparams))
    def validate_func_params(f):
        argspec = getargspec(f)
        print(argspec)
        for key in iter(kwparams):
            # confirm kwparams are named in the function
            if key not in argspec.args:
                raise UnknownParam('{} not in {}'.format(key, f.__name__))
            # validate that arguments passed into decorator are types
            elif not isinstance(kwparams[key], type):
                raise InvalidArgument('{} is not a type!'.format(kwparams[key]))

        num_defaults = len(argspec.defaults)
        kw_with_defaults = zip(argspec.args[-num_defaults:], argspec.defaults)
        for kw, default in kw_with_defaults:
            if not isinstance(default, kwparams[kw]):
                raise InvalidDefaultArgument(
                    '{} is not of type {}'.format(default, kwparams[kw]))

    def wrapper(func):
        validate_func_params(func)

        @wraps(func)
        def wrapped_f(*args, **kwargs):
            print('foo')
            func(*args, **kwargs)
            print('bar')
        return wrapped_f
    return wrapper
