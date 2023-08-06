import json

try:
    import yaml
except ImportError:
    pass

try:
    import toml
except ImportError:
    pass

from os.path import splitext
from abconfig.common import Dict


class Reader(Dict):
    def __init__(self, obj: Dict):
        self._path = obj.get('__file__', False)
        if self._path != False:
            super().__init__(obj + self._read())
        else:
            super().__init__(obj)

    def _read(self) -> dict:
        try:
            with open(self._path, 'r') as fd:
                result = self._driver(fd)
                if not isinstance(result, (dict, Dict)):
                    raise IOError
                return result
        except Exception:
            return self.__mempty__

    def _driver(self, fd) -> dict:
        raise NotImplementedError

# Drivers:

class Yaml(Reader):
    __extensions__ = ('yml', 'yaml')

    def _driver(self, fd) -> dict:
        return yaml.load(fd, Loader=yaml.FullLoader)


class Json(Reader):
    __extensions__ = ('json',)

    def _driver(self, fd) -> dict:
        return json.load(fd)


class Toml(Reader):
    __extensions__ = ('toml',)

    def _driver(self, fd) -> dict:
        return toml.load(fd)


class File(Dict):
    __formats__ = (Json, Yaml, Toml)

    def __init__(self, obj: Dict):
        self._path = obj.get('__file__', False)
        if self._path != False:
            super().__init__(obj.do(*self._format()))
        else:
            super().__init__(obj)

    def _format(self) -> tuple:
        _, extension = splitext(self._path)
        for format_ in self.__formats__:
            for e in format_.__extensions__:
                if e == extension[1:]:
                    return (format_,)
        return self.__formats__
