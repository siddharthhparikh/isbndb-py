#!/usr/bin/env python
import sys

if sys.version_info[0] == 2 and sys.version_info[1] <= 4:
    try:
        import cElementTree as ElementTree
    except:
        from elementtree import ElementTree
elif sys.version_info[0] == 2 and sys.version_info[1] >= 5:
    from xml.etree import ElementTree

import urllib, datetime, time

class IsbndbBook(object):
    """elem is an ElementTree (root <BookData>. It essentiall just flattens the
    XML to a flat structure. subject and price info is in lists. The names are
    fairly easy to figure out. for instance isbn is an attribute of BookData,
    can be looked up as instance.isbn and Title is the text for the, tag but
    can be looked up by (suprise!) instance.title. all names are lowercaseified.
    """
    class Subject:
        def __init__(self,elem):
            self.subject_id = elem.get('subject_id')
            self.subject = elem.text

    class Price:
        def __init__(self,elem):
            for name,value in elem.items():
                if name == 'price':
                    self.price = float(value)
                elif name == 'check_time':
                    tf = '%Y-%m-%dT%H:%M:%S'
                    self.check_time=time.strptime(value,tf)[0:6]
                    self.check_time = datetime.datetime(*self.check_time)
                elif name == 'is_in_stock' or name == 'is_new' \
                        or name == 'is_historic':
                    setattr(self,name,int(value))
                else:
                    setattr(self,name,value)

    def __init__(self, elem):
        if elem.tag != 'BookData':
            raise ValueError, "IsbndbBook needs to be a BookData ElementTree"
        self.subjects=[]
        self.prices=[]

        for x in elem.getiterator():
            self.__addelem(x)

        #NOTE: for short title names isbndb doesnt give a value for title long,
        #i think TitleLong should be the same as Title in that case, so thats
        #what this is about. change it if you dont want this behavior.
        if not self.TitleLong:
            self.TitleLong=self.Title

    def __addelem(self, elem):
        tname=elem.tag
        if elem.text:
            text = elem.text.strip()
        else:
            text = ''
        if tname =='Subject':
            self.__addsubject(elem)
        elif tname == 'Price':
            self.__addprice(elem)
        elif tname == 'Prices' or tname=='Subjects':
            return
        else:
            setattr(self,tname,text)
            for x in elem.items():
                setattr(self,x[0],x[1].strip())

    def __addsubject(self,elem):
        self.subjects.append(self.Subject(elem))

    def __addprice(self,elem):
        self.prices.append(self.Price(elem))

