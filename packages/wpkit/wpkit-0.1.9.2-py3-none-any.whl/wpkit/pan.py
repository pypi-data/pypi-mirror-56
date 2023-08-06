import git as g
import os
from wpkit.basic import PowerDirPath
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
    def newFile(self,fn,location,content=None):
        loc=PowerDirPath(location)
        return loc.file(fn)(content) if content is not None else loc.file(fn)
    def newDir(self,dn,location):
        loc = PowerDirPath(location)
        return loc(dn)
    def delete(self,name,location):
        loc = PowerDirPath(location)
        return (loc/name).rmself()
    def getFile(self,fn,location):
        loc = PowerDirPath(location)
        return (loc/fn)()
    def getDir(self,dn,location):
        loc = PowerDirPath(location)
        li=(loc/dn)()
        return [{'name':i,'type':PowerDirPath(loc/dn/i).type()} for i in li]










demo_code=\
'''
pan = Pan.init('./myspace', github_path='http://github.com/Peiiii/MyCloudSpace')
pan=Pan('./myspace')
repo.pull()
repo.goback(4)
a=pan.getDir('./',location='./myspace')
'''
