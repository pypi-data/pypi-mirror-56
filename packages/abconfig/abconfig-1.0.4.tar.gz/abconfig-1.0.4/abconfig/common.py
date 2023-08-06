from collections import UserDict


class Item:
    """ Converting an item type to type from a related subset of types. """

    __mempty__ = None
    __types__ = ([int, float, str, bool], [list, tuple, set, frozenset])

    def __init__(self, item: any):
        if item != self.__mempty__:
            self._type = self._detect_type(item)
            self._set = [s for s in self.__types__ if self._type in s][0]
        self.data = item

    def _detect_type(self, item: any) -> type:
        return item if isinstance(item, type) else type(item)

    def __add__(self, operand: any) -> any:
        """ Converting the type of second operand to type of the first operand.
        Values ​​are not sum, the first operand will be replaced by the second.
        When trying to convert an element type to a type that belongs another subset
        is thrown TypeError is raised. For example, you cannot convert a list, tuple and
        set to bool or string, a string cannot be converted to a list, tuple or set.
        This is different from the default behavior in Python. """
        if self.data == self.__mempty__:
            return operand
        elif operand == self.__mempty__ or isinstance(operand, type):
            return self.data
        elif not self._detect_type(operand) in self._set:
            raise TypeError
        else:
            return self._type(operand)


class Dict(UserDict):
    """ Wrapper to build a dictionary processing chain.

    (+) - atomic update values ​​of the first dictionary
    to values ​​from second dictionary with support recursive processing
    nested dictionaries.
    """

    __mempty__ = dict()

    def _fmap(self, f: type) -> dict:
        """ Applies function to each pair of key values ​​in dict. """
        return Dict([f(k,v) for k,v in self.items()])

    def _bind(self, f: dict) -> dict:
        """ Applies function to object. """
        return f(self)

    def do(self, *args: [dict]) -> dict:
        acc = args[0](self)
        for obj in args[1:]:
            acc = acc._bind(obj)
        return acc

    def __add__(self, operand: dict) -> dict:
        if operand == self.__mempty__:
            return self.data
        elif self.data == self.__mempty__:
            return operand

        return self._fmap(lambda k,v:
            (k, Dict(v) + operand.get(k, self.__mempty__))
            if isinstance(v, (dict, Dict)) else
            (k, Item(v) + operand.get(k, Item.__mempty__))
        )
