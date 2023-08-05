# -*- coding: utf-8 -*-

from .exec_env_config import ExecEnvConfig


class DockerConfig(ExecEnvConfig):
    def __init__(self, parsed_yaml: {}, key: str):
        super().__init__(parsed_yaml, key)

        configs = parsed_yaml.get(key, {})

        self.container = configs.get('container', '')
        self.ps = configs.get('ps', '')
        self.build = configs.get('build', '')
        self.up = configs.get('up', '')
        self.down = configs.get('down', '')
