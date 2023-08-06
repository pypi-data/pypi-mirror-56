import unittest
from kumaoche.config import ShellConfig


class TestShellConfig(unittest.TestCase):
    def test_init(self):
        parsed_yaml = {
            'shell': {
                'run': '0',
                'name': '1',
                'work_dir': '2',
            }
        }
        config = ShellConfig(parsed_yaml, 'shell')
        self.assertEqual('0', config.run)
        self.assertEqual('1', config.name)
        self.assertEqual('2', config.work_dir)

        config = ShellConfig({}, 'shell')
        self.assertEqual('', config.run)
        self.assertEqual('', config.name)
        self.assertEqual('', config.work_dir)


if __name__ == '__main__':
    unittest.main()
