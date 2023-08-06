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

    def var_assign(self, text: str, append_var=None):
        if append_var is None:
            append_var = {}

        if len(self.__default_var) + len(append_var) > 0:
            return text.format(**self.__default_var, **append_var)

        return text

    def exec(self, command: str, work_dir='', append_var=None):
        if append_var is None:
            append_var = {}

        if work_dir != '':
            work_dir = self.__runner.path_filter(self.var_assign(work_dir))
            cmd = self.var_assign(command, append_var)
            return self.__runner.run(f'cd {work_dir} && {cmd}')

        return ''

    def build(self):
        return self.exec(self.__config.build, work_dir=self.__config.work_dir)

    def up(self):
        return self.exec(self.__config.up, work_dir=self.__config.work_dir)

    def down(self):
        return self.exec(self.__config.down, work_dir=self.__config.work_dir)

    def ps(self):
        return self.exec(self.__config.ps, work_dir=self.__config.work_dir)

    def run(self, command: str, work_dir='', container=''):
        if work_dir == '':
            work_dir = self.__config.work_dir

        if container == '':
            container = self.__config.container

        append_var = {'container': container, 'command': command}
        cmd = self.var_assign(command, append_var)

        if container != '':
            return self.exec(self.__config.run, work_dir=work_dir, append_var={'container': container, 'command': cmd})

        return ''
