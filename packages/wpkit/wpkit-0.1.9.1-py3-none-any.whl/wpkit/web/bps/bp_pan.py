from flask import Flask, request, Blueprint, abort, send_file
from wpkit.web import resources,utils
from wpkit.pan import Pan
from wpkit.web.resources import env
import wpkit
s=env.get_template('board.html')
print(s)

def bp_pan(app, name='pan',url_prefix='/pan',host_dir='./data/pan'):
    bp=Blueprint(name=name,import_name=app.import_name,url_prefix=url_prefix)
    app.o.sitemap[name] = url_prefix
    @bp.route('/',methods=['GET'])
    def f1():
        data=wpkit.basic.PointDict.from_dict(request.get_json())
        # pan.execute(data.command)




    return bp