#!/usr/bin/python
import os
from isbndbkey import KEY

def check_xml():
    a = os.listdir('tests/xml')
    for b in range(1,16):
        if (str(b)+'.xml') not in a:
            return False
    return True

def make_xml():
    for a in range(1,16):
        os.system('wget -O tests/xml/%s.xml -q http://isbndb.com/api/books.xml?access_key=%s\&index1=full\&value1=sex\&results=details,keystats,texts,subjects\&page_number=%s'%(a,KEY,a))

    return

def make_keyfiles():
    x = ElementTree.Element('Keys')
    y = ElementTree.Element('key')
    y.text = KEY
    x.append(y)
    y = ElmentTree.Element('key')
    y.text = 'foo'
    x.append(y)
    b = ElementTree.ElementTree(x)
    b.write('tests/xml/keys')
    b.write('tests/xml/keys3')
    
def main():
    if not check_xml():
        make_xml()
if __name__=='__main__':
    main()

