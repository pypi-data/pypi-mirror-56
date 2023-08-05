# -*- coding: utf-8 -*-

from invoke import run
from .runner import Runner


class InvokeRunner(Runner):
    @classmethod
    def run(cls, command: str):
        return run(command, echo=True, pty=True)

    @classmethod
    def path_filter(cls, path: str):
        return run(f"echo '{path}'", hide=True).stdout.splitlines()[-1]
