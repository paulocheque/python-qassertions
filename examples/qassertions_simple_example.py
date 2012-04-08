'''
Created on Jul 27, 2009
@author: Paulo Cheque (paulocheque@gmail.com)
'''

import unittest
import qassertions as qa
from qassertions import Min, Max, Range, InList, NotInList, Blank, NonBlank

class MyClassUnderTest(object):

    def method_under_test(self, some_not_testable_value, my_testable_value):
        pass # some implementation...
    
    def clean_method(self, some_value1, some_value2):
        pass # some implementation...
    
    def raise_exception_method(self, some_value1, some_value2):
        raise Exception("ops")
        pass # some implementation...

class MyTests(unittest.TestCase):

    def setUp(self):
        self.my = MyClassUnderTest()

    def tests_assert_performance(self):
        qa.assertPerformance(1, self.my.clean_method, 1, 2)
        
    def tests_dont_raise_exception_1(self):
        qa.assertDontRaiseAnException(self.my.clean_method, 1, 2)
        
    def tests_dont_raise_exception_2(self):
        # The following method will fail
        qa.assertDontRaiseAnException(self.my.raise_exception_method, 1, 2)
        
    def tests_exception_message_1(self):
        qa.assertExceptionMessage("ops", self.my.raise_exception_method, 1, 2)
        
    def tests_exception_message_2(self):
        qa.assertExceptionMessage("this assertion will fail", self.my.raise_exception_method, 1, 2)
        
    def tests_exception_message_3(self):
        qa.assertExceptionMessage("this assertion will fail", self.my.clean_method, 1, 2)

    def tests_example_to_see_error_message_Min_1(self):
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is 4
        # Expect success if 'my_testable_value' is 5
        # Expect success if 'my_testable_value' is 6
        qa.assertValidation(self.my.method_under_test, 'some valid value', Min(5))
        
    def tests_example_to_see_error_message_Min_2(self):
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is 4.9
        # Expect success if 'my_testable_value' is 5
        # Expect success if 'my_testable_value' is 5.1
        qa.assertValidation(self.my.method_under_test, 'some valid value', Min(5, 0.1))
        
    def tests_example_to_see_error_message_Min_3(self):
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is 4.8
        # Expect success if 'my_testable_value' is 5
        # Expect success if 'my_testable_value' is 5.2
        qa.assertValidation(self.my.method_under_test, 'some valid value', Min(5, 0.2))
        
    def tests_example_to_see_error_message_Max_1(self):
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is 11
        # Expect success if 'my_testable_value' is 9
        # Expect success if 'my_testable_value' is 10
        qa.assertValidation(self.my.method_under_test, 'some valid value', Max(10))
        
    def tests_example_to_see_error_message_Max_2(self):
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is 13.2
        # Expect success if 'my_testable_value' is 6.8
        # Expect success if 'my_testable_value' is 10
        qa.assertValidation(self.my.method_under_test, 'some valid value', Max(10, 3.2))
        
    def tests_example_to_see_error_message_Range_1(self):
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is 0
        # Expect an exception if 'my_testable_value' is 3
        # Expect success if 'my_testable_value' is 1
        # Expect success if 'my_testable_value' is 2
        qa.assertValidation(self.my.method_under_test, 'some valid value', Range(1, 2))
        
    def tests_example_to_see_error_message_Range_2(self):
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is 0.99
        # Expect an exception if 'my_testable_value' is 2.01
        # Expect success if 'my_testable_value' is 1
        # Expect success if 'my_testable_value' is 2
        qa.assertValidation(self.my.method_under_test, 'some valid value', Range(1, 2, 0.01))
        
    def tests_example_to_see_error_message_InList_1(self):
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is 0
        # Expect an exception if 'my_testable_value' is 9
        # Expect success if 'my_testable_value' is 1
        # Expect success if 'my_testable_value' is 7
        # Expect success if 'my_testable_value' is 8
        qa.assertValidation(self.my.method_under_test, 'some valid value', InList([1, 2, 7, 8]))
        
    def tests_example_to_see_error_message_InList_2(self):
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is 0
        # Expect an exception if 'my_testable_value' is 10
        # Expect success if 'my_testable_value' is 1
        # Expect success if 'my_testable_value' is 7
        # Expect success if 'my_testable_value' is 9
        qa.assertValidation(self.my.method_under_test, 'some valid value', InList([1, 2, 7, 8, 9]))
        
    def tests_example_to_see_error_message_NotInList_1(self):
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is 1
        # Expect an exception if 'my_testable_value' is 7
        # Expect an exception if 'my_testable_value' is 9
        # Expect success if 'my_testable_value' is 0
        # Expect success if 'my_testable_value' is 10
        qa.assertValidation(self.my.method_under_test, 'some valid value', NotInList([1, 2, 7, 8, 9]))
        
    def tests_example_to_see_error_message_Blank_1(self):
        # You can overwrite/rewrite this method if these values are not good
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is None
        # Expect success if 'my_testable_value' is ''
        # Expect success if 'my_testable_value' is ' '
        # Expect success if 'my_testable_value' is '\t'
        qa.assertValidation(self.my.method_under_test, 'some valid value', Blank())
        
    def tests_example_to_see_error_message_NonBlank_1(self):
        # You can overwrite/rewrite this method if these values are not good
        # This will make the following tests:
        # Expect an exception if 'my_testable_value' is ''
        # Expect an exception if 'my_testable_value' is ' '
        # Expect an exception if 'my_testable_value' is '\t'
        # Expect success if 'my_testable_value' is 'a'
        # Expect success if 'my_testable_value' is 'abc'
        qa.assertValidation(self.my.method_under_test, 'some valid value', NonBlank())
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()