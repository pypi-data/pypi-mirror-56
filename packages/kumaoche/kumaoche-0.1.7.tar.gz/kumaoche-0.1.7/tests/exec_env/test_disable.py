# -*- coding: utf-8 -*-

import unittest
from kumaoche.exec_env import DisableEnv
from ..config import StubConfig


class TestShell(unittest.TestCase):
    def setUp(self):
        self.config = StubConfig.find('variable_assign_test_role')
        self.env = DisableEnv()
        self.src_text = 'git_host:{git_host},git_org:{git_org},git_repo:{git_repo},db_host:{db_host},db_port:{db_port},db_user:{db_user},db_database:{db_database}'
        self.dst_text = 'git_host:github.com,git_org:kumak1,git_repo:kumaoche,db_host:db,db_port:3306,db_user:root,db_database:db'

    def test_run(self):
        self.assertEqual(None, self.env.run(self.src_text))

    def test_var_assign(self):
        self.assertEqual(self.src_text, self.env.var_assign(self.src_text))

    def test_name(self):
        self.assertEqual("disable", self.env.name())


if __name__ == '__main__':
    unittest.main()
