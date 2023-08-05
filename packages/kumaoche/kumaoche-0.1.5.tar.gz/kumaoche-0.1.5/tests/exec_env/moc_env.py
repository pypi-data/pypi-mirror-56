# -*- coding: utf-8 -*-

from kumaoche.exec_env.exec_env import ExecEnv


class MocEnv(ExecEnv):
    def name(self):
        return ''

    def assign_variables(self):
        return ''

    def run(self, command: str):
        return command
