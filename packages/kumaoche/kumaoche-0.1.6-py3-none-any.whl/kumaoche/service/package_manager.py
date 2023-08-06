# -*- coding: utf-8 -*-

from ..config import PackageManagerConfig
from ..exec_env import ExecEnv
from .service import Service


class PackageManager(Service):
    def __init__(self, env: ExecEnv, config: PackageManagerConfig):
        self.__env = env
        self.__config = config

    def run(self, command: str):
        var_command = {'command': self.__env.var_assign(command)}
        return self.__env.run(self.__env.var_assign(self.__config.run, var_command))

    def setup(self):
        return self.__env.run(self.__env.var_assign(self.__config.setup))

    def update(self):
        return self.__env.run(self.__env.var_assign(self.__config.update))

    def test(self, suffix=''):
        cmd = self.__env.var_assign(self.__config.test)

        if suffix != '':
            suffix = ' ' + self.__env.var_assign(suffix)

        return self.__env.run(f'{cmd}{suffix}')
