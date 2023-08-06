import os
from pathlib import Path
from typing import List

from omegaconf import OmegaConf
from omegaconf.config import Config
from omegaconf.omegaconf import decode_primitive

from flubber.contrib.utils import get_flubber_path


def env(key, default):
    try:
        return decode_primitive(os.getenv(key, default))
    except KeyError:
        raise KeyError("Environment variable '{}' not found".format(key))


class SettingsObject:
    def __init__(self, path: str = "", files: List[str] = []):
        self.path = path
        self.files = files

    @property
    def flubber_settings(self) -> str:
        flubber_settings = Path(get_flubber_path()) / Path("contrib/settings/conf.yaml")
        return str(flubber_settings)

    def _clean_resolvers(self) -> None:
        Config._resolvers = {}

    def add_resolvers(self, resolvers: List[object]) -> None:
        """
        Add resolvers to settings parsing
        :param resolvers: List of list of resolvers where first element is the resolver name and the second is
        the resolver function.
        :return: None
        """
        for resolver in resolvers:
            OmegaConf.register_resolver(resolver[0], resolver[1])

    def _settings_object(self, filepath: str):
        return OmegaConf.load(filepath)

    def load(self, path: str = "", files: List[str] = []) -> object:
        # TODO: Change logic with python3.8
        path: str = self.path if self.path else path
        files: List[str] = self.files if self.files else files

        # Load base settings
        flubber_settings: object = self._settings_object(self.flubber_settings)

        for sfile in files:
            tsettings: str = str(Path(path) / Path(sfile))
            flubber_settings = OmegaConf.merge(
                flubber_settings, self._settings_object(tsettings)
            )
        return flubber_settings
