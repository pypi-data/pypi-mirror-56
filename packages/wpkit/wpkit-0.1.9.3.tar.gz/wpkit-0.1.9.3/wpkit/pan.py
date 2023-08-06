import git as g
import os
from wpkit.basic import PowerDirPath,PointDict
class Pan:
    def __init__(self,path):
        assert os.path.exists(path)
        self.lpath=path
        self.repo=g.Repo(path)
        git=self.repo.git
        self.git=git
        self.curser=PowerDirPath(path)
    @classmethod
    def init(cls,path,github_path):
        os.makedirs(path) if not os.path.exists(path) else None
        repo = g.Repo.init(path)
        git = repo.git
        git.remote('add', 'origin', github_path)
        git.pull('origin', 'master')
        git.branch('--set-upstream-to=origin/master', 'master')
        return cls(path=path)
    def pull(self):
        git=self.git
        git.fetch('--all')
        git.reset('--hard','origin/master')
    def push(self):
        git=self.git
        git.add('.')
        git.commit('-m','test')
        git.push('origin','master')
    def goback(self,n=1):
        self.git.reset('--hard','HEAD'+'^'*n)
    def newFile(self,filename,location,content=None):
        loc=PowerDirPath(location)
        return loc.file(filename)(content) if content is not None else loc.file(filename)
    def newDir(self,dirname,location):
        loc = PowerDirPath(location)
        return loc(dirname)
    def delete(self,name,location):
        loc = PowerDirPath(location)
        return (loc/name).rmself()
    def getFile(self,filename,location):
        loc = PowerDirPath(location)
        return (loc/filename)()
    def getDir(self,dirname,location):
        loc = PowerDirPath(location)
        li=(loc/dirname)()
        return [{'name':i,'type':PowerDirPath(loc/dirname/i).type()} for i in li]
    def execute(self,cmd):
        cmd=PointDict.from_dict(cmd)
        op,params=cmd.op,cmd.params
        if op=='newFile':return self.newFile(**params)
        if op=='newDir':return self.newDir(**params)
        if op=='getFile':return self.getFile(**params)
        if op=='getDir':return self.getDir(**params)
        if op=='delete':return self.delete(**params)
        if op=='synch':return self.push()
        if op=='pull':return self.pull()









demo_code=\
'''
pan = Pan.init('./myspace', github_path='http://github.com/Peiiii/MyCloudSpace')
pan=Pan('./myspace')
repo.pull()
repo.goback(4)
a=pan.getDir('./',location='./myspace')
'''
