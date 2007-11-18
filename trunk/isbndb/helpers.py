class LimitList(list):
    def __init__(self, li = [],ok= ['foo','bar', 'baz']):
        self.__ok = tuple(ok)
        if isinstance(li, LimitList):
            self.__ok=li._LimitList__ok
        for x in li:
            self.check_ok(x)
        return list.__init__(self,li)

    def check_ok(self, val):
        try:
            if isinstance(val, str):
                raise Exception
            a = iter(val)
        except:
            if val not in self.__ok:
                raise ValueError, "value must be in %s" % str(self.__ok)
        else:
            for x in a:
                if x not in self.__ok:
                    raise ValueError, "value must be is %s" % str(self.__ok)
        return

    def append(self, val):
        self.check_ok(val)
        return list.append(self,val)

    def extend(self,val):
        self.check_ok(val)
        return list.extend(self,val)
    def __add__(self,val):
        self.check_ok(val)
        return list.__add__(self, val)
    def __iadd__(self, val):
        self.check_ok(val)
        return list.__iadd__(self,val)

    def __setitem__(self, key, val):
        self.check_ok(val)
        return list.__setitem__(self, key, val)

    def __setslice__(self,a,b,c):
        self.check_ok(c)
        return list.__setslice__(self,a,b,c)

