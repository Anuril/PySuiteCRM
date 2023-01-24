"""Config parser."""

import dataclasses
import json
import os
import pathlib
from typing import Optional, Protocol


class PySuiteCRMConfigException(Exception):
    """Custom PySuiteCRM exception."""

    pass


@dataclasses.dataclass
class PySuiteCRMConfig:
    """PySuiteCRM config object."""

    url: str
    client_id: str
    client_secret: str
    custom_modules: Optional[list[dict[str, str]]
                             ] = dataclasses.field(default_factory=list)


class ConfigParser(Protocol):
    """The config parser protocol."""

    parsed_config: PySuiteCRMConfig

    def parse_config(self):
        """Parse the config source."""
        ...


class ENVParser:
    """The ENV config parser."""

    def __init__(self) -> None:
        """Initialize the ENV config parser.

        Set the following environment variables.
            - PYSUITECRM_URL
            - PYSUITECRM_CLIENT_ID
            - PYSUITECRM_CLIENT_SECRET
        """
        self.parsed_config: Optional[PySuiteCRMConfig] = None

    def parse_config(self) -> None:
        """Parse the config to a PySuiteCRMConfig object."""
        if self.parsed_config:
            return
        url = os.environ.get('PYSUITECRM_URL')
        client_id = os.environ.get('PYSUITECRM_CLIENT_ID')
        client_secret = os.environ.get('PYSUITECRM_CLIENT_SECRET')
        if not url or not client_id or not client_secret:
            raise PySuiteCRMConfigException('Invalid ENV variables.')
        self.parsed_config = PySuiteCRMConfig(
            url=url, client_id=client_id, client_secret=client_secret)


class JSONParser:
    """The JSON config parser."""

    def __init__(self, config_file: str) -> None:
        """Initialize the JSON config parser.

        params:
            config_file (str) : The path to the JSON file containing the config

        returns:
            None
        """
        self._json_config: dict = self._load_file(pathlib.Path(config_file))
        self.parsed_config: Optional[PySuiteCRMConfig] = None

    def _load_file(self, config_file: pathlib.Path) -> dict:
        json_config = None
        with open(config_file, 'r') as infile:
            json_config = json.load(infile)
        if not json_config:
            raise PySuiteCRMConfigException('Could not load JSON file.')
        return json_config

    def parse_config(self) -> None:
        """Parse the config into a PySuiteCRMObject."""
        if self.parsed_config:
            return
        self.parsed_config = PySuiteCRMConfig(**self._json_config)
