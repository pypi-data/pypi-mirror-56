import unittest
from kumaoche.config import StringBuilderConfig


class TestStringBuilderConfig(unittest.TestCase):
    def test_init(self):
        parsed_yaml = {
            'string_builder': {
                'run': '0',
                'name': '1',
                'work_dir': '2',
            }
        }
        config = StringBuilderConfig(parsed_yaml, 'string_builder')
        self.assertEqual('0', config.run)
        self.assertEqual('1', config.name)
        self.assertEqual('2', config.work_dir)

        config = StringBuilderConfig({}, 'string_builder')
        self.assertEqual('', config.run)
        self.assertEqual('', config.name)
        self.assertEqual('', config.work_dir)


if __name__ == '__main__':
    unittest.main()
