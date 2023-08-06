from typing import List, Any

from dnry.config.section import ConfigSection
from dnry.config.helpers import merge
from dnry.config.types import IConfigFactory, IConfigSource, IConfigSection


class ConfigFactory(IConfigFactory):
    """Builds a single configuration section from a set of configuration sources.

    Configuration sources will be loaded and merged in order. If configuration sources
    collide key names, the value for the last source loaded containing the key will
    be used.

    You can override the merge behavior by providing your own implementation and setting it
    on ConfigurationFactory.merge.

    You can provide your own IConfigurationSection implementation by setting it on
    ConfigurationFactory.Section. Note: you must accept a single dict in __init__.
    """

    __explicit_configs: List[IConfigSection]
    __sources: List[IConfigSource]
    Section = ConfigSection
    merge = merge

    def __init__(self, sources: List[IConfigSource] = None):
        self.__explicit_configs = list()
        self.__sources = sources or list()

    def add_source(self, source: IConfigSource) -> None:
        self.__sources.append(source)

    def add_configuration(self, conf: IConfigSection):
        self.__explicit_configs.append(conf)

    def build(self) -> IConfigSection:
        context = {}
        for source in self.__sources:
            context = ConfigFactory.merge(context, source.load(self, ConfigFactory.Section(context)))
        for conf in self.__explicit_configs:
            context = ConfigFactory.merge(context, vars(conf))
        return ConfigFactory.Section(context)
