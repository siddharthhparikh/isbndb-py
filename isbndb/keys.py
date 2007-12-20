import os.path, urllib
import sys

if sys.version_info[0] == 2 and sys.version_info[1] <= 4:
    try:
        import cElementTree as ElementTree
    except:
        from elementtree import ElementTree
elif sys.version_info[0] == 2 and sys.version_info[1] >= 5:
    from xml.etree import ElementTree

__all__ = ['getKey']

_KEYFILE = ''
_KEYS = {}

def addKey(key, name='',force_=False):
    try:
        k = Key(key, name, force_)
    except:
        return False
    _KEYS.append(k)
    return True

def getKey():
    for x in _KEYS.values():
        if x.active:
            return x
    return None

def loadKeys(fname=None, force_=False):
    global _KEYS,_KEYFILE
    if not fname:
        fname = os.path.expanduser('~/.isbndbkeys')
    if not os.path.exists(fname):
        a = ElementTree.Element('Keys')
        ElementTree.ElementTree(a).write(fname)
    _KEYFILE = fname
    _KEYS = dict()
    tree = ElementTree.parse(fname)
    for x in tree.findall('key'):
        try:
            _KEYS[x.get("name")]=Key(x.text,x.get("name"))
        except:
            if force_:
                _KEYS[x.get("name")]=Key(x.text,x.get("name"), force_=True)
            else:
                pass

def saveKeys():
    if not _KEYFILE:
        raise Exception, 'No _KEYFILE'

    tree = ElementTree.ElementTree(ElementTree.Element('Keys'))
    for x in _KEYS:
        e = ElementTree.Element('key')
        e.text = x
        tree.getroot().append(e)
    tree.write(_KEYFILE)

class Key(str):
    def __new__(cls, key, force_=False):
        return str.__new__(cls,key)

    def __init__(self, key, name, force_=False):
        #didn't i read somwhere that variable reuse is bad like this? :)
        #sys.stdout.write('Got key: %s\n' % (key,))
        x = 'http://isbndb.com/api/books.xml?access_key=%s&index1=isbn'
        x += '&value1=foo&results=keystats'
        x %=key
        a = urllib.urlopen(x).read()
        sys.stdout.write('Got from isbndb:\n %s\n' % (a,))
        y = ElementTree.fromstring(a)
        if ElementTree.iselement(y.find('ErrorMessage')):
            sys.stdout.write('Found error...')
            if force_:
                sys.stdout.write('forcing\n')
                self.active = False
                self.granted = 0
                self.limit = 0
                return
            else:
                sys.stdout.write('erroring\n')
                raise ValueError, 'either bad key or something'
        else:
            self.active = True
        y = y.find('KeyStats')
        self.granted = int(y.get('granted'))
        self.limit = int(y.get('limit'))
        self.name = name

    def update(self, elem):
        self.granted = int(elem.get('granted'))
        self.limit = int(elem.get('limit'))
        return

