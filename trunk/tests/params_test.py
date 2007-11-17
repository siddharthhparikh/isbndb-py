if __name__ == "__main__":
    import sys
    sys.path.insert(0,'..')

import unittest
import isbndb.internet as isbndb
import isbndb.keys as keys

from isbndbkey import KEY

class TestParams(unittest.TestCase):

    def setUp(self):
        print "\nTestParams:",
        self.access_key = keys.Key(KEY)
        self.testobj = isbndb.params()


    def test_key(self):
        print "Testing key stuff...",
        self.testobj.key = self.access_key
        self.access_key.active = False
        self.assertRaises(ValueError,setattr,isbndb.params(),'key'\
            ,self.access_key)
        print "OK"

    def test_searchValue(self):
        print "Testing searchValue...",
        self.testobj.searchValue = 'salmon'
        self.assertEquals(self.testobj.searchValue, 'salmon', "FAILED")
        print "OK"

    def test_searchIndex(self):
        print "Testing searchIndex...",
        self.testobj.searchIndex = 'combined'
        self.assertEquals(self.testobj.searchIndex, 'combined', 'FAILED (set)')
        self.assertRaises(ValueError, self.testobj._set_searchIndex, 'foo')
        print "OK"

    def test_results(self):
        print "Testing results...",
        self.testobj.results = 'all'
        n = self.testobj.results
        ok = self.testobj._ok_results[1:]

        self.assertEquals(n,list(ok),\
                          "FAILED (all)")
        #keystats should always be appended..
        n = ['texts','details','subjects','keystats']
        self.testobj.results = n
        self.assertEquals(self.testobj.results, n, "FAILED (list)")
        print "OK"

    def test_resultsDropsArgs(self):
        print "Testing results drops args quietly...",
        self.testobj.results = ['keystats','details','args']
        self.assertEqual(self.testobj.results, ['keystats','details'],
            "FAILED\n%s"%self.testobj.results)
        print "OK"
    def test_resultsApendsKeystats(self):
        print "Testing results appends keystats...",
        self.testobj.results = ['details']
        self.assertEqual(self.testobj.results, ['details','keystats'],'FAILED')
        print "OK"

    def test_pageNum(self):
        print "Testing page number...",
        self.testobj.pageNum = 3
        self.assertEqual(self.testobj.pageNum, 3, "FAILED (assign int)")
        self.testobj.pageNum = '14'
        self.assertEqual(self.testobj.pageNum, 14, "FAILED (assign str)")
        self.assertRaises(ValueError, self.testobj._set_pageNum, -4)
        self.assertRaises(ValueError, self.testobj._set_pageNum, 'foo')
        self.testobj.pageNum = None
        self.assertEqual(self.testobj.pageNum,None, 'FAILED (PageNum not None)')
        print "OK"

    def test_uri(self):
        print "Testing url construction...",
        import urllib
        self.testobj.pageNum = 4
        self.testobj.key = self.access_key
        self.testobj.searchIndex = 'isbn'
        self.testobj.searchValue = 'fuck you'
        self.testobj.results = ['texts','details','subjects']
        d = {'index1':'isbn', 'results':'texts,details,subjects,keystats',
             'value1':'fuck you', 'access_key':self.access_key,
             'page_number':'4'}
        test_url = 'http://isbndb.com/api/books.xml?'
        test_url += urllib.urlencode(d)
        self.assertEqual(test_url, self.testobj.url,\
            "FAILED (badurl)\nDEBUG:\ntest:%s\nreal:%s"\
            % (test_url,self.testobj.url))
        print "OK"

#For integrating tests.py
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestParams,'test'))
    return suite

if __name__ == '__main__':
    unittest.main()
