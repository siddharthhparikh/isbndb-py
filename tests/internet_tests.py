#So in a fun departure from the rest of the basic naming scheme going on
#with these tests, I dont have params tests in here, even tho they are in the
#internet module. you know. fun stuff.

import sys
if __name__=='__main__':
    sys.path.insert(0,'..')

if sys.version_info[0] == 2 and sys.version_info[1] <= 4:
    try:
        import cElementTree as ElementTree
    except:
        from elementtree import ElementTree
elif sys.version_info[0] == 2 and sys.version_info[1] >= 5:
    from xml.etree import ElementTree

import unittest
from isbndb.cursors import PageCursor, PyPageCursor, BookCursor, PyBookCursor
from isbndb.internet import params, fetch
from isbndb.keys import getKey, loadKeys, Key
from isbndb import IsbndbSearch

#set up keys...
loadKeys()

class ParamSetupMixin(object):
    def setUp(self):
        self.p = params()
        self.key = getKey()
        #set up params

        self.p.searchIndex = 'full'
        self.p.results = ['texts','details','subjects']
        self.p.searchValue = 'sex'
        self.p.key = self.key

class TestFetch(unittest.TestCase,ParamSetupMixin):
    def setUp(self):
        print "\nTestFetch:",
        ParamSetupMixin.setUp(self)


    def test_fetchReturnType(self):
        print "Testing return type is an Element and BookList...",
        x = fetch(self.p)
        self.assert_(ElementTree.iselement(x),"FAILED (fetch didnt get elem)")
        self.assert_(x.tag == 'BookList', "FAILED (fetched elem not BookList)")
        print "OK"


    def test_fetchRaisesError(self):
        print "Testing that bad key gives error..",
        x = Key('foobar',force_=True)
        x.active = True
        self.p.key = x
        self.assertRaises(Exception, fetch, self.p)
        print "OK"

class TestIsbndbSearch(unittest.TestCase, ParamSetupMixin):
    def setUp(self):
        print "\nTestIsbndbSearch:",
        ParamSetupMixin.setUp(self)

    def test_searchWorksWithParams(self):
        print "Testing that a params obj works with search...",
        print "with key...",
        x = IsbndbSearch(p=self.p)
        self.assert_(isinstance(x,PyBookCursor), "FAILED (didnt search)")
        print "without key...",
        p = params()
        p.searchIndex = 'full'
        p.searchValue = 'sex'

        x = IsbndbSearch(p=p)
        self.assert_(isinstance(x,PyBookCursor), "FAILED (didnt assign key)")
        print "OK"

    def test_searchEmptyRaisesError(self):
        print "Testing that no args raises error...",
        self.assertRaises(Exception, IsbndbSearch)
        print "OK"

    def test_searchWorks(self):
        print "Testing that search works...",
        p = self.p
        x = IsbndbSearch(searchValue=p.searchValue, searchIndex=p.searchIndex,
                         results = p.results)
        self.assert_(isinstance(x,PyBookCursor),"FAILED (search broke)")
        print "OK"

    def test_settingCursorWorks(self):
        print "Testing that setting a cursor works right...",
        x = IsbndbSearch(p=self.p, cursor = PyPageCursor)
        self.assert_(isinstance(x, PyPageCursor),"FAILED (didnt change cursor)")
        print "OK"

def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(TestFetch,'test'))
    s.addTest(unittest.makeSuite(TestIsbndbSearch,'test'))
    return s

if __name__ == '__main__':
    unittest.main()
