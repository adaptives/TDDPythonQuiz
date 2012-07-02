import unittest
import pymock
import FizzBuzz
"""
Q3. What will be printed when we execute 'python FizzBuzzStubbed.py' ? [3 pts]

Ans:
setUpClass FizzBuzzStubbed
setup
test_report #from method test_report
teardown
setup
test_report #from method test_report_for_empty_list
teardown
tearDownClass

Please note that the print statements have been commented out in the code below 
and a few additional methods have also been added. If you want to see the original
code please go up in the commit history and see the first commit. 



Q4. Implement MyStub class so that you can send it as a fake object to the
    report method of FizzBuzz object from a test case. [3 pts]

Ans:
Please see the implemented class below. I have created tests for:
main success scenario
scenario when there is nothing to print
scenario when the opener results in an IOError
scenario when a write to the file results in an IOError
"""


class Opener(object):
    
    def __init__(self):
        self.path = ""
        self.mode = ""
        
    def open(self, path, mode):
        self.path = pathself.mode = mode
        
    def gen_opener(self, file_stub):
        def open(path, mode):
            self.path = path
            self.mode = mode
            return file_stub
        return open
    
    def gen_opener_which_raises_ex(self, file_stub):
        def open(path, mode):
            raise IOError("No such file or directory: '%s'" % path)
        return open
    
    def get_path(self):
        return self.path
    
    def get_mode(self):
        return self.mode
        
        
class MyStub(object):
    
    def __init__(self, raise_ex_on_write=False):
        self.lines_written = []
        self.closed = False
        self.raise_ex_on_write = raise_ex_on_write
    
    def write(self, line):
        if self.raise_ex_on_write:
            raise IOError('Could not write to file')
        else:
            self.lines_written.append(line)
        
    def close(self):
        self.closed = True
    
    def is_line_written(self, line):
        return line in self.lines_written
    
    def num_lines_written(self):
        return len(self.lines_written)

    def is_closed(self):
        return self.closed
    
    def __str__(self):
        """
        Will allow us to print the state of this object for debugging purposes
        """
        buff = ""
        buff += "".join(self.lines_written)
        buff += "\n"
        buff += "closed %s" % self.closed
        return buff

    
class TestFizzBuzzStubbed(unittest.TestCase):
        
    @classmethod
    def setUpClass(cls):
        #print "setUpClass FizzBuzzStubbed"
        pass
        
    def setUp(self):
        super(TestFizzBuzzStubbed, self).setUp()
        self.fb = FizzBuzz.FizzBuzz()
        #print "setup"

    @classmethod
    def tearDownClass(cls):
        #print "tearDownClass"
        pass
        
    def tearDown(self):
        super(TestFizzBuzzStubbed, self).tearDown()
        self.fb = None
        #print "teardown"

    def test_report(self):
        """
        Verify main success scenario when the FizzBuzz class generates a correct report
        """
        
        #print "test_report"
        file_stub = MyStub()
        opener = Opener()
        open_stub = opener.gen_opener(file_stub)
        self.fb.report(range(10), open_stub)
        
        self.assertTrue(opener.get_path(), 'c:/temp/fizzbuzz_report.txt')
        self.assertTrue(opener.get_mode(), 'w')
        
        self.assertEquals(file_stub.num_lines_written(), 5)
        self.assertTrue(file_stub.is_line_written('0 fizz buzz \n'))
        self.assertTrue(file_stub.is_line_written('3 fizz \n'))
        self.assertTrue(file_stub.is_line_written('5 buzz \n'))
        self.assertTrue(file_stub.is_line_written('6 fizz \n'))
        self.assertTrue(file_stub.is_line_written('9 fizz \n'))
        self.assertTrue(file_stub.is_closed())

    
    def test_report_for_empty_list(self):
        """
        Verify scenario when there is nothing to write in the report file
        """
        
        #print "test_report"
        file_stub = MyStub()
        opener = Opener()
        open_stub = opener.gen_opener(file_stub)
        self.fb.report([], open_stub)
        
        self.assertTrue(opener.get_path(), 'c:/temp/fizzbuzz_report.txt')
        self.assertTrue(opener.get_mode(), 'w')
        
        self.assertEquals(file_stub.num_lines_written(), 0)
        self.assertTrue(file_stub.is_closed())
    
    
    def test_report_when_file_cannot_be_opened(self):
        """
        Verify scenario when the opener cannot open the report file and an IOError is raised
        """
        
        file_stub = MyStub()
        opener = Opener()
        open_stub = opener.gen_opener_which_raises_ex(file_stub)
        
        try:
            self.fb.report([], open_stub)
        except IOError:
            pass
        except Exception, e:
            self.fail('Unknown exception %r was expecting IOError' % e)
        else:
            self.fail('Exception IOError was expected, but was not thrown')
            
    
    def test_report_when_write_raise_ex(self):
        """
        Verify scenario when a write to the file causes an Exception to be raised
        """
        
        file_stub = MyStub(True)
        opener = Opener()
        open_stub = opener.gen_opener(file_stub)
        
        try:
            self.fb.report(range(10), open_stub)
        except IOError, ioe:
            expected_msg = 'Could not write to file'
            if not ioe.message == expected_msg:
                self.fail("Incorrect Exception message, was expected '%s' but was '%s' " % (expected_msg, ioe.message))
        except Exception, e:
            self.fail('Unknown exception %r was expecting IOError' % e)
        else:
            self.fail('Exception IOError was expected, but was not thrown')
        
        self.assertTrue(file_stub.is_closed())
        
        
if __name__ == "__main__":
    unittest.main()
