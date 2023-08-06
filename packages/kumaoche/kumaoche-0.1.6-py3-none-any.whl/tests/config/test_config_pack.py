import unittest
from kumaoche.config import ConfigPack


class TestShellConfig(unittest.TestCase):
    def test_init(self):
        parsed_yaml = {
            'variable': {'key': 'value'},
            'string_builder': {'name': '1'},
            'shell': {'name': '2'},
            'docker': {'name': '3'},
            'git': {'run': '100'},
            'db': {'run': '101'},
            'php': {'run': '102'},
            'ruby': {'run': '103'},
            'node': {'run': '104'},
        }
        config = ConfigPack(parsed_yaml)
        self.assertEqual({'key': 'value'}, config.variable)
        self.assertEqual('1', config.string_builder.name)
        self.assertEqual('2', config.shell.name)
        self.assertEqual('3', config.docker.name)
        self.assertEqual('100', config.git.run)
        self.assertEqual('101', config.db.run)
        self.assertEqual('102', config.php.run)
        self.assertEqual('103', config.ruby.run)
        self.assertEqual('104', config.node.run)

        config = ConfigPack({})
        self.assertEqual({}, config.variable)
        self.assertEqual('', config.string_builder.name)
        self.assertEqual('', config.shell.name)
        self.assertEqual('', config.docker.name)
        self.assertEqual('', config.git.run)
        self.assertEqual('', config.db.run)
        self.assertEqual('', config.php.run)
        self.assertEqual('', config.ruby.run)
        self.assertEqual('', config.node.run)


if __name__ == '__main__':
    unittest.main()
