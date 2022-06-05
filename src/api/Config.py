import toml

import src.api.Utils as Utils


class Config:
    data: dict

    def __init__(self, file):
        self.load(file)

    def load(self, file: str):
        self.data = toml.load(Utils.get_dir() + file)

    def get(self, path: str):
        keys = path.split('.')

        current_node = self.data
        for key in keys:
            current_node = current_node.get(key)

        return current_node
