# -*- coding: utf-8 -*-

from .exec_env_config import ExecEnvConfig


class ShellConfig(ExecEnvConfig):
    def __init__(self, parsed_yaml: {}, key: str):
        super().__init__(parsed_yaml, key)
