import ruamel.yaml
import typing
import voluptuous
from pathlib import Path

import EasyCo

yaml = ruamel.yaml.YAML(typ='rt')
yaml.default_flow_style = False
yaml.default_style = False
yaml.width = 1000000
yaml.allow_unicode = True
yaml.sort_base_mapping_type_on_output = False


class DelayedLoad:
    def __init__(self, filename: str):
        self.filename: str = filename
        self.data: typing.Union[list, dict]

    @classmethod
    def to_yaml(cls, representer, node):
        raise NotImplementedError()

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value)

    def load_data(self, folder: Path):
        path = folder / self.filename
        path = path.resolve().absolute()



class Include(DelayedLoad):
    yaml_tag = '!include'

yaml.register_class(Include)


class SimpleYamlFile:
    def __init__(self, path: Path):
        self.path = path

    def load(self):
        with self.path.open(mode='r', encoding='utf-8') as f:
            erg = yaml.load(f)

        self.__delayed_load(erg)

    def __delayed_load(self, data: typing.Union[list, dict]):
        if isinstance(data, dict):
            for k, v in data.items():
                self.__delayed_load(v)
        elif isinstance(data, (list, set, tuple, frozenset)):
            for k in data:
                self.__delayed_load(data)
        elif isinstance(data, DelayedLoad):
            data.load_data(self.path.parent)


def load(file: Path):
    with file.open(mode='r', encoding='utf-8') as f:
        erg = yaml.load(f)

    print(erg)

f = SimpleYamlFile(Path(r'z:\Python\EasyCo\tests\test_files\test_merge.yml'))
f.load()