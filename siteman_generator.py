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
            print Site(site_name, **site_data).generate_fcgi_file()
    def write_fcgi_files(self):
        pass
    def write_lighttpd_config(self):
        config_path = "/etc/lighttpd/conf-available/"
        config_enabled_path = "/etc/lighttpd/conf-enabled/"



class Site(object):
    def _path_fix(self, path):
        matches = re.match(r"^/?(.*)/?$", path)
        return u"/%s/" % matches.group(1)

    def __init__(self, name, **kwargs):

        self.project_name = name
        self.domain_name = kwargs['domain_name']
        self.project_root_dir = kwargs.get('project_root_dir',
                                            '/opt/django/%s/' % self.project_name)
        self.django_root_dir = kwargs.get('django_root_dir',
                                           "/opt/django/%s/%s/" % (self.project_name, self.project_name))
        self.fcgi_path = os.path.join(self.django_root_dir, "fcgi.py")

        self.static_root = kwargs.get('static_root',
                                      "/opt/static/")
        self.static_root = self._path_fix(self.static_root)

        self.uploaded_dir = kwargs.get('uploaded_dir',
                                       "%s_uploaded/" % self.project_name)
        self.uploaded_dir = os.path.join(self.static_root, self.uploaded_dir)

        self.static_dir = kwargs.get('media_dir',
                                    "%s/" % self.project_name)
        self.static_dir = os.path.join(self.static_root, self.static_dir)

        self.www_uploaded_path = kwargs.get("uploaded_path",
                                            "/uploaded/")
        self.www_static_path = kwargs.get('uploaded_path',
                                          '/m/')

        self.max_procs = kwargs.get('max_procs',
                                    3)

        self.virtual_env_dir = kwargs.get('virtual_env_dir',
                                           "%senv-%s/" % (self.project_root_dir, self.project_name))
        self.settings_module = kwargs.get('settings_module',
                                          "settings")
        self.settings_module = u"%s.%s" % (self.project_name, self.settings_module)

    def generate_fcgi_file(self):
        template = env.get_template('fcgi.py.jinja2')
        return template.render(**vars(self))

    def generate_lighttpd_config(self):
        template = env.get_template('lighttpd.conf')
        return template.render(**vars(self))

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Create lighttpd configuration files and fcgi.py files.')

    parser.add_argument('--config', "-c", type=argparse.FileType('r'), nargs=1,
                       help='project list file')

    args = parser.parse_args()
    config_file = vars(args)['config'][0]
    Server(config_file)

    pass
