import settings

"""
Q1. Why is the report method untestable ? [2 pts]

Ans: The report method is untestable because it creates it's collaborators
directly. When a function creates it's collaborators directly, we cannot
ensure that the environment they require will always be present when the 
unit test is executed. For example, in this case, the 'report' function
invokes the function 'open' to get a handle to the hardcodes file 
'c:/temp/fizzbuzz_report.txt'. We cannot always ensure that this file 
or even this directory will be present on the file system. Especially in 
this case you will have noticed that 'c:/temp/fizzbuzz_report.txt' is a 
Windows specific directory, so this tedt cannot be run on a Unix system.

For a function to be testable, it should always accept its collaborators
from elsewhere (function arguments, factories, etc). This way we can 
give the function mock/stub collaborators when the function is being 
run in test mode and give it real collaborators when it is being run in
production mode.


Q2. How will you change the api of the report method to make it more testable ? [2 pts]

Ans: There are two ways we can change the function signature to make it more testable
1. Give it an opener which will yeild the file handle
   def report(self, numbers, opener):
2. Give it the file handle itself
   def report(self, numbers, file_handle):

"""

""" The original class
class FizzBuzz(object):
    def report(self, numbers):

        report_file = open('c:/temp/fizzbuzz_report.txt', 'w')

        for number in numbers:
            msg = str(number) + " "
            fizzbuzz_found = False
            if number % 3 == 0:
                msg += "fizz "
                fizzbuzz_found = True
            if number % 5 == 0:
                msg += "buzz "
                fizzbuzz_found = True

            if fizzbuzz_found:
                report_file.write(msg + "\n")

        report_file.close()
"""
        
class FizzBuzz(object):
    """
    New and testable
    """
    
    def report(self, numbers, opener=open):

        #report_file = opener('c:/temp/fizzbuzz_report.txt', 'w')
        report_file = None
        try:
            report_file = opener(settings.report_file_name, 'w')
            for number in numbers:
                msg = str(number) + " "
                fizzbuzz_found = False
                if number % 3 == 0:
                    msg += "fizz "
                    fizzbuzz_found = True
                if number % 5 == 0:
                    msg += "buzz "
                    fizzbuzz_found = True
    
                if fizzbuzz_found:
                    report_file.write(msg + "\n")
                    
        finally:
            if not report_file == None:
                report_file.close()

if "__main__" == __name__:
    fb = FizzBuzz()
    fb.report(range(10))

            
