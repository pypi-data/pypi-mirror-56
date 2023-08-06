from .base import *
from .business import *
from .data import *
from .system import *


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [
            leaf_cls
            for sub_cls in cls.__subclasses__()
            for leaf_cls in all_subclasses(sub_cls)
        ]
    )


ERRORS = {
    cls.code: cls
    for cls in all_subclasses(GizwitsException)
}
