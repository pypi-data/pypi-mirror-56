import re

class NodeMetaClass(type):
    __not_found__='not_found'
    def __new__(cls, name, bases, attrs):
        attrs['__node_type__']=name.lower()
        if attrs.get('__open_node__',cls.__not_found__)==cls.__not_found__:
            attrs['__open_node__']=True
        return type.__new__(cls, name, bases, attrs)

class Node(dict,metaclass=NodeMetaClass):
    def __init__(self, **kwargs):
        self.__dict__['__children__'] = []
        super().__init__(**kwargs)

    def __call__(self, *args):
        args=list(args)
        for i in range(len(args)):
            if isinstance(args[i],str):
                s=args[i].strip()
                if s.startswith('<!--') and s.endswith('-->'):
                    args[i]=Comment(s.lstrip('<!--').rstrip('-->'))
                else:
                    args[i]=Text(s)
        self.__dict__['__children__'] = args
        return self

    def __getattr__(self, key):
        return self.get(key, None)

    def __setattr__(self, key, value):
        self[key] = value

    def set_attribute(self, key, value):
        self.__dict__[key] = value

    def get_attribute(self, *args, **kwargs):
        return self.__dict__.get(*args, **kwargs)

    def seta(self, **kwargs):
        for k, v in kwargs.items():
            self.set_attribute('__%s__' % (k), v)

    def geta(self, key, *args, **kwargs):
        return self.get_attribute('__%s__' % (key), *args, **kwargs)

    def find(self, sel):
        pass

    def to_string(self, depth=0):
        def to_string(ch,depth=0):
           return ch.to_string(depth=depth) if isinstance(ch,Node) else '\n'+'\t'*depth+str(ch)
        if self.__open_node__:
            mid='\n'+'\t' * depth if len(self.__dict__['__children__']) else ''
            return '\n%s<%s %s>%s%s</%s>' % ('\t' * depth,
                                               self.__node_type__,
                                               ' '.join(['%s="%s"' % ('class' if k == '_class' else k, v) for k, v in self.items()]),
                                               ''.join([to_string(ch,depth=depth + 1) for ch in self.__dict__['__children__']]),
                                                mid,
                                               self.__node_type__)
        else:
            return '\n%s<%s %s/>' % ('\t' * depth,
                                      self.__node_type__,
                                      ' '.join(['%s="%s"' % ('class' if k == '_class' else k, v) for k, v in self.items()]))

    def __str__(self):
        return self.to_string()
class CloseNode(Node):
    __open_node__=False
class Text(Node):
    def __init__(self,content=''):
        self.__dict__['content']=content
    def to_string(self, depth=0):
        return '\n'+'\t'*depth+str(self.__dict__['content'])

class Comment(Node):
    def __init__(self,content=''):
        self.__dict__['content']=content
    def to_string(self, depth=0):
        return '\n'+'\t'*depth+'<!--'+str(self.__dict__['content'])+'-->'

class Html(Node):pass
class Head(Node):pass
class Meta(CloseNode):pass
class Link(CloseNode):pass
class Style(Node):pass
class Body(Node):pass
class Div(Node):pass
class Span(Node):pass
class H(Node):pass
class P(Node):pass
class A(Node):pass
class Img(CloseNode):pass

