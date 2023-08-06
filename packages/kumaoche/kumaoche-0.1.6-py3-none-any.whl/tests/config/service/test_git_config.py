import unittest
from kumaoche.config import GitConfig


class TestGitConfig(unittest.TestCase):
    def test_init(self):
        parsed_yaml = {
            'git': {
                'run': '0',
                'setup': '1',
                'update': '2',
                'env': {
                    'name': '2.0',
                    'work_dir': '2.1',
                    'run': '2.2',
                },
                'repo_dir': '3',
            }
        }
        config = GitConfig(parsed_yaml, 'git')
        self.assertEqual('0', config.run)
        self.assertEqual('1', config.setup)
        self.assertEqual('2', config.update)
        self.assertEqual('2.0', config.env.name)
        self.assertEqual('2.1', config.env.work_dir)
        self.assertEqual('2.2', config.env.run)
        self.assertEqual('3', config.repo_dir)

        config = GitConfig({}, 'git')
        self.assertEqual('', config.run)
        self.assertEqual('', config.setup)
        self.assertEqual('', config.update)
        self.assertEqual('', config.env.name)
        self.assertEqual('', config.env.work_dir)
        self.assertEqual('', config.env.run)
        self.assertEqual('', config.repo_dir)



if __name__ == '__main__':
    unittest.main()
