from typing import List

from dnry.config.helpers import explode
from dnry.config.types import IConfigSource, IConfigFactory, IConfigSection
from argparse import ArgumentParser


class ArgumentSource(IConfigSource):
    """Read configuration values from an argparse.ArgumentParser object."""
    def __init__(self, argument_parser: ArgumentParser, argv: List[str] = None):
        self.__argv = argv
        self.__ap = argument_parser

    def load(self, fact: IConfigFactory, conf: IConfigSection) -> dict:
        opts = self.__ap.parse_args(self.__argv)
        return explode(vars(opts))
