# -*- coding: utf-8 -*-

from .service_config import ServiceConfig


class GitConfig(ServiceConfig):
    def __init__(self, parsed_yaml: {}, key: str):
        super().__init__(parsed_yaml, key)

        configs = parsed_yaml.get(key, {})

        self.repo = configs.get('repo', '')
        self.host = configs.get('host', '')
        self.org = configs.get('org', '')
        self.repo_dir = configs.get('repo_dir', '')
