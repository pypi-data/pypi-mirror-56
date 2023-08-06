# -*- coding: utf-8 -*-

import os

from kumaoche.config import ConfigParser, ConfigPack


class StubConfig(object):
    @classmethod
    def find(cls, role: str):
        file_path_list = [os.path.dirname(__file__) + '/stub_config.yml']
        return ConfigParser.find(role, file_path_list)
