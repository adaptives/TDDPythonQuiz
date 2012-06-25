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
        pass















        


if __name__ == "__main__":
    unittest.main()
