import yaml
from typing import Union, List
from os.path import exists
from dnry.config.types import IConfigSource, IConfigFactory, IConfigSection


class YamlSource(IConfigSource):
    """Read configuration values from a yaml file."""
    def __init__(self, path: Union[str, List[str]], required: bool = True, **kwargs):
        self.__paths = path if isinstance(path, list) else [path]
        self.__required = required
        self.__loader = kwargs.get("loader", yaml.SafeLoader)

    def load(self, fact: IConfigFactory, conf: IConfigSection) -> dict:
        path = self.__get_first_existing_path()
        if path is None and self.__required:
            paths = ",".join(self.__paths)
            raise RuntimeError(f"Configuration Error: None of these paths could be found: {paths}")

        elif path is None and not self.__required:
            return dict()

        with open(path, 'r') as f:
            return yaml.load(f, Loader=self.__loader) or dict()

    def __get_first_existing_path(self) -> Union[str, None]:
        try:
            return next(p for p in self.__paths if exists(p))
        except StopIteration:
            return None
