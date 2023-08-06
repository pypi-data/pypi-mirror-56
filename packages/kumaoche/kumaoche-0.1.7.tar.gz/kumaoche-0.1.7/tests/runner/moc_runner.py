# -*- coding: utf-8 -*-

from kumaoche.runner import Runner


class MocRunner(Runner):
    @classmethod
    def run(cls, command: str):
        return command

    @classmethod
    def path_filter(cls, path: str):
        return path
