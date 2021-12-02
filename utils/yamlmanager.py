from os import stat

import yaml

class YamlManager:
    @staticmethod
    def read(type: str):
        with open("querylist.yaml", "r") as file:
            return yaml.safe_load(file)[type]

    def write(type: str, data: str):
        with open("querylist.yaml", "r") as file:
            yaml_data = yaml.safe_load(file)
            yaml_data[type].append(data)

        with open("querylist.yaml", "w", encoding='utf-8') as file:
            yaml.safe_dump(yaml_data, file, allow_unicode=True, sort_keys=False)

    def remove(type:str, data: str):
        with open("querylist.yaml", "r") as file:
            yaml_data = yaml.safe_load(file)
            yaml_data[type].remove(data)

        with open("querylist.yaml", "w", encoding='utf-8') as file:
            yaml.safe_dump(yaml_data, file, allow_unicode=True, sort_keys=False)
