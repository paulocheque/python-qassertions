'''
Example of usage: qassertions_simple_example.py
A more complex example: qassertions_example.py

This module has additional assertions to facilitate writing good automated tests. It includes assertion methods that
verify design patterns behavior. These assertions make the tests more clean and legible.  

assertSingleton
assertPrototype
'''

failureException = AssertionError


def assertSingleton(clazz):
    '''
    Assert that class is a implementation of the design pattern Singleton. 
    '''
    a = clazz()
    b = clazz()
    if (a is not b):
        raise failureException("The class %s is not a singleton." % (clazz.__name__))


def assertPrototype(instance, method='clone'):
    '''
    Assert that instance is a implementation of the design pattern Prototype. 
    '''
    clone = instance.__class__.__dict__[method](instance)
    if(instance != clone or id(instance) == id(clone)):
        raise failureException("The class %s is not a prototype." % (instance.__class__.__name__))


# TODO method create may have parameters
def assertBuilder(builder_class, method='create', object_class):
    instance = builder_class.__dict__[method](builder_class())
    if not isinstance(instance, object_class):
        raise failureException("The class %s is not a builder of %s." % (builder_class.__name__, object_class.__name__))


def assertDelegate(method_adapter, method_delegate):
    pass





