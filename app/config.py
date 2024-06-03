import json
from configdict import ConfigDict


class Config:
    def __init__(self):
        self._config_dict = None

    def init(self, filename: str):
        with open(filename) as f:
            json_content = json.load(f)
            self._config_dict = ConfigDict("config", json_content)

    def get_config(self):
        return self._config_dict


config_manager = Config()


def get_config():
    return config_manager.get_config()
