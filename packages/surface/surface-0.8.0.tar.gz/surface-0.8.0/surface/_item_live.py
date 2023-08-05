""" Wrapping live objects """

if False:  # type checking
    from typing import *

import sys
import enum
import inspect
import typing
import logging
import traceback

from surface._base import PY2
from surface._utils import FuncSig, FuncSigArg, Cache
from surface._type import LiveType, FuncType, Context, AnnotationType, BUILTIN_TYPES

from surface._item import Item

LOG = logging.getLogger(__name__)


class ErrorItem(Item):
    """ Special Item to represent errors attained from unreachable items. """

    __slots__ = ("type", "trace")

    def __new__(cls, parent=None):  # type: (Optional[Any]) -> ErrorItem
        err_type, err_val, _ = sys.exc_info()
        scope = super(ErrorItem, cls).__new__(cls, [], err_val, parent)  # type: Any
        scope.type = err_type
        scope.trace = traceback.format_exc()
        LOG.debug(scope.trace)  # Alert us of this error
        return scope


class LiveItem(Item):
    """ Wrap and traverse live objects """

    __slots__ = []  # type: ignore
    _cache = Cache()

    @classmethod
    def wrap(cls, visitors, item, parent=None):
        item_id = id(item)
        cache_item = cls._cache.get(item_id, None)
        if cache_item is None:
            cls._cache[item_id] = cache_item = super(LiveItem, cls).wrap(
                visitors, item, parent
            )
        return cache_item

    def __getitem__(self, name):  # type: (str) -> Item
        """ We can get errors while traversing. Keep them. """
        try:
            return super(LiveItem, self).__getitem__(name)
        except Exception:
            return ErrorItem(self)

    @property
    def name(self):
        return getattr(self.item, "__name__", "")

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)


class ModuleItem(LiveItem):
    """ Wrap live module objects """

    __slots__ = []  # type: ignore

    ALL_FILTER = False

    _child_filter = set(id(_v) for _v in typing.__dict__.values())
    _child_filter.add(id(typing))

    @classmethod
    def is_this_type(cls, item, parent):
        return inspect.ismodule(item)

    def get_child(self, attr):
        return getattr(self.item, attr)

    def get_children_names(self):
        if self.name in sys.builtin_module_names:
            return []  # Don't bother traversing built in stuff...
        names = (
            name
            for name, item in self.item.__dict__.items()
            if name and not name.startswith("_") and not id(item) in self._child_filter
        )
        if self.ALL_FILTER:
            try:
                all_filter = self.item.__all__
            except AttributeError:
                pass
            else:
                names = (name for name in names if name in all_filter)

        return sorted(names)

    def get_type(self):
        return getattr(self.item, "__name__", "")


class ClassItem(LiveItem):
    """ Wrap live class objects """

    __slots__ = []  # type: ignore

    magic_methods = tuple("__{}__".format(_m) for _m in ("new", "init", "call"))

    @staticmethod
    def is_this_type(item, parent):
        return inspect.isclass(item)

    def get_children_names(self):
        names = [name for name in sorted(dir(self.item)) if not name.startswith("_")]
        for attr in self.magic_methods:
            if hasattr(self.item, attr) and FunctionItem.is_this_type(
                getattr(self.item, attr), self
            ):
                names.append(attr)
        return names

    def get_child(self, attr):
        return getattr(self.item, attr)

    def get_type(self):
        module = getattr(inspect.getmodule(self.item), "__name__", "")
        name = getattr(self.item, "__qualname__", "") or getattr(
            self.item, "__name__", ""
        )
        if module and name:
            return "{}.{}".format(module, name)
        return name


class VarItem(LiveItem):
    """ Wrap variable. Fallback. """

    __slots__ = []  # type: ignore
    EMPTY = object()

    @staticmethod
    def is_this_type(item, parent):
        return True

    def get_type(self):
        annotation = getattr(self.parent, "__annotations__", {}).get(
            self.name, self.EMPTY
        )
        if annotation is self.EMPTY:
            return str(LiveType(self.item))
        context = Context(getattr(inspect.getmodule(self.item), "__dict__", {}))
        return AnnotationType(annotation, context).type


class BuiltinItem(LiveItem):
    """ Wrap builtin. """

    __slots__ = []  # type: ignore

    @staticmethod
    def is_this_type(item, parent):
        for builtin_type in BUILTIN_TYPES:
            if item is builtin_type:
                return True
        return False

    def get_type(self):
        return self.item.__name__


class EnumItem(LiveItem):
    """ Wrap enum. """

    __slots__ = []  # type: ignore

    @staticmethod
    def is_this_type(item, parent):
        return isinstance(item, enum.Enum)

    def get_type(self):
        return str(LiveType(self.item.value))

    @property
    def name(self):
        return self.item.name


class NoneItem(LiveItem):
    """ Wrap None. """

    __slots__ = []  # type: ignore

    @staticmethod
    def is_this_type(item, parent):
        return item is None


class FunctionItem(LiveItem):
    """ Wrap function / method """

    __slots__ = []  # type: ignore

    @staticmethod
    def is_this_type(item, parent):
        return inspect.isfunction(item) or inspect.ismethod(item)

    def get_child(self, attr):
        sig = FuncSig(self.item)
        return sig.parameters[attr]

    def get_children_names(self):
        sig = FuncSig(self.item)
        if not sig:
            return []

        params = list(sig.parameters.keys())

        if isinstance(self.parent, ClassItem):
            # We want to ignore "self" and "cls", as those are implementation details
            # and are not relevant for API comparisons
            # It seems funcsigs removes "cls" for us in class methods... that is nice.
            if self.is_method:
                params = params[1:]  # chop off self
        return params

    def get_return_type(self,):
        func_type = FuncType(self.item)
        return func_type.returns

    @property
    def is_method(self):
        """ Check if function is a method (also not staticmethod or classmethod) """
        if not isinstance(self.parent, ClassItem):
            return False
        name = self.name
        for parent in inspect.getmro(self.parent.item):
            dct = getattr(parent, "__dict__", {})
            if name not in dct:
                continue
            func = dct[name]
            if isinstance(func, (staticmethod, classmethod)):
                return name == "__new__"
            break
        return True


class ParameterItem(LiveItem):
    """ Wrap function parameter """

    __slots__ = []  # type: ignore

    @staticmethod
    def is_this_type(item, parent):
        return isinstance(item, FuncSigArg)

    def get_type(self):
        func_type = FuncType(self.parent.item)
        return func_type.params[self.item.name]

    def get_kind(self):
        return self.item.kind
