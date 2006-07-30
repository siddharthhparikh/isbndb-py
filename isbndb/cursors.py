#!/usr/bin/env python
try:
    import cElementTree as ElementTree
except:
    from elementtree import ElementTree
import urllib, datetime, time
from helpers import LimitList
from book import IsbndbBook
from internet import fetch

__all__ = ['PageCursor','PyPageCursor','BookCursor','PyBookCursor']
#my accesskey to isbndb.com: 26CUOUG4

class CursorBase(object):
    def __init__(self, params, element):
        self.params = params
        
        #added caching of pages. prolly uses tons o memory, but saves time
        #not waiting for the network and conceivable save key accesses
        self.__cache={} 
            
        
        #make sure that the passed element is a book list
        if not element.tag == "BookList":
            raise TypeError, 'Element not a book list'
        
        self.totalBooks = int(element.get('total_results'))
        self.pageNum = int(element.get('page_number'))
        self.pageSize = int(element.get('page_size'))
        self.numPages,r = divmod(self.totalBooks,self.pageSize)
        if r: self.numPages += 1
    
        self.__cache[self.pageNum] = self.parse(element)
                   
    
    #properties
    #PROPERTY: pageNum
    def _get_pageNum(self):
        return self.params.pageNum
    def _set_pageNum(self, pn):
        self.params.pageNum=pn
    pageNum = property(_get_pageNum, _set_pageNum)
    
    #METHODS    
    def getPage(self, pn=None):
        if pn:
            self.pageNum = pn
        if self.__cache.has_key(self.pageNum):
            return self.__cache[self.pageNum]
        tree = self.get(self.params)
        self.__cache[self.pageNum] = self.parse(tree)
        
        return self.__cache[self.pageNum]
    
    
    #OTHER STUFF
    #
    #iterator, cuz all subclasses act like a list (in theory)
    def __iter__(self):
        p = 0
        while 1:
            try:
                r = self[p]
                p += 1
                yield r
            except IndexError:
                raise StopIteration
    
    #get, it is the function we use to get a result.
    get = staticmethod(fetch)

class PageBase(CursorBase):
    def __len__(self):
        return self.numPages

    def __getitem__(self, key):
        if isinstance(key,slice):
            return [self[a] for a in range(*key.indices(len(self)))]
        elif not isinstance(key, int):
            raise TypeError, 'Need an int as a key'
        if key < 0:
            key = self.numPages + key
        if key >= self.numPages:
            raise IndexError
        pn = key + 1
        return self.getPage(pn)

class BookBase(CursorBase):
    def __len__(self):
        return self.totalBooks

    def __getitem__(self,n):
        if isinstance(n, slice):
            return [self[a] for a in range(*n.indices(len(self)))]
        
        elif not isinstance(n, int):
            raise TypeError, 'indices must be integer'

        if n < 0:
            n = len(self) + n
        if n >= len(self):
            raise IndexError
        page,index = divmod(n, 10)
        try:
            return self.getPage(page + 1)[index]
        except:
            raise IndexError, 'stuff: %s, %s'%(page,index)

class ElementParser(object):
    def parse(self,element):
        #x = ElementTree.fromstring(p)
        #x = x.find('BookList')
        return element.getchildren()
        
class PyParser(ElementParser):
    def parse(self, p):
        x = ElementParser.parse(self, p)
        return [IsbndbBook(a) for a in x]

#page cursors
class PageCursor(PageBase,ElementParser):
    pass
class PyPageCursor(PageBase,PyParser):
    pass

#book cursors
class BookCursor(BookBase,ElementParser):
    pass
class PyBookCursor(BookBase,PyParser):
    pass
