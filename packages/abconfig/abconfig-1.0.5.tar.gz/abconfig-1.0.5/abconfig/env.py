from os import environ

try:
    import hvac
except ImportError:
    pass

from abconfig.common import Dict


class Environment(Dict):
    def __init__(self, obj: Dict):
        super().__init__(obj + self._read(obj, obj.get('__prefix__', None)))

    def _read(self, obj: Dict, prefix: str) -> Dict:
        return Dict([self._env(prefix,k,v) for k,v in obj.items()])

    def _env(self, prefix: str, k: str, v: any) -> tuple:
        if self.is_dict(v):
            return (k, self._read(v, self._prefix(prefix,k)))
        else:
            return (k, environ.get(self._prefix(prefix, k).upper(), None))

    def _prefix(self, *args: [str]):
        return '_'.join(filter(lambda x: True if x else False, args))

    @staticmethod
    def _enabled(obj: Dict):
        return obj.get('__env__', True)


class Vault(Environment):
    __config = Dict(
        type='json',
        kv_version=2,
        addr='127.0.0.1:8200',
        token=str,
        path=str
    )

    def __init__(self, obj: Dict):
        self._config = self.__config + obj.get('__vault__')
        self._cache = self._request
        if self._config['type'] == 'kv':
            super().__init__(obj + self._read(obj, obj.get('__prefix__')))
        elif self._config['type'] == 'json':
            super().__init__(obj + self._cache)
        else:
            raise ValueError(f'only supported "kv" or "json"')

    def _env(self, prefix: str, k: str, v: any) -> tuple:
        key = k if k != '__vault__' else 'vault'
        if self.is_dict(v):
            return (key, self._read(v, self._prefix(prefix,key)))
        else:
            return (key, self._cache.get(self._prefix(prefix, key).upper(), None))

    @property
    def _request(self) -> dict:
        client = hvac.Client(
            url=self._config['addr'],
            token=self._config['token']
        ).secrets.kv

        if self._config['kv_version'] == 2:
            return client.v2.read_secret_version(
                path=self._config['path']
            )['data']['data']
        elif self._config['kv_version'] == 1:
            return client.v1.read_secret(
                path=self._config['path']
            )['data']
        else:
            return dict()

    @staticmethod
    def _enabled(obj: Dict):
        return Dict.is_dict(obj.get('__vault__'))


class Types(Dict):
    def __init__(self, obj: Dict):
        super().__init__(
            obj._fmap(
                lambda k,v:
                    (k, Types(Dict(v)))
                    if self.is_dict(v) else
                    (k, None if isinstance(v, type) else v)
            )
        )


class Switch(type):
    def __call__(cls, obj: Dict) -> Dict:
        do = [s for s in cls.__sources__ if s._enabled(obj)]
        return (obj.do(*do) if do else obj).bind(Types)


class Env(metaclass=Switch):
    __sources__ = (Environment, Vault)
