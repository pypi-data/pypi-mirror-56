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
    __type_file__ = '<type:file>'
    __type_dir__ = '<type:dir>'
    __type_link__ = '<type:link>'
    __type_mount__='<type:mount>'
    __type_not_exists__='<type:not_exists>'
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
            self.__write__(s)
            return self
    def info(self):
        assert self.exists()
        info=PointDict()
        info.atime=self.getatime()
        info.ctime=self.getctime()
        info.mtime=self.getmtime()
        info.type=self.type()
        return info
    def type(self):
        if self.isfile():return self.__type_file__
        if self.isdir():return self.__type_dir__
        if self.islink():return self.__type_link__
        if self.ismount():return self.__type_mount__
        return self.__type_not_exists__
    def isfile(self):
        return os.path.isfile(self)
    def isdir(self):
        return os.path.isdir(self)
    def islink(self):
        return os.path.islink(self)
    def ismount(self):
        return os.path.ismount(self)
    def isabs(self):
        return os.path.isabs(self)
    def abspath(self):
        return os.path.abspath(self)
    def lexists(self):
        return os.path.lexists(self)
    def exists(self):
        return os.path.exists(self)
    def basename(self):
        return os.path.basename(self)
    def dirname(self):
        return os.path.dirname(self)
    def getatime(self):
        return os.path.getatime(self)
    def getctime(self):
        return os.path.getctime(self)
    def getmtime(self):
        return os.path.getmtime(self)
    def getsize(self):
        assert self.isfile()
        return os.path.getsize(self)
    def add(self,s):
        assert self.isfile()
        with open(self,'a',encoding='utf-8') as f:
            f.write(s)
        return self
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
    def seta(self,**kwargs):
        for k,v in kwargs.items():
            self.set_attribute('__%s__'%(k),v)
    def geta(self,key,*args,**kwargs):
        return self.get_attribute('__%s__'%(key),*args,**kwargs)
    @classmethod
    def from_dict(cls,dic):
        dic2=cls()
        for k,v in dic.items():
            if not isinstance(v,dict):
                dic2[k]=v
            else:
                dic2[k]=cls.from_dict(v)
        return dic2
    def print(self):
        import json
        print(json.dumps(self,sort_keys=True,indent=4))
    def print1(self,depth=0,step=5,space_around_delimiter=1,fillchar=' ',cell_border='|',delimiter=':'):
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
                v.print1(depth=depth+1,step=step,space_around_delimiter=space_around_delimiter,
                          cell_border=cell_border,fillchar=fillchar,delimiter=delimiter)
    def pprint1(self):
        self.print1(step=5, space_around_delimiter=0, fillchar='`', cell_border='|', delimiter=':')

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
    def set_info(self,info):
        return self.seta(info=info)
    def get_info(self):
        return self.geta('info')
    def info(self,*args,**kwargs):
        if len(args)!=0:
            return self.get_info()[args[0]]
        if len(kwargs)!=0:
            info=self.get_info()
            info.update(**kwargs)
            return self.set_info(info)
        return self.get_info()
    def generate_info(self):
        path=self.path()
        info=path.info()
        info.update(path=path)
        info.update(abspath=path.abspath())
        self.set_info(info)
    def set_type(self,type):
        return self.set_attribute('__type__',type)
    def get_type(self,*args,**kwargs):
        return self.get_attribute('__type__',*args,**kwargs)
    def set_size(self,size):
        return self.set_attribute('__size__',size)
    def get_size(self,*args,**kwargs):
        return self.get_attribute('__size__',*args,**kwargs)
    def get_path(self):
        return self.geta('path')
    def set_path(self,path):
        return self.seta(path=path)
    def path(self):
        return self.get_path()
    def print_size(self):
        print(self.auto_size_str())
    def auto_size_str(self):
        size = self.get_size()
        return self.pretty_format_size(size)
    def pretty_format_size(self,size):
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
    def info_format(self):
        return self.format_info(self.info())
    def format_info(self,info):
        info2=PointDict()
        for fd in ['atime','ctime','mtime']:
            v=info.get(fd,self.__no_value__)
            if v:
                info2[fd]=self.format_time(v)
        fd='size'
        v=info.get(fd,self.__no_value__)
        if v:
            info2[fd] = self.pretty_format_size(v)
        info3=PointDict(info)
        info3.update(info2)
        return info3


    def size_format(self,type='Bytes'):
        size=self.get_size()
        # size=self.size()
        return self.format_size(size=size,type=type)
    def format_time(self,t):
        import time
        t=time.gmtime(t)
        return time.strftime('%Y-%m-%d %H:%M:%S',t)
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
    def print2(self,depth=0,step=5,space_around_delimiter=0,fillchar=' ',cell_border='|',delimiter=':'):
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
            if v.path().isfile():
                print('\n',end='')
                v.info_format().print1(depth=depth+1,step=step,space_around_delimiter=space_around_delimiter,
                          cell_border=cell_border,fillchar=fillchar,delimiter=delimiter)
            else:
                print('\n',end='')
                v.print2(depth=depth+1,step=step,space_around_delimiter=space_around_delimiter,
                          cell_border=cell_border,fillchar=fillchar,delimiter=delimiter)
    def pprint2(self):
        return self.print2(step=5, space_around_delimiter=0, fillchar='`', cell_border='|', delimiter=':')
class DirTree(FileDirDict):
    def __init__(self,path):
        path=DirPath(path)
        self.set_path(path)
        self.generate_info()
        size=0
        n=0
        N=0
        for item in path():
            n+=1
            p2=path/item
            if p2.isdir():
                self[item]=DirTree(p2)
                N+=self[item].info('N')
            elif p2.isfile():
                N+=1
                file=FileDirDict(name=item)
                file.set_path(p2)
                file.generate_info()
                fsize = p2.getsize()
                file.info(size=fsize)
                file.set_size(size=fsize)
                file.update(size=file.auto_size_str())
                self[item]=file
            size+=self[item].info('size')
        self.info(size=size,n=n,N=N)
    def size(self):
        size=0
        for k,v in self.items():
            path=self.geta('path')/k
            if path.isfile():
                size+=path.size()
            elif path.isdir():
                size+=v.size()
        return size
    def pppprint(self):
        return self.pprint2()