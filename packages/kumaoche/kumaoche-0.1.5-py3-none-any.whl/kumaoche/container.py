# -*- coding: utf-8 -*-

from .config import ConfigParser, ServiceConfig
from .exec_env import DisableEnv, Shell, Docker
from .service import Git, DB, PackageManager
from .runner import InvokeRunner


class Container(object):
    def __init__(self, role: str):
        config = ConfigParser.find(role)

        self.name = config.git.repo
        self.shell = Shell(config.shell, config.variable, InvokeRunner)
        self.docker = Docker(config.docker, config.variable, InvokeRunner)

        self.git = Git(self.env(config.git, config.variable), config.git)
        self.db = DB(self.env(config.db, config.variable), config.db)
        self.php = PackageManager(self.env(config.php, config.variable), config.php)
        self.ruby = PackageManager(self.env(config.ruby, config.variable), config.ruby)
        self.node = PackageManager(self.env(config.node, config.variable), config.node)

        self.package_managers = [
            self.php,
            self.ruby,
            self.node
        ]

    @staticmethod
    def env(config: ServiceConfig, variable: {}):
        if config.env.name == 'shell' and config.env.work_dir != '':
            return Shell(config.env, variable, InvokeRunner)
        elif config.env.name == 'docker' and config.env.work_dir != '':
            return Docker(config.env, variable, InvokeRunner)
        else:
            return DisableEnv()

    @classmethod
    def all_role_names(cls):
        return ConfigParser.all_roles()
