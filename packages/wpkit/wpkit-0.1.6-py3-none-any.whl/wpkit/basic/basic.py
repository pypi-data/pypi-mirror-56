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
    def isfile(self):
        return os.path.isfile(self)
    def isdir(self):
        return os.path.isdir(self)
    def exists(self):
        return os.path.exists(self)
    def base(self):
        return os.path.basename(self)
    def dirname(self):
        return os.path.dirname(self)
    def file(self,fn):
        fp=self/fn
        if not os.path.exists(fp):
            with open(fp,'w',encoding='utf-8') as f:
                f.write('')
        return fp
    def size(self):
        assert self.isfile()
        return os.path.getsize(self)
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
    def set_attribute(self,key,value):
        self.__dict__[key] = value
    def get_attribute(self,*args,**kwargs):
        return self.__dict__.get(*args,**kwargs)
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
    def ppprint(self,depth=0,step=5,space_around_delimiter=1,fillchar=' ',cell_border='|',delimiter=':'):
        import re
        def len_zh(data):
            temp = re.findall('[^a-zA-Z0-9.]+', data)
            count = 0
            for i in temp:
                count += len(i)
            return (count)
        for k,v in self.items():
            for i in range(depth):
                print(fillchar*step,end='')
                print(cell_border,end='')
            print(k.rjust(step-len_zh(k),fillchar),end=' '*space_around_delimiter+delimiter+' '*space_around_delimiter)
            if not isinstance(v,PointDict):
                print(v)
            else:
                print('\n',end='')
                v.ppprint(depth=depth+1,step=step,space_around_delimiter=space_around_delimiter,
                          cell_border=cell_border,fillchar=fillchar,delimiter=delimiter)
    def pprint2(self):
        self.ppprint(step=5, space_around_delimiter=0, fillchar='`', cell_border='|', delimiter=':')

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



class FileDirDict(PointDict):
    __type_file__='<type:file>'
    __type_dir__='<type:dir>'
    __type_link__='<type:link>'
    def set(self,**kwargs):
        for k,v in kwargs.items():
            self.set_attribute('__%s__'%(k),v)
    def set_type(self,type):
        return self.set_attribute('__type__',type)
    def get_type(self,*args,**kwargs):
        return self.get_attribute('__type__',*args,**kwargs)
    def set_size(self,size):
        return self.set_attribute('__size__',size)
    def get_size(self,*args,**kwargs):
        return self.get_attribute('__size__',*args,**kwargs)
    def print_size(self):
        print(self.auto_size_str())
    def auto_size_str(self):
        size=self.get_size()
        def gen_str(size,type):
            if size%1==0:return '%d %s'%(size,type)
            return '%.2f %s'%(size,type)
        def inrange(s):
            if size>=1 and size <1000:
                return True
        if inrange(size):return gen_str(size,'Bytes')
        size/=1024
        if inrange(size):return gen_str(size,'KB')
        size/=1024
        if inrange(size):return gen_str(size,'MB')
        size/=1024
        if inrange(size):return gen_str(size,'GB')
        size/=1024
        if inrange(size):return gen_str(size,'TB')
        size/=1024
        return gen_str(size,'PB')
    def size_str(self,type='Bytes'):
        size=self.size_format(type=type)
        if type=='Bytes':
            return '%d %s'%(size,type)
        return '%.2f %s'%(size,type)
    def size_format(self,type='Bytes'):
        size=self.get_size()
        # size=self.size()
        return self.format_size(size=size,type=type)
    def format_size(self,size,type='Bytes'):
        if type=='Bytes':return size
        size/=1024
        if type=='KB':return size
        size/=1024
        if type=='MB':return size
        size/=1024
        if type=='GB':return size
        size/=1024
        if type=='TB':return size
        else:
            raise Exception('Type %s not supported.'%(type))
    def set_face(self,string):
        self.set_attribute('__face__',string)
    def default_face(self):
        items=[]
        for k,v in self.items():
            items.append('%s:%s'%(k,v))
        return '<%s>'%(','.join(items))
    def __repr__(self):
        s=self.get_attribute('__face__',None)
        if s:
            return s
        else:
            return self.default_face()

class DirTree(FileDirDict):
    def __init__(self,path):
        path=DirPath(path)
        self.set_attribute('__path__',path)
        size=0
        for item in path():
            p2=path/item
            if p2.isdir():
                self[item]=DirTree(p2)
            elif p2.isfile():
                fsize=os.path.getsize(p2)
                self[item]=FileDirDict(name=item,size=fsize)
                self[item].set(size=fsize,type=self.__type_file__)
                self[item].size=self[item].auto_size_str()
            size+=self[item].get_size(0)
        self.set(size=size,type=self.__type_dir__)
    def size(self):
        size=0
        for k,v in self.items():
            path=self.get_attribute('__path__')/k
            if path.isfile():
                size+=path.size()
            elif path.isdir():
                size+=v.size()
        return size
    def pppprint(self):
        return self.pprint2()