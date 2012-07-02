import unittest
import pymock
import FizzBuzz
"""
Q5. Write the psuedocode for the test_repport method, such that it uses PyMock
    mock objects to test the report method of FizzBuzz. [5 pts]
"""
class TestFizzBuzzMocked(pymock.PyMockTestCase):
        
    def setUp(self):
        super(TestFizzBuzzMocked, self).setUp()
        self.fb = FizzBuzz.FizzBuzz()
        print "setUp TestFizzBuzzMocked"

    def tearDown(self):
        super(TestFizzBuzzMocked, self).tearDown()
        self.fb = None

    def test_report(self):
        """
        Verify main success scenario when the FizzBuzz class generates a correct report
        """
        
        #Create the mocks
        opener_mock = self.mock()        
        file_mock = self.mock()
        
        #Set expectations
        expected_file_path = './fizzbuzz_report.txt'
        expected_mode = 'w'
        self.expectAndReturn(opener_mock(expected_file_path, expected_mode), file_mock)              
        file_mock.write('0 fizz buzz \n')
        file_mock.write('3 fizz \n')
        file_mock.write('5 buzz \n')
        file_mock.write('6 fizz \n')
        file_mock.write('9 fizz \n')
        file_mock.close()        
        
        #Replay
        self.replay()
        
        #Call the API
        self.fb.report(range(10), opener_mock)
        
        #Verify
        self.verify()


    def test_report_for_empty_list(self):
        """
        Verify scenario when there is nothing to write in the report file
        """
        
        #Create the mocks
        opener_mock = self.mock()        
        file_mock = self.mock()
        
        #Set expectations
        expected_file_path = './fizzbuzz_report.txt'
        expected_mode = 'w'
        self.expectAndReturn(opener_mock(expected_file_path, expected_mode), file_mock)              
        file_mock.close()        
        
        #Replay
        self.replay()
        
        #Call the API
        self.fb.report([], opener_mock)
        
        #Verify
        self.verify()
        
        
    def test_report_when_open_raises_ex(self):
        """
        Verify scenario when the opener cannot open the report file and an IOError is raised
        """
        
        #Create the mocks
        opener_mock = self.mock()                
        
        #Set expectations
        expected_file_path = './fizzbuzz_report.txt'
        expected_mode = 'w'
        self.expectAndRaise(opener_mock(expected_file_path, expected_mode), IOError("No such file or directory: '%s'" % expected_file_path))
        
        #Replay
        self.replay()
        
        try:
            self.fb.report([], opener_mock)
        except IOError:
            pass
        except Exception, e:
            self.fail('Unknown exception %r was expecting IOError' % e)
        else:
            self.fail('Exception IOError was expected, but was not thrown')
            
        #Verify
        self.verify()
        
        
    def test_report_when_write_raise_ex(self):
        """
        Verify scenario when a write to the file causes an Exception to be raised
        """
        
        #Create the mocks
        opener_mock = self.mock()                
        file_mock = self.mock()
        
        #Set expectations
        expected_file_path = './fizzbuzz_report.txt'
        expected_mode = 'w'
        self.expectAndReturn(opener_mock(expected_file_path, expected_mode), file_mock)
        error_msg = 'Could not write to file'
        self.expectAndRaise(file_mock.write('0 fizz buzz \n'), IOError(error_msg))
        file_mock.close()
        
        #Replay
        self.replay()
        
        #Call the API                
        try:
            self.fb.report(range(10), opener_mock)
        except IOError, ioe:
            expected_msg = 'Could not write to file'
            if not ioe.message == expected_msg:
                self.fail("Incorrect Exception message, was expected '%s' but was '%s' " % (expected_msg, ioe.message))
        except Exception, e:
            self.fail('Unknown exception %r was expecting IOError' % e)
        else:
            self.fail('Exception IOError was expected, but was not thrown')
        
        #Verify
        self.verify()
            
            

if __name__ == "__main__":
    unittest.main()
