
import pkg_resources
import os, glob, uuid
from .resources import default_templates,get_default_template_string,default_static_dir
from .utils import piu,render,pkg_info,join_path
from . import bluepoints as bps
from . import utils
try:
    from jinja2 import Environment
    from flask import Flask, request, Blueprint, abort, send_file
except:
    pass
class App(Flask):
    def __init__(self, import_name ,dbpath='./data/db',add_pkg_resources=True):
        super().__init__(import_name)
        self.default_templates = default_templates
        self.db=piu.Piu(dbpath)
        self.o=utils.IterObject()
        self.o.sitemap={}
        if add_pkg_resources:
            self.add_static(url_prefix='/pkg-resource', static_dir=default_static_dir)
    def add_default_route(self):
        self.register_blueprint(self.bp_root())
        self.register_blueprint(self.bp_board())
        self.add_multi_static({'/fs':'./'})
    def add_multi_static(self, dic):
        for k, v in dic.items():
            self.add_static(k, v)
    def add_static(self, url_prefix, static_dir, template=None, name=None):
        name = 'bp_static_' + uuid.uuid4().hex if not name else name
        bp = self.bp_static(url_prefix=url_prefix,static_dir=static_dir, template=template, name=name)
        self.register_blueprint(bp)
    def get_default_template_string(self,tem):
        return open(self.default_templates[tem],'r',encoding='utf-8').read()
    def bp_sitemap(self,name='sitemap',url_prefix='/sitemap',map={}):
        bp = Blueprint(name=name, import_name=self.import_name, url_prefix=url_prefix)
        @bp.route('/')
        def do_root():
            temf = self.default_templates['sitemap']
            return render(open(temf, 'r', encoding='utf-8').read(),list=map.items())
        return bp
    def bp_root(self,name='root',url_prefix='/'):
        bp = Blueprint(name=name, import_name=self.import_name, url_prefix=url_prefix)
        @bp.route('/')
        def do_root():
            temf = self.default_templates['welcome']
            return render(open(temf, 'r', encoding='utf-8').read())
        return bp
    def bp_board(self,name='board',url_prefix='/board'):
        bp=Blueprint(name=name,import_name=self.import_name,url_prefix=url_prefix)
        @bp.route('/')
        def do_board():
            data = self.db.get('board_data', '')
            return render(self.get_default_template_string('board'), content=data)
        @bp.route('/post', methods=['POST'])
        def do_board_post():
            data = request.get_json()
            # print('board data:%s' % (data))
            self.db.add('board_data', data['content'])
            return 'success'
        return bp
    def bp_static(self,url_prefix='/fs', static_dir='./', template=None, name='None'):
        name = 'bp_static_' + uuid.uuid4().hex if not name else name
        template = self.default_templates['files'] if not template else template
        bp = Blueprint(name=name, import_name=self.import_name,url_prefix=url_prefix)

        @bp.route('/', defaults={'req_path': ''})
        @bp.route(join_path('/', '<path:req_path>'))
        def dir_listing(req_path):
            BASE_DIR = static_dir
            abs_path = os.path.join(BASE_DIR, req_path)
            if not os.path.exists(abs_path):
                return abort(404)
            if os.path.isfile(abs_path):
                return send_file(abs_path)
            if os.path.isdir(abs_path):
                fns = os.listdir(abs_path)
                fps = [join_path(url_prefix, req_path, f) for f in fns]
                return render(open(template, 'r', encoding='utf-8').read(), files=zip(fps, fns))

        return bp


def get_default_app(import_name,static_dir_dic=None):
    app = App(__name__)
    app.register_blueprint(bps.bp_welcome(app, url_prefix='/'))
    app.register_blueprint(bps.bp_static(app, url_prefix='/files', static_dir='./', name='files'))
    app.add_multi_static(static_dir_dic) if static_dir_dic else None
    app.register_blueprint(bps.bp_board(app, url_prefix='/board'))
    if pkg_info.is_linux():
        app.register_blueprint(bps.bp_post_and_download_by_linux_wget(app, url_prefix='/post_and_download'))
    app.register_blueprint(bps.bp_sitemap(app, url_prefix='/sitemap'))
    return app
def start_simple_http_server(import_name,host='127.0.0.1',port=80,static_dir_dic=None):
    app=get_default_app(import_name=import_name,static_dir_dic=static_dir_dic)
    print(app.url_map)
    app.run(host=host,port=port)

if __name__ == '__main__':
    start_simple_http_server(__name__)