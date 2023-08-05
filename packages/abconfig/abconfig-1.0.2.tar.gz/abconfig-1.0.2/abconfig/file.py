import json

try:
    import yaml
except ImportError:
    pass

try:
    import toml
except ImportError:
    pass

from os import environ
from abconfig.common import Dict
from typing import IO, Type


class Reader(Dict):
    def __init__(self, x: Type[Dict]):
        self.x = x
        file_path = self.x.get('__file__', False)
        if file_path != False:
            super().__init__(x + self._read(file_path))
        else:
            super().__init__(x)

    def _read(self, file_path: str):
        try:
            with open(file_path, 'r') as fd:
                read = self._reader(fd)
                if not isinstance(read, (dict, Dict)):
                    raise IOError
                self.x.pop('__file__', False)
                return read
        except Exception:
            return self.__mempty__

    def _reader(self, fd: IO[str]):
        raise NotImplementedError


class Yaml(Reader):
    def _reader(self, fd: IO[str]):
        return yaml.load(fd, Loader=yaml.FullLoader)


class Json(Reader):
    def _reader(self, fd: IO[str]):
        return json.load(fd)


class Toml(Reader):
    def _reader(self, fd: IO[str]):
        return toml.load(fd)


class File(Dict):
    __formats__ = (Json, Yaml, Toml)

    def __init__(self, obj: Dict):
        super().__init__(obj._do(*self.__formats__))