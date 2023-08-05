# -*- coding: utf-8 -*-

from ..config import PackageManagerConfig
from ..exec_env import ExecEnv
from .service import Service


class PackageManager(Service):
    def __init__(self, env: ExecEnv, config: PackageManagerConfig):
        self.env = env
        self.__config = config

    def run(self, command: str):
        cmd = command.format(**self.env.assign_variables())
        return self.env.run(self.__config.run.format(**self.env.assign_variables(), **{'command': cmd}))

    def setup(self):
        return self.env.run(self.__config.setup.format(**self.env.assign_variables()))

    def update(self):
        return self.env.run(self.__config.update.format(**self.env.assign_variables()))

    def test(self, suffix=''):
        return self.env.run(f'{self.__config.test} {suffix}')
