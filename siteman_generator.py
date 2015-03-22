#!/usr/bin/env python
import os.path
import argparse
import re
import yaml
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("templates"))


class Server(object):
    def __init__(self, config_file):

        config_data = yaml.load(config_file)
        self.sites = []
        for site_name, site_data in config_data.items():
            site = Site(site_name, **site_data)
            print site.generate_lighttpd_config()
            print "-------------------------------------"
            print site.generate_fcgi_file()

    def write_fcgi_files(self):
        pass
    def write_lighttpd_config(self):
        config_path = "/etc/lighttpd/conf-available/"
        config_enabled_path = "/etc/lighttpd/conf-enabled/"


DEFAULTS = {
    "project_root_dir": "/opt/django/%(project_name)s/",
    "django_root_dir": "%(project_root_dir)s%(project_name)s/",
    "fcgi_path": "%(django_root_dir)sfcgi.py",
    "uploaded_dir": "/opt/static/uploaded_%(project_name)s/",
    "static_dir": "/opt/static/%(project_name)s/",
    "www_uploaded_path": "/uploaded/",
    "www_static_path": "/m/",
    "max_procs": "3",
    "virtual_env_dir": "%(project_root_dir)senv-%(project_name)s/",
    "settings_module": "settings"
}

class Site(object):
    def _path_fix(self, path):
        matches = re.match(r"^/?(.*)/?$", path)
        return u"/%s/" % matches.group(1)

    def _or_default(self, kwargs, key):
        return kwargs.get(key, unicode(DEFAULTS[key]) % vars(self))

    def __init__(self, name, **kwargs):

        self.project_name = name
        self.domain_name = kwargs['domain_name']
        self.project_root_dir = self._or_default(kwargs, 'project_root_dir')

        self.django_root_dir = self._or_default(kwargs, 'django_root_dir')

        self.uploaded_dir = self._or_default(kwargs, 'uploaded_dir')

        self.static_dir = self._or_default(kwargs, 'static_dir')

        self.www_uploaded_path = self._or_default(kwargs, "www_uploaded_path")
        self.www_static_path = self._or_default(kwargs, 'www_static_path')

        self.fcgi_path = self._or_default(kwargs, "fcgi_path")
        self.max_procs = self._or_default(kwargs, 'max_procs')

        self.virtual_env_dir = self._or_default(kwargs, 'virtual_env_dir')
        self.settings_module = self._or_default(kwargs, 'settings_module')
        self.settings_module = u"%s.%s" % (self.project_name, self.settings_module)

    def generate_fcgi_file(self):
        template = env.get_template('fcgi.py.jinja2')
        return template.render(**vars(self))

    def generate_lighttpd_config(self):
        template = env.get_template('lighttpd.conf.jinja2')
        return template.render(**vars(self))

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Create lighttpd configuration files and fcgi.py files.')

    parser.add_argument('--config', "-c", type=argparse.FileType('r'), nargs=1,
                       help='project list file')

    args = parser.parse_args()
    config_file = vars(args)['config'][0]
    Server(config_file)

    pass
