from os import environ

from abconfig.common import Dict


class DefaultType(Dict):
    """ Replaces type objects remaining after processing with None. """

    def __init__(self, obj: Dict):
        super().__init__(
            obj._fmap(lambda k,v:
                (k, DefaultType(v))
                if isinstance(v, (dict, Dict)) else
                (k, None if isinstance(v, type) else v)
            )
        )


class Environment(Dict):
    def __init__(self, obj: Dict):
        prefix = obj.pop('__prefix__', None)
        if obj.pop('__env__', True) != None:
            super().__init__(obj + self._read(obj, prefix))
        else:
            super().__init__(obj)

    def _read(self, obj: Dict, prefix: str) -> Dict:
        return Dict([self._env(prefix,k,v) for k,v in obj.items()])

    def _env(self, prefix: str, k: str, v: any) -> tuple:
        if isinstance(v, (dict, Dict)):
            return (k, self._read(v, self._prefix(prefix,k)))
        else:
            return (k, environ.get(self._prefix(prefix, k).upper(), None))

    def _prefix(self, *args: [str]):
        return '_'.join(filter(lambda x: True if x else False, args))


class Env(Dict):
    __envnd__ = (Environment, DefaultType)

    def __init__(self, obj: Dict):
        super().__init__(obj._do(*self.__envnd__))