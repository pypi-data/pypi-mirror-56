# -*- coding: utf-8 -*-

import unittest
from kumaoche.service import DB
from ..exec_env import MocEnv
from ..config import StubConfig


class TestDb(unittest.TestCase):
    def setUp(self):
        self.config = StubConfig.find('variable_assign_test_role')
        self.empty_config = StubConfig.find('empty_role')
        self.env = MocEnv(self.config.variable)
        self.db = DB(self.env, self.config.db)
        self.empty_db = DB(self.env, self.empty_config.db)
        self.src_text = 'git_host:{git_host},git_org:{git_org},git_repo:{git_repo},db_host:{db_host},db_port:{db_port},db_user:{db_user},db_database:{db_database}'
        self.dst_text = 'git_host:github.com,git_org:kumak1,git_repo:kumaoche,db_host:db,db_port:3306,db_user:root,db_database:db'

    def test_run(self):
        self.assertEqual(f"work_dir:,command:db run test_command", self.db.run("test_command"))
        self.assertEqual(f"work_dir:,command:db run {self.dst_text}", self.db.run(self.src_text))
        self.assertEqual(f"work_dir:,command:", self.empty_db.run(self.src_text))

    def test_setup(self):
        self.assertEqual(f"work_dir:,command:db setup {self.dst_text}", self.db.setup())
        self.assertEqual(f"work_dir:,command:", self.empty_db.setup())

    def test_update(self):
        self.assertEqual(f"work_dir:,command:db update {self.dst_text}", self.db.update())
        self.assertEqual(f"work_dir:,command:", self.empty_db.update())


if __name__ == '__main__':
    unittest.main()
