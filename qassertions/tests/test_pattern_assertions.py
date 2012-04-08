import unittest

import qassertions as qa
from qassertions import pattern_assertions as pa
from qassertions.pattern_assertions import *


class Singleton(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance


class MySingleton(Singleton):
    pass


class DesignPattern_AssertSingletonTests(unittest.TestCase):

    def test_class_is_a_singleton_get_success(self):
        pa.assertSingleton(MySingleton)

    def test_class_is_not_a_singleton_throws_an_assertion_error(self):
        class NotSingleton():
            pass
        qa.assertExceptionMessage('The class NotSingleton is not a singleton.',
                                  pa.assertSingleton, NotSingleton)


class MyPrototype(object):
    def __init__(self, x=3):
        self.x = x

    def __eq__(self, other):
        return self.x == other.x

    def __ne__(self, other):
        return not self.__eq__(other)

    def clone(self):
        import copy
        return copy.deepcopy(self)

    def copy(self):
        return self.clone()


class DesignPattern_AssertPrototypeTests(unittest.TestCase):
    def test_class_is_prototype_get_success(self):
        pa.assertPrototype(MyPrototype())

    def test_class_is_prototype_with_custom_method_get_success(self):
        pa.assertPrototype(MyPrototype(), 'copy')

    def test_class_is_not_prototype_throws_an_assertion_error(self):
        class NotPrototype():
            def clone(self):
                pass
        qa.assertExceptionMessage('The class NotPrototype is not a prototype.',
                                  pa.assertPrototype, NotPrototype())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
