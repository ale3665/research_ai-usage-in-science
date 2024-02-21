import inspect
from abc import ABCMeta
from types import ModuleType
from typing import Any, List, Protocol


def findSubclasses(module: ModuleType, protocol: Any) -> List[Any]:
    """
    This method can identify if a class in a module adhears to a defined
    Protocol class.

    It returns a list of instantied classes that do adhear to the Protocol.
    """
    subclasses = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj != protocol:
            try:
                tempObj: Any = obj()
            except TypeError:
                continue
            else:
                if isinstance(tempObj, protocol):
                    subclasses.append(tempObj)
                else:
                    del tempObj

    return subclasses
