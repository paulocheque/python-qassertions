'''
Created on Jul 27, 2009
@author: Paulo Cheque (paulocheque@gmail.com)
'''

import unittest
import qassertions as qa
from qassertions import Min, Max, Range, InList, NotInList, Blank, NonBlank

class MyClassUnderTest(object):

    def method_under_test(self, value1, value2, value3, value4, value5, value6):
        if value1 < 5: raise Exception('validation problem')
        if value2 > 7: raise Exception('validation problem')
        if value4 < 5 or value4 > 10: raise Exception('validation problem')
        if value6 not in [1, 5, 7]: raise Exception('validation problem')
        
    def bugged_method_under_test_1(self, value1, value2):
        if value2 < 6: raise Exception('validation problem')
        
    def bugged_method_under_test_2(self, value1, value2):
        if value2 > 8: raise Exception('validation problem')
        
    def bugged_method_under_test_3(self, value1, value2):
        if value2 < 3 or value2 > 11: raise Exception('validation problem')
        
    def bugged_method_under_test_4(self, value1, value2):
        if value2 not in [4]: raise Exception('validation problem')

class MyTests(unittest.TestCase):

    def setUp(self):
        self.my = MyClassUnderTest()

    def tests_example_of_success(self):
        qa.assertValidation(self.my.method_under_test, Min(5), Max(7, 0.1), 'dummy1', Range(5, 10), 'dummy2', InList([1, 5, 7]))
        
    def tests_example_of_failure_1(self):
        qa.assertValidation(self.my.bugged_method_under_test_1, 'dummy1', Min(5))
        
    def tests_example_of_failure_2(self):
        qa.assertValidation(self.my.bugged_method_under_test_2, 'dummy1', Max(9))
        
    def tests_example_of_failure_3(self):
        qa.assertValidation(self.my.bugged_method_under_test_3, 'dummy1', Range(2, 10))
        
    def tests_example_of_failure_4(self):
        qa.assertValidation(self.my.bugged_method_under_test_4, 'dummy1', InList([5]))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()