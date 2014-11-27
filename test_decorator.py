import unittest
import types

from meta import check
from func_util import func_copy


def foo(bar, baz=1, bazbaz=''):
    return baz

class FuncUtilTests(unittest.TestCase):
    def foo(self, bar):
        return bar + 2

    def test_func_copy(self):
        new_f = func_copy(foo, 'new_foo')
        self.assertNotEqual(id(new_f), id(foo))
        self.assertEqual(foo(3), new_f(3))

    def test_unbound_method_copy(self):
        new_f = func_copy(self.foo, 'new_foo')
        self.assertNotEqual(id(new_f), id(self.foo))
        self.assertEqual(self.foo(1), new_f(object, 1))

    def test_bound_method_copy(self):
        new_f = func_copy(self.foo, 'new_foo')
        self.foo2 = types.MethodType(new_f, self)
        self.assertNotEqual(id(self.foo2), id(self.foo))
        self.assertEqual(self.foo(1), self.foo2(1))
