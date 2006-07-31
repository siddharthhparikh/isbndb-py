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

    
def main():
    if not check_xml():
        make_xml()
if __name__=='__main__':
    main()

