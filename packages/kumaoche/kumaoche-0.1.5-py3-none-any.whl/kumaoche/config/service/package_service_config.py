# -*- coding: utf-8 -*-

from .service_config import ServiceConfig


class PackageManagerConfig(ServiceConfig):
    def __init__(self, parsed_yaml: {}, key: str):
        super().__init__(parsed_yaml, key)

        configs = parsed_yaml.get(key, {})
        self.test = configs.get('test')
