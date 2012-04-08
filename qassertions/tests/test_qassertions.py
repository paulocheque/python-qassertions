import time
import unittest

import qassertions as qa
from qassertions import *


class AssertDontRaiseAnExceptionTests(unittest.TestCase):
    def test_CaseOfSuccess(self):
        def some_method(value1):
            pass
        qa.assertDontRaiseAnException(some_method, 1)

    def test_CaseOfFailure(self):
        def some_method(value1):
            if(value1 == 1):
                raise Exception("Some msg")
        try:
            qa.assertDontRaiseAnException(some_method, 1)
        except AssertionError, e:
            self.assertEquals("It was not expect an exception, but it get a Exception: Some msg",
                              str(e))


class AssertExceptionMessageTests(unittest.TestCase):
    def test_CaseOfSuccess(self):
        def some_method():
            raise Exception("some msg")
        qa.assertExceptionMessage("some msg", some_method)

    def test_CaseOfSuccessOfOneVariableValueInMessage(self):
        def some_method():
            raise Exception("some msg: 0.134")
        qa.assertExceptionMessage("some msg: [...]", some_method)

    def test_CaseOfSuccessOfTwoVariableValuesInMessage(self):
        def some_method():
            raise Exception("some msg: 0.134s of some method zzz")
        qa.assertExceptionMessage("some msg: [...] of some method [...]", some_method)

    def test_CaseOfFailureOfOneVariableValueInMessage(self):
        def some_method():
            raise Exception("some msg: 0.134")
        try:
            qa.assertExceptionMessage("some msg2: [...]", some_method)
        except AssertionError, e:
            self.assertEquals("It was expected an exception with message 'some msg2: [...]', but receive 'some msg: 0.134'",
                              str(e))

    def test_ButNoExceptionIsRaised(self):
        def some_method():
            pass
        try:
            qa.assertExceptionMessage("some msg", some_method)
        except AssertionError, e:
            self.assertEquals("It was expected an exception.", str(e))

    def test_GetAnExceptionButWithADifferentMessage(self):
        def some_method():
            raise Exception("some msg2")
        try:
            qa.assertExceptionMessage("some msg", some_method)
        except AssertionError, e:
            self.assertEquals("It was expected an exception with message 'some msg', but receive 'some msg2'",
                              str(e))


class ValidationTestResultTests(unittest.TestCase):
    def setUp(self):
        self.result = ValidationTestResult()

    def testAddUnexpectedSuccess(self):
        self.result.addUnexpectedSuccess([1, 2, ''])
        self.assertEquals('Unexpected success for the combination of arguments:\n> 1, 2, ''', str(self.result))

    def testAddUnexpectedFailure(self):
        self.result.addUnexpectedFailure('some error msg', [1, 2, ''])
        self.assertEquals('Unexpected failure for the combination of arguments:\n> 1, 2, '' - some error msg', str(self.result))

    def testAddUnexpectedFailureAndSuccess(self):
        self.result.addUnexpectedSuccess([1, 2, 'a'])
        self.result.addUnexpectedFailure('some error msg', [8, 7, 'b'])
        self.result.addUnexpectedSuccess([3, 4, 'c'])
        self.result.addUnexpectedFailure('some error msg2', [5, 6, ''])
        self.assertEquals(
'''Unexpected success for the combination of arguments:
> 1, 2, a
> 3, 4, c
Unexpected failure for the combination of arguments:
> 8, 7, b - some error msg
> 5, 6,  - some error msg2''', str(self.result))

    def testResultHasNoFailures(self):
        self.assertFalse(self.result.hasFailure())

    def testResultHasFailuresByUnexpectedSuccess(self):
        self.result.addUnexpectedSuccess(['1'])
        self.assertTrue(self.result.hasFailure())

    def testResultHasFailuresByUnexpectedFailure(self):
        self.result.addUnexpectedFailure('', ['1'])
        self.assertTrue(self.result.hasFailure())


class MinValidationTests(unittest.TestCase):
    def testMinSuccessValues(self):
        self.assertEquals([5, 6, 15], Min(5).successValues())
        self.assertEquals([5.123, 6.123, (5.123 + 10)], Min(5.123).successValues())
        self.assertEquals([5.123, 5.223, 6.123], Min(5.123, 0.1).successValues())

    def testMinSuccessValuesForNegativeNumbers(self):
        self.assertEquals([-5, -4, 5], Min(-5).successValues())

    def testMinFailureValues(self):
        self.assertEquals([-5, 4], Min(5).failureValues())
        self.assertEquals([4, 4.9], Min(5, 0.1).failureValues())

    def testMinFailureValuesForNegativeNumbers(self):
        self.assertEquals([-15, -6], Min(-5).failureValues())


class MaxValidationTests(unittest.TestCase):
    def testMaxSuccessValues(self):
        self.assertEquals([-4, 5, 6], Max(6).successValues())
        self.assertEquals([5, 5.9, 6], Max(6, 0.1).successValues())

    def testMaxSuccessValuesForNegativeNumbers(self):
        self.assertEquals([-15, -6, -5], Max(-5).successValues())

    def testMaxFailureValues(self):
        self.assertEquals([6, 15], Max(5).failureValues())
        self.assertEquals([5.1, 6], Max(5, 0.1).failureValues())

    def testMaxFailureValuesForNegativeNumbers(self):
        self.assertEquals([-4, 5], Max(-5).failureValues())


class PositiveValidationTests(unittest.TestCase):
    def testMinSuccessValues(self):
        self.assertEquals([1, 2, 11], Positive().successValues())
        self.assertEquals([1, 1.1, 2], Positive(0.1).successValues())

    def testMinFailureValues(self):
        self.assertEquals([-1, 0], Positive().failureValues())
        self.assertEquals([-0.1, 0], Positive(0.1).failureValues())


class  NegativeValidationTests(unittest.TestCase):
    def testMaxSuccessValues(self):
        self.assertEquals([-11, -2, -1], Negative().successValues())
        self.assertEquals([-2, -1.1, -1], Negative(0.1).successValues())

    def testMaxFailureValues(self):
        self.assertEquals([0, 1], Negative().failureValues())
        self.assertEquals([0, 0.1], Negative(0.1).failureValues())


class RangeValidationTests(unittest.TestCase):
    def testRangeMaxLowerThanMin(self):
        try:
            Range(2, 1)
        except Exception, e:
            self.assertEquals('min > max, change the order of the arguments.', str(e))

    def testRangeSuccessValues(self):
        self.assertEquals([3, 4], Range(3, 4).successValues())
        self.assertEquals([3, 4, 5], Range(3, 5).successValues())
        self.assertEquals([56, 423, 790], Range(56, 790).successValues())
        self.assertEquals([56, 423, 791], Range(56, 791).successValues())
        self.assertEquals([3, 4], Range(3, 4, 0.1).successValues())
        self.assertEquals([3, 4, 5], Range(3, 5, 0.1).successValues())

    def testRangeFailureValues(self):
        self.assertEquals([-7, 2, 5, 14], Range(3, 4).failureValues())
        self.assertEquals([-7, 2, 6, 15], Range(3, 5).failureValues())
        self.assertEquals([46, 55, 791, 800], Range(56, 790).failureValues())
        self.assertEquals([46, 55, 792, 801], Range(56, 791).failureValues())
        self.assertEquals([2, 2.9, 4.1, 5], Range(3, 4, 0.1).failureValues())
        self.assertEquals([2, 2.9, 5.1, 6], Range(3, 5, 0.1).failureValues())


class InListValidationTests(unittest.TestCase):
    def testInListMinusThan2Elements(self):
        qa.assertExceptionMessage("If the list has minus of 2 elements, why don't make an exact test?",
                                  InList, [3])

    def testInListSuccessValues(self):
        self.assertEquals([1, 2], InList([1, 2]).successValues())
        self.assertEquals([1, 3, 4], InList([1, 2, 3, 4]).successValues())
        self.assertEquals([1, 3, 5], InList([1, 2, 3, 4, 5]).successValues())

    def testInListFailureValuesOfNumbers(self):
        self.assertEquals([2, 26], InList([11, 3, 16, 25]).failureValues())

    def testInListFailureValuesOfStrings(self):
        self.assertEquals([], InList(["A", "B"]).failureValues())

    def testInListFailureValuesOfObjects(self):
        class SomeClass(object): pass
        self.assertEquals([], InList([SomeClass(), SomeClass()]).failureValues())


class RegExprValidationTests(unittest.TestCase):
    def helper_success_values(self, regexpr, a_list):
        REGEXPR = regexpr
        self.assertEquals(a_list, RegExpr(REGEXPR).successValues())
        for s in RegExpr(REGEXPR).successValues():
            self.assertTrue(re.match(REGEXPR, s), str(s))
            self.assertTrue(re.search(REGEXPR, s), str(s))

    def helper_failure_values(self, regexpr, a_list):
        REGEXPR = regexpr
        self.assertEquals(a_list, RegExpr(REGEXPR).failureValues())
        for s in RegExpr(REGEXPR).failureValues():
            self.assertFalse(re.match(REGEXPR, s), str(s))
            self.assertFalse(re.search(REGEXPR, s), str(s))

    def test_SuccessValues_SimplestRegExpr(self):
        self.helper_success_values(r"a", ["a", "aa", "ab"])
        self.helper_success_values(r"z", ["z", "zz", "z{"])

    def test_FailureValues_SimplestRegExpr(self):
        self.helper_failure_values(r"a", ["b", "bb"])

    def test_SuccessValues_SimpleRegExpr(self):
        self.helper_success_values(r"abc", ["abc", "abcabc", "abcd"])

    def test_FailureValues_SimpleRegExpr(self):
        self.helper_failure_values(r"abc", ["bbc", "bbcbbc"])

    # TODO I stopped here
#    def test_SuccessValues_RegExpr_with_plus_greedy(self):
#        self.helper_success_values(r"abc+", ["abc", "abcabc", "abcd"])

#    def test_FailureValues_RegExpr_with_plus_greedy(self):
#        self.helper_failue_values(r"abc+", ["", "ab", "abab"])
#        
#    def test_SuccessValues_RegExpr_with_star_greedy(self):
#        self.helper_success_values(r"abc*", ["abc", "abcabc", "abcd"])
#        
#    def test_FailureValues_RegExpr_with_star_greedy(self):
#        self.helper_failue_values(r"abc*", ["", "ab", "abab"])
#        
#    def test_SuccessValues_RegExpr_with_interrogation_greedy(self):
#        self.helper_success_values(r"abc?", ["abc", "abcabc", "abcd"])
#        
#    def test_FailureValues_RegExpr_with_interrogation_greedy(self):
#        self.helper_failue_values(r"abc?", ["", "ab", "abab"])


#    def test_SuccessValues_RegExpr_with_plus_non_greedy(self):
#        self.helper_success_values(r"abc+", ["abc", "abcabc", "abcd"])
#        
#    def test_FailureValues_RegExpr_with_plus_non_greedy(self):
#        self.helper_failue_values(r"abc+", ["", "ab", "abab"])
#        
#    def test_SuccessValues_RegExpr_with_star_non_greedy(self):
#        self.helper_success_values(r"abc*", ["abc", "abcabc", "abcd"])
#        
#    def test_FailureValues_RegExpr_with_star_non_greedy(self):
#        self.helper_failue_values(r"abc*", ["", "ab", "abab"])
#        
#    def test_SuccessValues_RegExpr_with_interrogation_non_greedy(self):
#        self.helper_success_values(r"abc?", ["abc", "abcabc", "abcd"])
#        
#    def test_FailureValues_RegExpr_with_interrogation_non_greedy(self):
#        self.helper_failue_values(r"abc?", ["", "ab", "abab"])


#    def testAssertValidation_of_SimpleRegExpr(self):
#        REG_EXPR = r"abc"
#        def has_some_pattern(self, string):
#            return re.match(REG_EXPR, string)
#        qa.assertDontRaiseAnException(qa.assertValidation, has_some_pattern, RegExpr(EXPR_REG))


#        (<)?(\w+@\w+(?:\.\w+)+)(?(1)>)

#         nao greedy
#         "a+?"
#         "a*?"
#         "a??"

#        good value
#        strings positivas?
#        string negativas?



class QAssertionsTests(unittest.TestCase):
    def testExecuteMethodWithoutArguments(self):
        def some_method():
            return 13
        spy = qa.executeMethod(some_method)
        self.assertEquals(13, spy)

    def testExecuteMethodWithOneArgument(self):
        def some_method(value1):
            return value1
        spy = qa.executeMethod(some_method, 5)
        self.assertEquals(5, spy)

    def testExecuteMethodWithArguments(self):
        def some_method(value1, value2):
            return value1 + value2
        spy = qa.executeMethod(some_method, 5, 6)
        self.assertEquals(11, spy)


class AssertValidationTests(unittest.TestCase):
    def test_MinimumValue_for_valid_method_with_one_argument(self):
        def some_method(value1):
            if value1 < 7: raise Exception('ops')
        qa.assertDontRaiseAnException(qa.assertValidation, some_method, Min(7))

    def test_MinimumValue_for_lower_minimum_method_with_one_argument(self):
        def some_method(value1):
            if value1 < 6: raise Exception()
        qa.assertExceptionMessage("Unexpected success for the combination of arguments:\n> 6",
                                  qa.assertValidation, some_method, Min(7))

        def another_method(value1):
            if value1 < 0: raise Exception()
        qa.assertExceptionMessage("Unexpected success for the combination of arguments:\n> 6",
                                  qa.assertValidation, another_method, Min(7))

    def test_MinimumValue_for_greater_minimum_method_with_one_argument(self):
        def some_method(value1):
            if value1 <= 7: raise Exception("ops")
        qa.assertExceptionMessage("Unexpected failure for the combination of arguments:\n> 7 - ops",
                                  qa.assertValidation, some_method, Min(7))

        def another_method(value1):
            if value1 <= 8: raise Exception("ops")
        qa.assertExceptionMessage("This method appears to have at least a big validation error, try to fix it:\nUnexpected failure for the combination of arguments:\n> 8 - ops",
                                  qa.assertValidation, another_method, Min(7))


    def test_MinimumValue_for_symbol_error_method_with_one_argument(self):
        def some_method(value1):
            if value1 > 7: raise Exception()
        qa.assertExceptionMessage("This method appears to have at least a big validation error, try to fix it:\nUnexpected failure for the combination of arguments:\n> 8 - ",
                                  qa.assertValidation, some_method, Min(7))

        def another_method(value1):
            if value1 >= 7: raise Exception()
        qa.assertExceptionMessage("This method appears to have at least a big validation error, try to fix it:\nUnexpected failure for the combination of arguments:\n> 8 - ",
                                  qa.assertValidation, another_method, Min(7))



    def test_MaximumValue_for_valid_method_with_one_argument(self):
        def some_method(value1):
            if value1 > 7: raise Exception('ops')
        qa.assertDontRaiseAnException(qa.assertValidation, some_method, Max(7))

    def test_RangeValue_for_valid_method_with_one_argument(self):
        def some_method(value1):
            if value1 < 3: raise Exception('ops')
            if value1 > 4: raise Exception('ops')
        qa.assertDontRaiseAnException(qa.assertValidation, some_method, Range(3, 4))

    def test_InListValue_for_valid_method_with_one_argument(self):
        def some_method(value1):
            if value1 != 3 and value1 != 4: raise Exception('ops')
        qa.assertDontRaiseAnException(qa.assertValidation, some_method, InList([3, 4]))


class AssertListIsSortedTests(unittest.TestCase):
    def test_CaseOfSuccess(self):
        qa.assertListIsSorted([1, 2, 3])

    def test_CaseOfSuccess_of_custom_list(self):
        qa.assertListIsSorted([3, 2, 1], reverse=True)
        qa.assertListIsSorted(['D', 'b', 'c'], key=lambda s: s.upper)

    def test_CaseOfFailure(self):
        qa.assertExceptionMessage("List is not sorted.",
                                  qa.assertListIsSorted, [3, 2, 1])

    def test_CaseOfFailure_of_custom_list(self):
        qa.assertExceptionMessage("List is not sorted.",
                                  qa.assertListIsSorted, ['D', 'b', 'E'], key=lambda s: s.upper)


class AssertListIsNotSortedTests(unittest.TestCase):
    def test_CaseOfSuccess(self):
        qa.assertListIsNotSorted([3, 2, 1])

    def test_CaseOfSuccess_of_custom_list(self):
        qa.assertListIsNotSorted([1, 2, 3], reverse=True)
        qa.assertListIsNotSorted(['D', 'b', 'E'], key=lambda s: s.upper)

    def test_CaseOfFailure(self):
        qa.assertExceptionMessage("List is sorted.",
                                  qa.assertListIsNotSorted, [1, 2, 3])

    def test_CaseOfFailure_of_custom_list(self):
        qa.assertExceptionMessage("List is sorted.",
                                  qa.assertListIsNotSorted, ['D', 'b', 'c'], key=lambda s: s.upper)


class AssertPerformanceTests(unittest.TestCase):
    def testAssertPerformance_BuggedMethod(self):
        def some_bugged_method():
            raise Exception("ops")
        qa.assertExceptionMessage("This method is bugged, It impossible to measure the performance: ops",
                                  qa.assertPerformance, 0.1, some_bugged_method)

    def testAssertPerformance_FastMethod(self):
        def some_fast_method():
            return 13
        qa.assertPerformance(1, some_fast_method)

    def testAssertPerformance_SlowMethod(self):
        def some_slow_method():
            time.sleep(0.1)
        qa.assertPerformance(0.2, some_slow_method)

    def testAssertPerformance_SlowMethod_ErrorSituation(self):
        def some_slow_method():
            time.sleep(0.4)
        qa.assertExceptionMessage("This method is too slow: [...]",
                                  qa.assertPerformance, 0.2, some_slow_method)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
