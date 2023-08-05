# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Service(metaclass=ABCMeta):
    @abstractmethod
    def run(self, command: str):
        raise NotImplementedError()

    @abstractmethod
    def setup(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()
