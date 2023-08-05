__version__ = '1.0.2'

from abconfig.common import Dict
from abconfig.file import File
from abconfig.env import Env


class GetAttrs(Dict):
    """ Class attribute reader. """

    __settings__ = ('__prefix__','__env__','__file__')

    def __init__(self, obj: Dict):
        super().__init__({
            str(i): getattr(obj, i) for i in type(obj).__dict__.keys()
            if (i[:1] != '_' or i in self.__settings__)
        })


class ABConfig(Dict):
    """ Abstract base class. """

    __prefix__  = None
    __env__     = True
    __file__    = False

    __sources__ = (GetAttrs, File, Env)

    def __init__(self):
        if str(type(self).__name__) == 'ABConfig':
            raise NotImplementedError

        super().__init__(self._do(*self.__sources__))
        self.__dict__.update(self)
