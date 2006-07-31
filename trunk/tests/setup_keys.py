import os
from isbndbkey import KEY

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
