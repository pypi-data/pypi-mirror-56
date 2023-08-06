import unittest
import os

from kumaoche.config import ConfigParser


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.file_path_list = [os.path.dirname(__file__) + '/stub_config.yml']

    def test_all_roles(self):
        self.assertEqual(['variable_assign_test_role', 'empty_role'], ConfigParser.all_roles(self.file_path_list))

    def test_find(self):
        ConfigParser.find('empty_role', self.file_path_list)

if __name__ == '__main__':
    unittest.main()
