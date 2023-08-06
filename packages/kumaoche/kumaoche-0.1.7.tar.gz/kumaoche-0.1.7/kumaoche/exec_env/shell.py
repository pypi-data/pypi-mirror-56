# -*- coding: utf-8 -*-

from .exec_env import ExecEnv
from ..runner import Runner
from ..config import ShellConfig


class Shell(ExecEnv):
    def __init__(self, config: ShellConfig, variable: {}, runner: Runner):
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

    def run(self, command: str, work_dir=''):
        if work_dir == '':
            work_dir = self.__runner.path_filter(self.var_assign(self.__config.work_dir))

        if work_dir != '':
            work_dir = f'cd {work_dir} && '

        cmd = self.var_assign(command)
        cmd = self.var_assign(self.__config.run, {'command': cmd})

        return self.__runner.run(f'{work_dir}{cmd}')
