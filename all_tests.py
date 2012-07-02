import unittest
import TestFizzBuzzStubbed
import TestFizzBuzzMocked

suite = unittest.TestLoader().loadTestsFromTestCase(TestFizzBuzzStubbed.TestFizzBuzzStubbed)
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFizzBuzzMocked.TestFizzBuzzMocked))

unittest.TextTestRunner(verbosity=2).run(suite)