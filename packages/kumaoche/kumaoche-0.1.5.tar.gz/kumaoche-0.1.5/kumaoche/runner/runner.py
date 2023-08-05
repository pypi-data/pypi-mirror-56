# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Runner(metaclass=ABCMeta):
    @abstractmethod
    def run(self, command: str):
        raise NotImplementedError()

    @abstractmethod
    def path_filter(self, path: str):
        raise NotImplementedError()
