if __name__ == '__main__':
    import sys
    sys.path.insert(0,'..')
    prependdir = ''
else:
    prependdir = 'tests/'
    
import unittest

try:
    import cElementTree as ElementTree
except:
    from elementtree import ElementTree

import isbndb.keys as keys
from isbndbkey import KEY
class fauxKey(str):
    def __init__(self,key):
        self.active = True
        
class TestKeyObject(unittest.TestCase):
    def setUp(self):
        print '\nTestKeyConstructor:',
        import isbndb.keys as k
        self.good_key = KEY
        self.bad_key = 'foobarbaz'

    def test_goodKey(self):
        print 'Testing construction with good key...',
        self.key = keys.Key(self.good_key)
        self.assert_(isinstance(self.key, str), 'FAILED (improper subclassing)')
        self.assert_(isinstance(self.key.granted, int), 'FAILED (granted)')
        self.assert_(isinstance(self.key.limit, int), 'FAILED (limit)')
        self.assert_(self.key.active ==True, 'FAILED (made inactive key)')
        print 'OK'
    
    def test_badKey(self):
        print "Testing construction with bad key...",
        self.assertRaises(ValueError, keys.Key, self.bad_key)
        print "forced...",
        x = keys.Key(self.bad_key, force_=True)
        self.assertEqual(x, self.bad_key, "FAILED (didnt make the bad key)")
        self.assert_(x.active == False, "FAILED (made bad key active)")
        print "OK"
    
    def test_update(self):
        print "Testing the update function...",
        self.key = keys.Key(self.good_key)
        es = '<KeyStats granted="45" access_key="foo"'
        es += ' requests="45" limit="0" />'
        x = ElementTree.fromstring(es)
        self.key.update(x)
        self.assertEqual(self.key.granted, 45, 'FAILED (update granted)')
        self.assertEqual(self.key.limit, 0, 'FAILED (update limit)')
        print "OK"
        
class TestKeyFuncs(unittest.TestCase):
    def setUp(self):
        print "\nTestKeyFuncs:",
        reload(keys)

    def test_loadKeys(self):
        print "Testing loadKeys() with a test_file...",
        keys.loadKeys(prependdir+'xml/keys')
        t = [KEY,'foo']
        self.assertEqual(t, keys._KEYS, 'FAILED (loadkeys)')
        self.assert_(not keys._KEYS[-1].active, 'FAILED (bad key active)')
        print "OK"
    
    def test_loadKeysSetsFile(self):
        print "Testing that loadKeys sets the KEYFILE global...",
        keys.loadKeys(prependdir+'xml/keys')
        self.assertEqual(keys._KEYFILE, prependdir+'xml/keys',
                         "FAILED (set bad KEYFILE)\n%s"%keys._KEYFILE)
        print "OK"
    def test_loadKeysEmpty(self):
        print "Testing loadKeys() with a non-existant file...",
        import os, os.path
        f = prependdir+'xml/keys2'
        if os.path.exists(f):
            os.remove(f)
        keys.loadKeys(f)
        self.assertEqual(keys._KEYS, [], "FAILED (new keyfile not empty)")
        print "OK"

    def test_getKey(self):
        print 'Testing getKey()...',
        keys._KEYS = [fauxKey('stuff'),fauxKey('things'),fauxKey('foo')]
        keys._KEYS[0].active = False

        x = keys.getKey()
        self.assertEqual(x, 'things','FAILED (didnt get first active key)')
        x.active = False
        x = keys.getKey()
        self.assertEqual(x,'foo','FAILED (inactivating a key didnt work)')
        keys._KEYS[0].active = True
        self.assertEqual(keys.getKey(),'stuff',"FAILED (Reactivating)")
        print "OK"
    
    def test_getKeyReturnsNoneOnOutOfKeys(self):
        print "Testing getKey() returns none on no keys...",
        keys._KEYS = [fauxKey('foo'),fauxKey('bar')]
        for x in keys._KEYS:
            x.active = False
        n = keys.getKey()
        self.assert_(n is None, "FAILED")
        print "OK"

    def test_addKey(self):
        print 'Testing addKey()...',
        print 'good key...',
        good=keys.addKey(KEY)
        self.assert_(good, 'FAILED (wrong return type on good key)')
        self.assert_(KEY in keys._KEYS, 'FAILED (didnt add good key)')
        print 'bad key ...',
        bad = keys.addKey('foo')
        self.assert_(not bad, "FAILED (wront return type on bad key)")
        self.assert_('foo' not in keys._KEYS, 'FAILED (added bad key to _KEYS)')
        print 'forced bad key...',
        bad = keys.addKey('foo',force_=True)
        self.assert_(bad, "FAILED (wrong return type on forced key)")
        self.assert_('foo' in keys._KEYS, 'FAILED (didnt force bad to _KEYS)')
        self.assert_(keys._KEYS[keys._KEYS.index('foo')].active == False,
                     "FAILED (didnt make bad key inactive)")
        print "OK"
    
    def test_saveKeys(self):
        import os, os.path
        print "Testing SaveKeys...",
        keys._KEYFILE = ''
        self.assertRaises(Exception, keys.saveKeys)
        kf = prependdir+'xml/keys3'
        keys.loadKeys(prependdir+'xml/keys')
        os.remove(kf)
        if os.path.exists(kf): raise Exception, 'didnt delete kf'
        keys._KEYFILE = kf
        x = keys._KEYS
        keys.saveKeys()
        keys.loadKeys(kf)
        self.assert_(os.path.exists(kf), "FAILED (kf doesnt exits)")
        self.assert_(x == keys._KEYS, "FAILED (didnt save right)")
        print "OK"
        
        
def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(TestKeyObject, 'test'))
    s.addTest(unittest.makeSuite(TestKeyFuncs,'test'))
    return s

if __name__ == '__main__':
    unittest.main()

