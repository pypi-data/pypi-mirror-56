import unittest
from kumaoche.config import DockerConfig


class TestDockerConfig(unittest.TestCase):
    def test_init(self):
        parsed_yaml = {
            'docker': {
                'run': '0',
                'name': '1',
                'work_dir': '2',
                'container': '3',
                'ps': '4',
                'build': '5',
                'up': '6',
                'down': '7',
            }
        }
        config = DockerConfig(parsed_yaml, 'docker')
        self.assertEqual('0', config.run)
        self.assertEqual('1', config.name)
        self.assertEqual('2', config.work_dir)
        self.assertEqual('3', config.container)
        self.assertEqual('4', config.ps)
        self.assertEqual('5', config.build)
        self.assertEqual('6', config.up)
        self.assertEqual('7', config.down)

        config = DockerConfig({}, 'docker')
        self.assertEqual('', config.run)
        self.assertEqual('', config.name)
        self.assertEqual('', config.work_dir)
        self.assertEqual('', config.container)
        self.assertEqual('', config.ps)
        self.assertEqual('', config.build)
        self.assertEqual('', config.up)
        self.assertEqual('', config.down)


if __name__ == '__main__':
    unittest.main()
