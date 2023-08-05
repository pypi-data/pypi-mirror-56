# -*- coding: utf-8 -*-


class ExecEnvConfig(object):
    def __init__(self, parsed_yaml: {}, key: str):
        configs = parsed_yaml.get(key, {})

        self.name = configs.get('name', '')
        self.work_dir = configs.get('work_dir', '')
        self.run = configs.get('run', '')
