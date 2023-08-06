import unittest
from kumaoche.config import PackageManagerConfig


class TestPackageManagerConfig(unittest.TestCase):
    def test_init(self):
        parsed_yaml = {
            'php': {
                'run': '0',
                'setup': '1',
                'update': '2',
                'env': {
                    'name': '2.0',
                    'work_dir': '2.1',
                    'run': '2.2',
                },
                'test': '3',
            }
        }
        config = PackageManagerConfig(parsed_yaml, 'php')
        self.assertEqual('0', config.run)
        self.assertEqual('1', config.setup)
        self.assertEqual('2', config.update)
        self.assertEqual('2.0', config.env.name)
        self.assertEqual('2.1', config.env.work_dir)
        self.assertEqual('2.2', config.env.run)
        self.assertEqual('3', config.test)

        config = PackageManagerConfig({}, 'php')
        self.assertEqual('', config.run)
        self.assertEqual('', config.setup)
        self.assertEqual('', config.update)
        self.assertEqual('', config.env.name)
        self.assertEqual('', config.env.work_dir)
        self.assertEqual('', config.env.run)
        self.assertEqual('', config.test)


if __name__ == '__main__':
    unittest.main()
