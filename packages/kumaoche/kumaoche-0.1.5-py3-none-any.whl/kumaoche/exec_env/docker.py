# -*- coding: utf-8 -*-

from .exec_env import ExecEnv
from ..runner import Runner
from ..config import DockerConfig


class Docker(ExecEnv):
    def __init__(self, config: DockerConfig, variable: {}, runner: Runner):
        self.__config = config
        self.__default_var = variable
        self.__runner = runner

    def name(self):
        return self.__config.name

    def assign_variables(self):
        return self.__default_var

    def exec(self, command: str, append_var={'default': 0}):
        if self.__config.work_dir != '':
            work_dir = self.__runner.path_filter(self.__config.work_dir.format(**self.assign_variables()))
            cmd = command.format(**self.assign_variables(), **append_var)
            return self.__runner.run(f'cd {work_dir} && {cmd}')

    def build(self):
        return self.exec(self.__config.build)

    def up(self):
        return self.exec(self.__config.up)

    def down(self):
        return self.exec(self.__config.down)

    def ps(self):
        return self.exec(self.__config.ps)

    def run(self, command: str, container=''):
        if container == '':
            container = self.__config.container

        if container != '':
            return self.exec(self.__config.run, {'container': container, 'command': command})
