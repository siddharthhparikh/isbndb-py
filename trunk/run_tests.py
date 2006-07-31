#!/usr/bin/python 
import sys
sys.path.insert(0,'./tests/')

import unittest
import helpers_test,cursors_test,book_test,setup_xml,setup_keys,params_test,key_test
import internet_tests


#setup test input files:
setup_xml.main()
setup_keys.main()
#add the tests
s=unittest.TestSuite()
s.addTest(helpers_test.suite())
s.addTest(cursors_test.suite())
s.addTest(book_test.suite())
s.addTest(key_test.suite())
s.addTest(params_test.suite())
s.addTest(internet_tests.suite())

def suite():
    return s
#run it
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1).run(s)


