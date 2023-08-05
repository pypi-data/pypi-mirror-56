import json,os,shutil
def json_load(fp):
    return json.load(open(fp,'r',encoding='utf-8'))
def json_dump(obj,fp):
    return json.dump(obj,open(fp,'w',encoding='utf-8'))
class Piu:
    def __init__(self,path='./db'):
        self.dbpath=path
        self.dicpath=os.path.join(self.dbpath,'data.dic')
        self.dic=self.setup()
    def setup(self):
        if self._exists():return json_load(self.dicpath)
        return self._make()
    def add(self,key,value):
        self.dic[key]=value
        self._save()
    def delete(self,key):
        del self.dic[key]
        self._save()
    def get(self,*args,**kwargs):
        return self.dic.get(*args,**kwargs)
    def _save(self):
        json_dump(self.dic,self.dicpath)
    def _exists(self):
        if os.path.exists(self.dbpath) and os.path.exists(self.dicpath):
            return True
        return False
    def _make(self):
        dir=self.dbpath
        shutil.rmtree(dir) if os.path.exists(dir) else None
        os.makedirs(dir)
        dic={}
        json_dump(dic,self.dicpath)
        return dic

def demo():
    P = Piu()
    P.add('a', 13)
    P.add('name', 'wangpei')
    P.add('age', 21)
    P.delete('a')
    age = P.get('age')
    print(age)
    x = P.get('x', 30)
    print(x)
if __name__ == '__main__':
    demo()

