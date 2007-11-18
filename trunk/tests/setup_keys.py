import os, sys
from isbndbkey import KEY

if sys.version_info[0] == 2 and sys.version_info[1] <= 4:
    try:
        import cElementTree as ElementTree
    except:
        from elementtree import ElementTree
elif sys.version_info[0] == 2 and sys.version_info[1] >= 5:
    from xml.etree import ElementTree

def make_keyfiles():
    x = ElementTree.Element('Keys')
    y = ElementTree.Element('key')
    y.text = KEY
    x.append(y)
    y = ElementTree.Element('key')
    y.text = 'foo'
    x.append(y)
    b = ElementTree.ElementTree(x)
    b.write('tests/xml/keys')
    b.write('tests/xml/keys3')

def check_keyfiles():
    l = ['keys','keys2','keys3']
    fl = os.listdir('tests/xml')
    for x in l:
        if x not in fl:
            return False
    return True

def main():
    if not check_keyfiles():
        make_keyfiles()

if __name__ == '__main__':
    main()
