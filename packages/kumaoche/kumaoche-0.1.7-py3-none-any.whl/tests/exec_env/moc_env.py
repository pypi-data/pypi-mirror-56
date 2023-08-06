# -*- coding: utf-8 -*-

from kumaoche.exec_env.exec_env import ExecEnv


class MocEnv(ExecEnv):
    def __init__(self, variable: {}):
        self.__default_var = variable

    def name(self):
        return ''

    def var_assign(self, text: str, append_var=None):
        if append_var is None:
            append_var = {}

        if len(self.__default_var) + len(append_var) > 0:
            return text.format(**self.__default_var, **append_var)

        return text

    def run(self, command: str, work_dir=''):
        return f'work_dir:{work_dir},command:{command}'
