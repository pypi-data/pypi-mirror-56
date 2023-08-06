
def makedirs_ifneeded(d):
    import os
    os.makedirs(d) if not os.path.exists(d) else None
def remakedirs_anyway(d):
    import os,shutil
    shutil.rmtree(d) if os.path.exists(d) else None
    os.makedirs(d)
def inrange(n,rg):
    if n>=rg[0] and n<= rg[1]:return True
    return False
def split_list(lis,uint_size):
    num=(len(lis)-1)//uint_size+1
    l_list=[]
    [l_list.append(lis[i*uint_size:(i+1)*uint_size]) if i<num-1 else l_list.append(lis[i*uint_size:]) for i in range(num)]
    return l_list
def render_template(s, *args, **kwargs):
    from jinja2 import Environment
    env = Environment()
    tem = env.from_string(s)
    return tem.render(*args, **kwargs)
def json_load(f):
    import json
    with open(f,'r') as fp:
        return json.load(fp)
def json_dump(obj,fp):
    import json
    with open(fp,'w') as f:
        json.dumps(obj,f)
