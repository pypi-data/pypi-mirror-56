import os
from abc import abstractmethod

import tregex


class WunderpyAccessBase:
    @property
    @abstractmethod
    def client_id(self) -> str:
        """This property must contain the client_id for wunderlist."""
    @property
    @abstractmethod
    def access_token(self) -> str:
        """This property must contain the access_token for wunderlist."""

    @property
    @abstractmethod
    def default_list(self) -> str:
        """Default wunderlist list to send groceries."""


class WunderpyAccessEnvironmentVariables(WunderpyAccessBase):
    """Wunderpy access information fetched from environment_variables."""
    def __init__(self, client_id_var: str, access_token_var: str, default_list_var: str = '') -> None:
        self.access_token_var = self.check_env_var(access_token_var)
        self.client_id_var = self.check_env_var(client_id_var)
        self.default_list_var = self.check_env_var(default_list_var) if default_list_var else default_list_var

    @staticmethod
    def check_env_var(var: str) -> str:
        if var not in os.environ:
            raise EnvironmentError(f"Can't find environment variable {var}. "
                                   f"Closest match is {tregex.find_best(var, [var for var in os.environ])}.")
        return var

    @property
    def client_id(self) -> str:
        return os.environ[self.client_id_var]

    @property
    def access_token(self) -> str:
        return os.environ[self.access_token_var]

    @property
    def default_list(self) -> str:
        if self.default_list_var:
            return os.environ[self.default_list_var]
        else:
            return ''
