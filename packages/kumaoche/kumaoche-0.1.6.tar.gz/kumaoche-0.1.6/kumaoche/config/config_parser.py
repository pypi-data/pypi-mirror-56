# -*- coding: utf-8 -*-

import yaml
import os
import sys

from .config_pack import ConfigPack


class ConfigParser(object):

    @classmethod
    def file_path_list(cls):
        return os.environ.get('KUMAOCHE_CONFIG_PATH', os.getcwd() + '/kumaoche_config.yml').split(':')

    @classmethod
    def all_roles(cls, file_path_list=None):
        loaded_yaml = cls.yaml_load(file_path_list)
        parsed_yaml = cls.parse_version(loaded_yaml)
        loaded_roles = parsed_yaml.get('roles', {})

        # 順序を維持した重複削除
        return sorted(set(loaded_roles), key=loaded_roles.index)

    @classmethod
    def find(cls, role: str, file_path_list=None):
        loaded_yaml = cls.yaml_load(file_path_list)
        parsed_yaml = cls.parse_version(loaded_yaml)
        loaded_roles = parsed_yaml.get('roles', {})

        if role not in loaded_roles.keys():
            print(f'Target role "{role}" is not exist.')
            sys.exit()

        return ConfigPack(loaded_roles.get(role, {}))

    @classmethod
    def yaml_load(cls, file_path_list=None):
        if file_path_list is None:
            file_path_list = cls.file_path_list()

        # ファイル存在確認
        for path in file_path_list:
            if not os.path.exists(path):
                print(f'Target config file "{path}" is not exist.')
                sys.exit()

        loaded_yaml = {}
        for file_path in file_path_list:
            with open(file_path) as file:
                loaded_yaml = {**loaded_yaml, **yaml.safe_load(file)}

        return loaded_yaml

    @classmethod
    def parse_version(cls, loaded_yaml):
        version = int(loaded_yaml.get('version', 1))

        if version == 1:
            return loaded_yaml
        else:
            print(f'Yaml version "{version}" is invalid.')
            sys.exit()
