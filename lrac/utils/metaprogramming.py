import inspect
from abc import ABCMeta
from types import ModuleType
from typing import List


def findSubclasses(module: ModuleType, abc: ABCMeta) -> List[ABCMeta]:
    subclasses = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, abc) and obj != abc:
            subclasses.append(obj)
    return subclasses
