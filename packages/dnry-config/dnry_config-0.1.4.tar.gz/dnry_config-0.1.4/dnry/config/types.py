from abc import ABC, abstractmethod
from typing import Union


class IConfigSection(ABC):
    @abstractmethod
    def get(self, key: str) -> any:
        raise NotImplemented()

    @abstractmethod
    def get_section(self, key: str) -> Union["IConfigSection", None]:
        raise NotImplemented()

    @abstractmethod
    def has(self, key: str) -> bool:
        raise NotImplemented()


class IConfigSource(ABC):
    @abstractmethod
    def load(self, fact: "IConfigFactory", conf: IConfigSection) -> dict:
        raise NotImplemented()


class IConfigFactory(ABC):
    @abstractmethod
    def add_source(self, source: IConfigSource) -> None:
        raise NotImplemented()

    @abstractmethod
    def build(self) -> IConfigSection:
        raise NotImplemented()

    @abstractmethod
    def add_configuration(self, conf: IConfigSection):
        raise NotImplemented()
