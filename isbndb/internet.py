#!/usr/bin/env python

try:
    import cElementTree as ElementTree
except:
    from elementtree import ElementTree
import urllib, datetime, time
from helpers import LimitList
import keys
#
#my accesskey to isbndb.com: 26CUOUG4
#

class params(object):
    _ok_search = ('isbn','title','combined','full','publisher_id',\
                      'book_id', 'person_id', 'subject_id')
    _ok_results = ('args','texts','details','prices','pricehistory',\
                    'subjects','keystats')
    
    def __init__(self):
        self.__access_key = None 
        self.results = []
        self.searchValue = ''
        self.searchIndex = 'isbn'
        self.pageNum = None
    #properties
    #PROPERTY: url
    def _get_url(self, sv=''):
        if sv:
            self.__v1 = sv
        d = {}
        d['access_key'] = self.__access_key
        d['index1'] = self.__i1
        d['value1'] = self.__v1
        d['results'] = ','.join(self.results)
        #pagenumber must be >= 1
        if  self.pageNum >=1:
            d['page_number'] = self.pageNum
        a='http://isbndb.com/api/books.xml?'+urllib.urlencode(d)
        return a
    url = property(_get_url)

    #PROPERTY: searchValue
    def _set_searchValue(self, sv):
        self.__v1 = sv
    def _get_searchValue(self):
        return self.__v1
    searchValue = property(_get_searchValue, _set_searchValue)

    #PROPERTY: searchIndex
    def _get_searchIndex(self):
        return self.__i1
    def _set_searchIndex(self, i):
        if i not in self._ok_search:
            raise ValueError
        else:
            self.__i1 = i
    searchIndex = property(_get_searchIndex,_set_searchIndex)

    #PROPERY: results
    def _get_results(self):
        return self.__results
    def _set_results(self, val):
        if isinstance(val, str) and val == 'all':
            self.__results = LimitList(self._ok_results[1:], self._ok_results)
            return
        if 'args' in val:
            del val[val.index('args')]
        if 'keystats' not in val:
            val.append('keystats')
        self.__results = LimitList(val, self._ok_results)
    results = property(_get_results,_set_results)
    
    #PROPERTY: pageNum
    def _get_pageNum(self):
        return self.__pn
    def _set_pageNum(self, val):
        #none value sets dont get page
        if val == None:
            self.__pn = val
            return
            
        try:
            val = int(val)
        except:
            raise ValueError, "pageNum must be able to turn into an int"

        if val < 1:
            raise ValueError, "pageNum must be greater than 1"
        self.__pn = val
    pageNum = property(_get_pageNum, _set_pageNum)
    
    #PROPERTY: key
    def _get_key(self):
        return self.__access_key
    def _set_key(self, key):
        if not hasattr(key, 'active'):
            try:
                key = keys.Key(key)
            except:
                raise ValueError, 'invalid key'
        if not key.active:
            raise ValueError,'key is not active'
        self.__access_key = key
    key = property(_get_key,_set_key)

#Fetch function, gets stuff from the internets
def fetch(param):
    a = urllib.urlopen(param.url)
    x = unicode(a.read(),'ascii',errors='ignore')
    tree = ElementTree.fromstring(x)
    err = tree.find('ErrorMessage')
    if ElementTree.iselement(err):
        raise Exception, 'an error occurred'
    stats = tree.find('KeyStats')
    list = tree.find('BookList')
    param.key.update(stats)
    return list
