'''
Example of usage: qassertions_simple_example.py
A more complex example: qassertions_example.py

This module has additional assertions to facilitate writing good automated tests. In particular, assertValidation
has an special behavior that use QA recommendations to create extra test cases automatically.

assertDontRaiseAnException
assertExceptionMessage
assertListIsSorted
assertListIsNotSorted
assertValidation (Min, Max, Positive, Negative, Range, InList, NotInList, Blank, NonBlank)
assertPerformance
'''

import re
import threading2
import time


failureException = AssertionError

# Exceptions

def assertDontRaiseAnException(method, *args, **kwargs):
    '''
    Assert that the method is executed without raise an exception. 
    This method is useful to document the test in an elegant way and facilitate the comprehension of errors in the report . 
    '''
    try:
        executeMethod(method, *args, **kwargs)
    except Exception as e:
        raise failureException("It was not expect an exception, but it get a %s: %s" % (e.__class__.__name__, str(e)))

def assertExceptionMessage(exception_message, method, *args, **kwargs):
    '''
    Assert that a exception is raised and has an specific message. 
    '''
    try:
        executeMethod(method, *args, **kwargs)
    except Exception as e:
        if not re.match(exception_message.replace("[...]", ".*"), str(e)):
            raise failureException("It was expected an exception with message '%s', but receive '%s'" % (exception_message, str(e)))
    else:
        raise failureException("It was expected an exception.")

# Validation

def executeMethod(method, *args, **kwargs):
    return method(*args, **kwargs)

class ValidationTestResult(object):
    '''
    Result object (used as collect parameter) that store the log of validation tests
    '''

    def __init__(self):
        self.unexpectFailure = []
        self.unexpectSuccess = []

    def addUnexpectedFailure(self, msg, values):
        self.unexpectFailure.append((values, msg))

    def addUnexpectedSuccess(self, values):
        self.unexpectSuccess.append(values)

    def __str__(self):
        result = ''
        if len(self.unexpectSuccess) > 0:
            result = result + "Unexpected success for the combination of arguments:"
            for success in self.unexpectSuccess:
                values = ', '.join(str(v) for v in success)
                result = result + '\n> %s' % (values)
        if len(self.unexpectFailure) > 0:
            if len(self.unexpectSuccess) > 0:
                result = result + "\n"
            result = result + "Unexpected failure for the combination of arguments:"
            for failure in self.unexpectFailure:
                values = ', '.join(str(v) for v in failure[0])
                msg = failure[1]
                result = result + '\n> %s - %s' % (values, msg)
        return result

    def hasFailure(self):
        return len(self.unexpectFailure) > 0 or len(self.unexpectSuccess) > 0


class ValidationTest(object):
    '''
    Abstract class that is used to identify a validation test to a specific argument
    '''

    def goodValue(self):
        '''
        Not special case of success
        '''
        pass

    def successValues(self):
        '''
        Cases of success, that don't expect an exception
        '''
        pass

    def failureValues(self):
        '''
        Cases of failure, that expect an exception
        '''
        pass


class Min(ValidationTest):
    '''
    Properties:
    min = inclusive
    precision = default 1, the value that will be added to min to create failure cases
    
    Make the following tests: 
    - Cases of success: min, min+precision, min+10*precision
    - Cases of failure: min-precision, min-10*precision
    '''

    def __init__(self, a_min, precision=1):
        self.min = a_min
        self.precision = precision

    def goodValue(self):
        return self.min + self.precision

    def successValues(self):
#        if isinstance(self.value, (str, list, dict, tuple)):
#          return len(self.value) >= self.requiredValue
        return [self.min,
                self.goodValue(),
                self.min + (10 * self.precision)]

    def failureValues(self):
        return [self.min - (10 * self.precision),
                self.min - self.precision]


class Max(ValidationTest):
    '''
    Properties:
    max = inclusive
    precision = default 1, the value that will be added to max to create failure cases
    
    Make the following tests: 
    - Cases of success: max, max-precision, max-10*precision
    - Cases of failure: max+precision, max+10*precision
    '''

    def __init__(self, a_max, precision=1):
        self.max = a_max
        self.precision = precision

    def goodValue(self):
        return self.max - self.precision

    def successValues(self):
        return [self.max - (10 * self.precision),
                self.goodValue(),
                self.max]

    def failureValues(self):
        return [self.max + self.precision,
                self.max + (10 * self.precision)]


class Positive(Min):
    '''
    Properties:
    precision = default 1, the value that will be added to max to create failure cases
    
    Similar to Min(1) but with the following difference:
    - Cases of failure: -precision, 0
    '''
    def __init__(self, precision=1):
        super(Positive, self).__init__(1, precision)

    def failureValues(self):
        return [-self.precision, 0]


class Negative(Max):
    '''
    Properties:
    precision = default 1, the value that will be added to max to create failure cases
    
    Similar to Max(-1) but with the following difference: 
    - Cases of failure: 0, precision
    '''
    def __init__(self, precision=1):
        super(Negative, self).__init__(-1, precision)

    def failureValues(self):
        return [0, self.precision]


class Range(ValidationTest):
    '''
    Properties:
    min = inclusive
    max = inclusive
    precision = default 1, the value that will be added to min and max to create failure cases

    Make the following tests: 
    - Cases of success: min, max, (max-min)/2
    - Cases of failure: min-precision, max+precision, min-10*precision, max+10*precision
    '''

    def __init__(self, a_min, a_max, precision=1):
        if (min > max): raise Exception('min > max, change the order of the arguments.')
        self.min = a_min
        self.max = a_max
        self.precision = precision

    def goodValue(self):
        return self.min + ((self.max - self.min) / 2)

    def successValues(self):
        if (self.max - self.min) < 2:
            return [self.min, self.max]
        return [self.min,
                self.goodValue(),
                self.max]

    def failureValues(self):
        return [self.min - (10 * self.precision),
                self.min - self.precision,
                self.max + self.precision,
                self.max + (10 * self.precision)]


class InList(ValidationTest):
    '''
    Properties:
    list = list ([]) of valid values for some property (len > 1) 
    
    Make the following tests: 
    - Cases of success: list[first], list[middle], list[last]
    - Cases of failure: [list[first] - 1, list[last] + 2] if numbers, else []
    '''

    def __init__(self, a_list):
        if(len(a_list) < 2): raise Exception("If the list has minus of 2 elements, why don't make an exact test?")
        self.list = a_list

    def goodValue(self):
        return self.list[len(self.list) / 2]

    def successValues(self):
        if len(self.list) < 4:
            return self.list
        return [self.list[0], self.goodValue(), self.list[len(self.list) - 1]]


    def failureValues(self):
        try:
            self.list.sort()
            return [self.list[0] - 1, self.list[len(self.list) - 1] + 1]
        except:
            return []


class NotInList(InList):
    '''
    Properties:
    list = list ([]) of valid values for some property (len > 1) 
    
    Make the following tests: 
    - Cases of success: [list[first] - 1, list[last] + 2] if numbers, else []
    - Cases of failure: list[first], list[middle], list[last]
    '''

    def goodValue(self):
        values = self.successValues()
        try:
            if (len(values) > 0):
                return values[0]
        except Exception as e:
            pass
        raise Exception("NotInList just work for numbers")

    def successValues(self):
        return InList.failureValues(self)

    def failureValues(self):
        return InList.successValues(self)


class Blank(ValidationTest):
    '''
    Properties:
    
    Make the following tests: 
    - Cases of success: '', ' ', '\t' 
    - Cases of failure: None
    '''

    def goodValue(self):
        return '\t'

    def successValues(self):
        return ['', ' ', self.goodValue()]

    def failureValues(self):
        '''
        You can overwrite this method if these values are not good
        '''
        return [None]


class NonBlank(ValidationTest):
    '''
    Properties:
    
    Make the following tests: 
    - Cases of success: []
    - Cases of failure: None, '', ' '
    '''

    def goodValue(self):
        '''
        You can overwrite/rewrite this method if these values are not good
        '''
        return 'a'

    def successValues(self):
        '''
        You can overwrite/rewrite this method if these values are not good
        '''
        return ['a', 'abc']

    def failureValues(self):
        return ['\t', '', ' ']


class RegExpr(ValidationTest):
    '''
    Properties:
    regexpr = regular expression
    
    Make the following tests: 
    - Cases of success: []
    - Cases of failure: None, '', ' '
    '''

    def __init__(self, regexpr):
        self.regexpr = regexpr

    def goodValue(self):
        '''
        You can overwrite/rewrite this method if these values are not good
        '''
        return 'a'

    def successValues(self):
        '''
        You can overwrite/rewrite this method if these values are not good
        '''
        self.regexpr[:].replace("+", "")
        lastchar = self.regexpr[len(self.regexpr) - 1]
        newchar = chr(ord(lastchar) + 1)
        return [self.regexpr, 2 * self.regexpr, self.regexpr + newchar]

    def failureValues(self):
        newchar = chr(ord(self.regexpr[0]) + 1)
        newstr = newchar + self.regexpr[1:]
        return [newstr, 2 * newstr]


def verifySuccess(resultCollectParameter, method, *args):
    try:
        executeMethod(method, *args)
    except Exception as e:
        resultCollectParameter.addUnexpectedFailure(str(e), args)


def verifyFailure(resultCollectParameter, method, *args):
    try:
        executeMethod(method, *args)
        resultCollectParameter.addUnexpectedSuccess(args)
    except Exception as e: # TODO Exception base exceptionClass=Exception, identificar erro de falha normal
        pass
#        print(str(e))


def getGoodValues(args):
    goodValues = []
    for arg in args:
        if isinstance(arg, ValidationTest):
            goodValues.append(arg.goodValue())
        else:
            goodValues.append(arg)
    return goodValues


def assertValidation(method, *args):
    '''
    Assert validation of Min, Max, Range, InList, Blank, NonBlank and others constraints. 
    '''
    result = ValidationTestResult()
    goodValues = getGoodValues(args)
    verifySuccess(result, method, *tuple(goodValues))
    if result.hasFailure():
        raise failureException('This method appears to have at least a big validation error, try to fix it:\n%s' % str(result))

    for index, arg in enumerate(args):
        if isinstance(arg, ValidationTest):
            values = goodValues[:]
            for v in arg.successValues():
                values[index] = v
                verifySuccess(result, method, *tuple(values))
            for v in arg.failureValues():
                values[index] = v
                verifyFailure(result, method, *tuple(values))

    if result.hasFailure():
        raise failureException(str(result))

# List

def _listIsSorted(a_list, a_cmp=None, key=None, reverse=False):
    clone = a_list[:]
    clone.sort(cmp=a_cmp, key=key, reverse=reverse)
    return clone == a_list


def assertListIsSorted(a_list, a_cmp=None, key=None, reverse=False):
    sorted_list = sorted(a_list, cmp=a_cmp, key=key, reverse=reverse)
    if(a_list != sorted_list):
        raise failureException("List is not sorted. Expected list: %s" % sorted_list)


def assertListIsNotSorted(a_list, a_cmp=None, key=None, reverse=False):
    sorted_list = sorted(a_list, cmp=a_cmp, key=key, reverse=reverse)
    if(a_list == sorted_list):
        raise failureException("List is sorted (%s)." % sorted_list)


# Performance

def assertPerformance(timeout, method, *args):
    '''
    timeout in milliseconds
    
    Use this assertion in a specialized suite of performance tests.
    Don't use this assertion inside of a unit test suite, unless the method is too fast.
    This method don't take care the speed of the CPU, so try to set a big timeout, considering a bad hardware to avoid
    intermitent tests.
    TODO: Use PSI (http://www.psychofx.com/psi) to get the CPU speed to be possible to make more precise tests.
    '''
    startTime = time.clock()
    thread = None
    try:
        thread = threading2.KThread(target=method,
                                    args=args,
                                    name='Thread-AssertPerformance-' + str(method))
        thread.start()
        thread.joinWithTimeout(timeout)
        if thread.isExpired():
            endTime = time.clock()
            durationTime = endTime - startTime
            raise failureException("This method is too slow: %s" % str(durationTime))
    except failureException as e:
        raise e
    except Exception as e:
        raise failureException("This method is bugged, It impossible to measure the performance: %s" % str(e))
    finally:
        endTime = time.clock()
        durationTime = endTime - startTime

