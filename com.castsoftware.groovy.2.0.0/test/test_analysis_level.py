import os
import unittest
from cast.analysers.test import UATestAnalysis

from cast.analysers import log


class Test(unittest.TestCase):
    
    def testName(self):
        print (os.getcwd())
        analysis = UATestAnalysis('groovy')
        analysis.add_selection("groovysample")
        analysis.set_verbose(True)
        analysis.run()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()