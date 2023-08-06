from typing import Callable, Union

from dnry.config.types import IConfigSource, IConfigFactory, IConfigSection


class DelegateSource(IConfigSource):
    def __init__(self, delegate: Callable[[IConfigFactory], Union[dict, None]]):
        self.__delegate = delegate

    def load(self, fact: IConfigFactory, conf: IConfigSection) -> dict:
        return self.__delegate(fact, conf) or {}
