#!/usr/bin/env python

import unittest
from isbndb.helpers import *

class LimitListTester(unittest.TestCase):
    def setUp(self):
        print "\nLimitListTester:",
        tv = ('foo','bar','baz','things','stuff','yellow','red','green',\
              'blue','purple','aces','web','books','isbn','stuff')

        self.l = LimitList(ok=tv)
        self.tv = tv

    def test_makes_list(self):
        print "Testing list is constructed no args...",
        self.assert_(isinstance(self.l, LimitList),'FAILED')
        print "OK"

    def test_appends_good(self):
        print "Testing append, ok vals...",
        self.l.append('things')
        self.l.append('stuff')
        self.assertEqual(self.l,['things','stuff'],"FAILED")
        print "OK"

    def test_appends_bad(self):
        print "Testing append, bad vals raises ValueError...",
        self.assertRaises(ValueError, self.l.append, 'mom')
        print "OK"

    def test_extends_list(self):
        print "Testing extends...",
        self.l.extend(['foo','bar'])
        self.assertEqual(self.l,['foo','bar'],'FAILED')
        print "OK"

    def test_constructor(self):
        print "Testing constructor with list..",
        n = LimitList(['foo','bar','yellow'],self.tv)
        self.assert_(isinstance(n,LimitList),"FAILED")
        print "OK"
        print "Testing constructor with LimitList...",
        n = LimitList(self.l,self.tv)
        self.assertEqual(n, self.l,"FAILED, not equal")
        self.failIf(n is self.l, "FAILED, same object")
        print "OK"

    def test_add(self):
        print "Testing adds good...",
        self.l += ['red','aces']
        n = LimitList(['foo','bar'],self.tv)
        self.l += n
        print "OK"

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LimitListTester, 'test'))
    return suite

if __name__=='__main__':
    unittest.main()
