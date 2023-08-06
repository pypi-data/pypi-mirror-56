import unittest
from kumaoche.config import DbConfig


class TestDbConfig(unittest.TestCase):
    def test_init(self):
        parsed_yaml = {
            'db': {
                'run': '0',
                'setup': '1',
                'update': '2',
                'env': {
                    'name': '2.0',
                    'work_dir': '2.1',
                    'run': '2.2',
                },
                'host': '3',
                'port': '4',
                'user': '5',
                'database': '6',
            }
        }
        config = DbConfig(parsed_yaml, 'db')
        self.assertEqual('0', config.run)
        self.assertEqual('1', config.setup)
        self.assertEqual('2', config.update)
        self.assertEqual('2.0', config.env.name)
        self.assertEqual('2.1', config.env.work_dir)
        self.assertEqual('2.2', config.env.run)
        self.assertEqual('3', config.host)
        self.assertEqual('4', config.port)
        self.assertEqual('5', config.user)
        self.assertEqual('6', config.database)

        config = DbConfig({}, 'db')
        self.assertEqual('', config.run)
        self.assertEqual('', config.setup)
        self.assertEqual('', config.update)
        self.assertEqual('', config.env.name)
        self.assertEqual('', config.env.work_dir)
        self.assertEqual('', config.env.run)
        self.assertEqual('', config.host)
        self.assertEqual('', config.port)
        self.assertEqual('', config.user)
        self.assertEqual('', config.database)



if __name__ == '__main__':
    unittest.main()
