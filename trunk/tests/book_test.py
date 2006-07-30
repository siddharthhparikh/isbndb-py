import unittest
from datetime import datetime
import sys
sys.path.insert(0,'..')
try:
    import cElementTree as ElementTree
except:
    from elementtree import ElementTree
    
from isbndb.book import IsbndbBook

class Comparer(object):
    def __init__(self):
        """This class just holds the values the book should have at the same
        name. For comparison purposes..."""
        self.book_id = 'unix_system_administration_handbook_a01'
        self.isbn = '0130206016'
        self.Title = "UNIX System Administration Handbook"
        self.TitleLong = "UNIX System Administration Handbook (3rd Edition)"
        self.AuthorsText = 'Evi Nemeth, Garth Snyder, Scott Seebass, Trent R. Hein'
        self.dewey_decimal=''
        self.physical_description_text="7.1\"x9.2\"x1.3\"; 896 pages; 2.7 lb"
        self.language = ''
        self.edition_info = 'Paperback; 2000-08'
        self.store_isbn=""
        self.store_title=""
        self.store_url="http://isbndb.com/x/book/unix_system_administration_"\
            +"handbook_a01/buy/isbn/textbookx.html"
        self.store_id="textbookx"
        self.currency_code="USD"
        self.is_in_stock=1
        self.is_historic = 0
        self.check_time=datetime(2005,3,11,13,49,22)
        self.is_new = 0
        self.currency_rate='1'
        self.price = 45.33
        
class IsbndbBookTest(unittest.TestCase):
    def setUp(self):
        #This uses a canned file so that im not dealing with changed values to
        #check two parsers against each other...
        print '\nIsbndbBookTest:',
        elem = ElementTree.parse('tests/xml/book_test.xml')
        elem = elem.getroot()
        elem = elem.find('BookList')
        elem = elem.find('BookData')
        self.book = IsbndbBook(elem)
        self.comparer = Comparer()
    
    def test_basicFunc(self):
        print 'Testing basic constructor functionality...',
        c = self.assertEqual
        c(self.book.book_id, self.comparer.book_id, "FAILED (bad book_id)")
        c(self.book.isbn, self.comparer.isbn, 'FAILED (bad isbn)')
        c(self.book.Title, self.comparer.Title, 'FAILED (bad Title)')
        c(self.book.TitleLong, self.comparer.TitleLong,'FAILED (bad TitleLong)')
        c(self.book.AuthorsText, self.comparer.AuthorsText,\
                'FAILED (bad AuthorsText)')
        c(self.book.dewey_decimal, self.comparer.dewey_decimal,\
                'FAILED (bad dewey_decimal)')
        c(self.book.physical_description_text, self.comparer.physical_description_text, "FAILED (pysical_description_text)\n%s\n%s"% (self.book.physical_description_text, self.comparer.physical_description_text))
        c(self.book.language, self.comparer.language, 'FAILED (bad language)')
        c(self.book.edition_info, self.comparer.edition_info,\
                "FAILED (bad edition_info)")
        self.assert_(len(self.book.prices) == 27, 'FAILED (wrong # of prices)\n%s,%s'%(len(self.book.prices),27))
        self.assert_(len(self.book.subjects) == 2, 'FAILED (wrong # of subs)')
        print "OK"
    
    def test_priceContstuctor(self):
        print 'Testing that the price is right...',
        fs = 'FAILED (bad %s)'
        x = self.book.prices[0]
        c = self.comparer
        f = self.assertEqual
        f(x.store_isbn, c.store_isbn, 'FAILED (bad store_isbn)')
        f(x.store_title, c.store_title,'FAILED (bad store_title)')
        f(x.store_url, c.store_url,\
            'FAILED (bad store_url)\n%s\n%s'%(x.store_url,c.store_url))
        f(x.store_id, c.store_id, fs%('store_id'))
        f(x.currency_code, c.currency_code, fs%'currency_code')
        f(x.is_in_stock, c.is_in_stock, fs%'is_in_stock')
        f(x.is_historic, c.is_historic, fs%'is_historic')
        f(x.is_new, c.is_new, fs % 'is_new')
        f(x.check_time, c.check_time, fs% 'check_time')
        f(x.currency_rate, c.currency_rate, fs%'currency_rate')
        f(x.price, c.price, fs % 'price')
        print 'OK'

    def test_subjectConstructor(self):
        print 'Testing that the subject is right...',
        x = self.book.subjects[0]
        self.assertEqual(x.subject_id,'amazon_com_computers_internet_operating_systems_unix_adminis', 'FAILED (subject_id)')
        self.assertEqual(x.subject,'Amazon.com -- Computers & Internet --'\
            +' Operating Systems -- Unix -- Administration', \
            'FAILED (subject)\ntv:%s'%x.subject)
        print "OK"
    
    def test_titleBehavior(self):
        print "Testing Title and TitleLong match if no TitleLong given...",
        xmlstr =\
        '''<BookData book_id="test" isbn="0000000000">
           <Title>Foo</Title>
           <TitleLong></TitleLong>
           </BookData>'''
        x = ElementTree.fromstring(xmlstr)
        book = IsbndbBook(x)
        self.failUnless(book.Title == book.TitleLong, "FAILED (titles)")
        print "OK"

    def test_badValuePassed(self):
        print "Testing that a bad element passed raises an error...",
        xmlstr = \
        """<FooBar isbn="0000000000"><Title>Stuff</Title></FooBar>"""
        x = ElementTree.fromstring(xmlstr)
        self.assertRaises(ValueError,IsbndbBook,x)
        print "OK"

def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(IsbndbBookTest, 'test'))
    return s

if __name__ == '__main__':
    unittest.main()
