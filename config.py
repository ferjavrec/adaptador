#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = "Fernando Recci <<Geneos>> <reccifernando@gmail.com>"
__copyright__ = "Copyright (C) 2018 GENEOS http://www.geneos.com.ar/"
__license__ = "GPL 3.0"
__version__ = "1.00"

import os

try:
    from ConfigParser import RawConfigParser, NoSectionError, NoOptionError
except ImportError:  
    # Python 3
    from configparser import RawConfigParser, NoSectionError, NoOptionError

__all__ = ['config']

path = '/home/fer/unqui/'
CONFIG_PATH = [
    path + 'configuracion.conf',
]


class ConfigurationManager(object):
    def __init__(self):
        self.config = RawConfigParser()
        self.config.read(CONFIG_PATH)

    def get(self, section, name):
        try:
            return self.config.get(section, name)
        except (NoSectionError, NoOptionError):
            pass

        return None

    def read(self, config_file):
        self.config.read(config_file)


config = ConfigurationManager()
