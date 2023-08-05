import os,shutil
class IterObject(dict):
    __no_value__='<__no_value__>'
    def __getattr__(self, key):
        v=self.get(key,self.__no_value__)
        if v is self.__no_value__:
            self[key]=IterObject()
            return self[key]
        else:
            return v
    def __setattr__(self, key, value):
        self[key]=value
class Path(str):
    __no_value__ = '<__no_value__>'
    def __init__(self,*args,**kwargs):
        super().__init__()
    def __getattr__(self, item):
        return self/item
    def __setattr__(self, key, value):
        self.__dict__[key]=value
    def __truediv__(self, other):
        return Path(self+'/'+other)
    def __call__(self,s):
        return self/s

class StrictPath:
    def __init__(self,s):
        self.__value__=Path(self.__strict__(s))
    def __strict__(self,s):
        prefix='/' if s.startswith('/') or s.startswith("\\") else ''
        def remove_all(lis,item):
            if item in lis:
                lis.remove(item)
                return remove_all(lis,item)
            else:
                return lis
        lis=s.split('/')
        lis2=[]
        for i in lis:
            lis2+=i.split('\\')
        lis=lis2
        lis=remove_all(lis,'/')
        lis=remove_all(lis,"\\")
        lis=remove_all(lis,'')
        return prefix+'/'.join(lis)
    def __getattr__(self, item):
        return self/item
    def __truediv__(self, other):
        return StrictPath(self.__value__/other).__value__
    def __call__(self, s=''):
        if s=='':return self.__value__
        return StrictPath(self.__value__/s)
    def __repr__(self):
        return "<StrictPath:'%s'>"%(self.__value__)
    def __str__(self):
        return self.__value__
def join_path(*args):
    return StrictPath('/'.join(args))()

class SecureDirPath(str):

    __no_value__ = '<__no_value__>'
    def __init__(self,s):
        super().__init__()
    def __getattr__(self, item):
        return self/item
    def __truediv__(self, other):
        return SecureDirPath(StrictPath(self+'/'+other))
    def __call__(self):
        assert os.path.exists(self)
        return self.__read__()
    def file(self,fn):
        fp=self/fn
        return fp
    def __read__(self):
        import os
        if os.path.isfile(self):
            with open(self,'r',encoding='utf-8') as f:
                return f.read()
        if os.path.isdir(self):
            return os.listdir(self)

class DirPath(str):

    __no_value__ = '<__no_value__>'
    def __init__(self,s):
        super().__init__()
    def __getattr__(self, item):
        return self/item
    def __truediv__(self, other):
        return DirPath(StrictPath(self+'/'+other))
    def __call__(self, s=__no_value__):
        assert os.path.exists(self)
        if s is self.__no_value__:
            return self.__read__()
        else:
            return self.__write__(s)
    def file(self,fn):
        fp=self/fn
        if not os.path.exists(fp):
            with open(fp,'w',encoding='utf-8') as f:
                f.write('')
        return fp
    def __write__(self,s):
        assert os.path.isfile(self) or os.path.isdir(self)
        if os.path.isfile(self):
            with open(self,'w',encoding='utf-8') as f:
                f.write(s)
                return s
        else:
            s2 = self / s
            os.mkdir(s2) if not os.path.exists(s2) else None
            return s2
    def __read__(self):
        import os
        if os.path.isfile(self):
            with open(self,'r',encoding='utf-8') as f:
                return f.read()
        if os.path.isdir(self):
            return os.listdir(self)

class PowerDirPath(DirPath):
    '''
    This class can be very distructive.
    Be Really Careful !!!
    '''
    def rmself(self):
        assert os.path.isdir(self) or os.path.isfile(self)
        if os.path.isdir(self):
            shutil.rmtree(self)
        else:
            os.remove(self)
    def __truediv__(self, other):
        return PowerDirPath(DirPath(self).__truediv__(other))

class PointDict(dict):
    __no_value__='<__no_value__>'
    def __getattr__(self, key):
        return self.get(key)
    def __setattr__(self, key, value):
        self[key]=value
    def __call__(self, key , value=__no_value__):
        if value is self.__no_value__:
            self[key]=PointDict()
        else:
            self[key]=value
        return self[key]
    @classmethod
    def from_dict(cls,dic):
        dic2=cls()
        for k,v in dic.items():
            if not isinstance(v,dict):
                dic2[k]=v
            else:
                dic2[k]=cls.from_dict(v)
        return dic2
    def pprint(self):
        import json
        print(json.dumps(self,sort_keys=True,indent=4))

import os
def dir_tree(dir):
    dic=PointDict()
    items=os.listdir(dir)
    for item in items:
        path=dir+'/'+item
        if os.path.isdir(path):
            dic[item]=dir_tree(path)
        else:
            dic[item]=item
    return dic
