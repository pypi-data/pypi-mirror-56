# -*- coding: utf-8 -*-

from .exec_env import ExecEnv


class DisableEnv(ExecEnv):
    def name(self):
        return 'disable'

    def var_assign(self, text: str, append_var=None):
        return text

    def run(self, command: str, work_dir=''):
        return
