__version__ = '1.0.5'

from abconfig.common import Dict
from abconfig.file import File
from abconfig.env import Env


class GetAttrs(Dict):
    __settings__ = (
        '__hidesettings__',
        '__prefix__',
        '__env__',
        '__file__',
        '__vault__'
    )

    def __init__(self, obj: Dict):
        super().__init__({
            str(k): v for k,v in type(obj).__dict__.items()
            if k[:1] != '_' or k in self.__settings__
        })


class HideSettings(Dict):
    def __init__(self, obj:Dict):
        if obj.get('__hidesettings__'):
            for k,_ in dict(obj).items():
                if k in GetAttrs.__settings__:
                    obj.pop(k)
        super().__init__(obj)


class ABConfig(Dict):
    __hidesettings__ = True
    __prefix__       = None
    __env__          = True
    __file__         = False
    __vault__        = False

    __sources__      = (File, Env)

    def __init__(self, obj=None):
        if str(type(self).__name__) == 'ABConfig':
            raise NotImplementedError

        super().__init__(
            GetAttrs(obj if obj else self)
                .do(*self.__sources__)
                .bind(HideSettings)
        )

        self.__dict__.update(self)
