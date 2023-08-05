# -*- coding: utf-8 -*-

from .exec_env import ExecEnv


class DisableEnv(ExecEnv):
    def name(self):
        return 'disable'

    def assign_variables(self):
        return {}

    def run(self, command: str):
        return
