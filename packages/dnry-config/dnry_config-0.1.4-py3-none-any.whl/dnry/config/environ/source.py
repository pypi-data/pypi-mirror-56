import os

from dnry.config.helpers import explode
from dnry.config.types import IConfigSource, IConfigFactory, IConfigSection


class EnvironmentSource(IConfigSource):
    """Read configuration values from Environment Variables.

    Reads all environment variables available to the process
    that starts with the optional prefix.  Keys are split on '_'
    and used as section separators.

    Example:
        /* ENV_KEY="hello" */
        hello = conf.get("ENV:KEY")
    """
    def __init__(self, prefix: str = None):
        self.__prefix = prefix or ""

    def load(self, fact: IConfigFactory, conf: IConfigSection) -> dict:
        val = {
            key[len(self.__prefix):].lstrip('_'): value
            for key, value
            in os.environ.items()
            if key.startswith(self.__prefix)}
        return explode(val, "_")

