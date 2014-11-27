
@typecheck
class TestClass(object):
    def __init__(self, param_type=None):
        if param_type:
            self._param_type = param_type

    @check(foo=int)
    def checked_method(self, foo):
        self.foo = foo + 1
        print(self.foo)

    def unchecked_method(self, bar):
        self.bar = bar
        print(self.bar)

    @check(baz=list)
    def checked_class_method(cls, baz):
        cls.class_baz = baz.reverse
        print(cls.class_baz)

class MetaTests(unittest.TestCase):
    def setUp(self):
        pass


