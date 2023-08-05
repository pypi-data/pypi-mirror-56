# -*- coding: utf-8 -*-

from .service_config import ServiceConfig


class DbConfig(ServiceConfig):
    def __init__(self, parsed_yaml: {}, key: str):
        super().__init__(parsed_yaml, key)

        configs = parsed_yaml.get(key, {})
        self.host = configs.get('host', '')
        self.port = configs.get('port', '')
        self.user = configs.get('user', '')
        self.database = configs.get('database', '')
