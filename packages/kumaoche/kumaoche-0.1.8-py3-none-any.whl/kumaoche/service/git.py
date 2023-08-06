# -*- coding: utf-8 -*-

from ..config import GitConfig
from ..exec_env import ExecEnv
from .service import Service


class Git(Service):
    def __init__(self, env: ExecEnv, config: GitConfig):
        self.__env = env
        self.__config = config

    def run(self, command: str):
        repo_dir = self.__env.var_assign(self.__config.repo_dir)
        var_command = {'command': self.__env.var_assign(command)}

        return self.__env.run(self.__env.var_assign(self.__config.run, var_command), work_dir=repo_dir)

    def setup(self):
        return self.__env.run(self.__env.var_assign(self.__config.setup))

    def update(self):
        return self.__env.run(self.__env.var_assign(self.__config.update))
