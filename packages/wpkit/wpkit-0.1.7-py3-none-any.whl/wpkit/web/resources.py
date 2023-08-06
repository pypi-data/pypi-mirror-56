import pkg_resources,os
from .utils import SecureDirPath,PointDict,pkg_info,Path

data_path=pkg_info.pkg_data_dir
default_templates =PointDict.from_dict({
    'welcome': pkg_resources.resource_filename('wpkit', 'data/templates/welcome.html'),
    'files': pkg_resources.resource_filename('wpkit', 'data/templates/files.html'),
    'board': pkg_resources.resource_filename('wpkit', 'data/templates/board.html'),
    'sitemap': pkg_resources.resource_filename('wpkit', 'data/templates/sitemap.html'),
    'post': pkg_resources.resource_filename('wpkit','data/templates/post.html'),
    'outsite': pkg_resources.resource_filename('wpkit','data/templates/outsite.html')
})
default_static_dir=SecureDirPath(pkg_info.pkg_dir)/'data'/'static'
def get_default_template_string(tem):
    return open(default_templates[tem], 'r', encoding='utf-8').read()
