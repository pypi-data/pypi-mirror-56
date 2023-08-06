from os import environ

try:
    import hvac
except ImportError:
    pass

from abconfig.common import Dict


class Environment(Dict):
    def __init__(self, obj: Dict):
        prefix = obj.get('__prefix__', None)
        if obj.get('__env__', True) != None:
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


class Vault(Environment):
    _config = dict(
        addr=str,
        token=str,
        path=str,
        kv_version='2'
    )

    _types = ('kv','json')

    def __init__(self, obj: Dict):
        prefix = obj.get('__prefix__', None)
        current = obj.get('__vault__', None)
        self._secrets = self._request(obj) if current in self._types else dict()
        if current == self._types[0]:
            super().__init__(obj + self._read(obj, prefix))
            self._hideconfig(obj)
        elif current == self._types[1]:
            super().__init__(obj + self._request(obj))
            self._hideconfig(obj)
        else:
            super().__init__(obj)

    def _hideconfig(self, obj: Dict) -> None:
        if obj.get('__hidesettings__', True) == True:
            self.pop('vault')

    def _env(self, prefix: str, k: str, v: any) -> tuple:
        if isinstance(v, (dict, Dict)):
            return (k, self._read(v, self._prefix(prefix,k)))
        else:
            return (k, self._secrets.get(self._prefix(prefix, k).upper(), None))

    def _request(self, obj: Dict) -> dict:
        config = (Dict(vault=self._config) + obj)['vault']
        client = hvac.Client(url=config['addr'],token=config['token']).secrets.kv
        if config['kv_version'] == '2':
            return client.v2.read_secret_version(path=config['path'])['data']['data']
        else:
            return client.v1.read_secret(path=config['path'])['data']


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


class Env(Dict):
    def __init__(self, obj: Dict):
        super().__init__(obj.do(Environment, Vault, DefaultType))
