import json

from tornado import web
from notebook.utils import url_path_join
from notebook.base.handlers import APIHandler
import psutil


class SysInfoHandler(APIHandler):
    """系统信息处理接口"""
    root_dir = ""
    @web.authenticated
    def get(self):
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage(self.root_dir)
        self.write(json.dumps({
            'cpu_usage': psutil.cpu_percent(interval=0.1),
            'memory_usage': int(mem.used/1024/1024),
            'memory_total': int(mem.total/1024/1024),
            'disk_usage': int(disk.used/1024/1024),
            'disk_total': int(disk.total/1024/1024),
        }))
        self.finish()


def _jupyter_server_extension_paths():
    """
    Set up the server extension for collecting metrics
    """
    return [{
        'module': 'nbsysinfo',
    }]


def _jupyter_nbextension_paths():
    """
    Set up the notebook extension for displaying metrics
    """
    return [{
        "section": "tree",
        "dest": "nbsysinfo",
        "src": "static",
        "require": "nbsysinfo/main"
    }]


def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """
    SysInfoHandler.root_dir = nbapp.contents_manager.root_dir
    route_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/sysinfo')
    nbapp.web_app.add_handlers('.*', [(route_pattern, SysInfoHandler)])
