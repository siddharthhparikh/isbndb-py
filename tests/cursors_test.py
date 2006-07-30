if __name__=='__main__':
    import sys
    sys.path.insert(0,'..')
    prependdir = ''
else:
    prependdir = 'tests/'
    
from isbndb import PageCursor, PyPageCursor, BookCursor, PyBookCursor
from isbndb.book import IsbndbBook
import unittest,urllib
try:
    import cElementTree as ElementTree
except:
    from elementtree import ElementTree

class fauxParams(object):
    def __init__(self):
        self.pageNum = 1
        
def fauxFetch(params):
    """This is a simple fetch for testing cursor functionality"""
    f = open(prependdir+'xml/%s.xml'%params.pageNum)
    a = f.read()
    r =  ElementTree.fromstring(unicode(a,'ascii',errors='ignore'))
    r = r.find('BookList')
    if ElementTree.iselement(r):
        return r
    else:
        raise Exception, 'not getting a page...'
        
class cursorTestsMixin(object):
    def setUp(self):
        a = fauxParams()
        self.cursor = self.cursor_type(a,fauxFetch(a))
        self.cursor.get = fauxFetch
    
    def validateSlice(self,li):
        for x in li:
            if not self.validateResult(x):
                return False
        return True
        
    def test_numbers(self):
        print "Test that everything parses right...",
        self.assertEqual(self.cursor.totalBooks, 8408, "FAILED (totalBooks)")
        self.assertEqual(self.cursor.numPages, 841, "FAILED (numPages)")
        print "OK"

    def test_listfuncs(self):
        print "Testing the cursor works as a list...",
        a = self.cursor[self.start_index]
        self.assert_(self.validateResult(a),
            "FAILED (invalid result)\n%s"%type(a))
        print "OK"

    def test_slicefuncs(self):
        print "Testing the cursor works with slices...",
        x = self.cursor[self.start_index:self.stop_index]
        self.assert_(self.validateSlice(x), "FAILED (slice no good)")
        print "OK"

    def test_resultsNotSame(self):
        print "Testing that different accesses return different results...",
        a = self.cursor[self.start_index]
        b = self.cursor[self.stop_index]
        self.assertNotEqual(a, b, 'FAILED (different pages same)')
        print "OK"

    def test_settingSlicesFails(self):
        print "Testing that setting as a list fails with an error...",
        def setcursorval(foo,index,stop=None):
            if stop:
                self.cursor[index:stop]=foo
            else:
                self.cursor[index] = foo
        self.assertRaises(TypeError, setcursorval, 'foo', 5)
        self.assertRaises(TypeError,setcursorval,['foo','things','stuff'], 5, 8)
        print "OK"

class pageMixin(cursorTestsMixin):
    def setUp(self):
        self.start_index = 4
        self.stop_index = 13
        cursorTestsMixin.setUp(self)
        
    def validateResult(self, r):
        if not isinstance(r, list):
            return False
        return self.check_type(r[0])

class bookMixin(cursorTestsMixin):
    def setUp(self):
        self.start_index = 22
        self.stop_index = 108
        cursorTestsMixin.setUp(self)

    def validateResult(self,r):
        return self.check_type(r)
        
class elementMixin(object):
    def check_type(self, c):
        return ElementTree.iselement(c)

class pyMixin(object):
    def check_type(self,c):
        return isinstance(c, IsbndbBook)

class TestPageCursor(unittest.TestCase, pageMixin, elementMixin):
    def setUp(self):
        print "\nTestPageCuror:",
        self.cursor_type = PageCursor
        pageMixin.setUp(self)

class TestPyPageCursor(unittest.TestCase,pageMixin, pyMixin):
    def setUp(self):
        print "\nTestPyPageCursor:",
        self.cursor_type = PyPageCursor
        pageMixin.setUp(self)
        
class TestBookCursor(unittest.TestCase,bookMixin,elementMixin):
    def setUp(self):
        print "\nTestBookCursor:",
        self.cursor_type = BookCursor
        bookMixin.setUp(self)

class TestPyBookCursor(unittest.TestCase,bookMixin,pyMixin):
    def setUp(self):
        print "\nTestPyBookCursor:",
        self.cursor_type = PyBookCursor
        bookMixin.setUp(self)

        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPageCursor,'test'))
    suite.addTest(unittest.makeSuite(TestPyPageCursor,'test'))
    suite.addTest(unittest.makeSuite(TestBookCursor, 'test'))
    suite.addTest(unittest.makeSuite(TestPyBookCursor, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main()
