__all__ = ['IsbndbSearch','PageCursor','PyPageCursor','BookCursor',
           'PyBookCursor','getKey','loadKeys','saveKeys','addKey','fetch',
           'params']

#from key import *
from cursors import *
from keys import getKey, loadKeys, saveKeys, addKey
from internet import fetch, params
#from keys import Keys

#IsbndbSearch function, a factory that makes cursors. Also does silly things,
#like makes search way easy...
def IsbndbSearch(searchValue='', searchIndex='',\
                   results=[], key='', p=None, cursor=PyBookCursor):
    if not p and not searchValue:
        raise Exception, 'must pass either params or a search value'
    if p:
        if p.key is None:
            p.key = keys.getKey()
    else:
        p = params()
        if not key:
            key = keys.getKey()
        p.key = key
        if results: p.results = results
        if searchValue: p.searchValue = searchValue
        if searchIndex: p.searchIndex = searchIndex

    while True:
        try:
            x = fetch(p)
        except:
            p.key.active = False
            p.key = keys.getKey()
            if not p.key: raise Exception,'out of keys'
        else:
            break
    return cursor(p,x)
