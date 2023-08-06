from dnry.config.types import IConfigSource, IConfigFactory, IConfigSection


class InMemorySource(IConfigSource):
    """Read configuration values from a dictionary"""
    def __init__(self, data: dict):
        self.__data = data

    def load(self, fact: IConfigFactory, conf: IConfigSection) -> dict:
        return self.__data
