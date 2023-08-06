import os
import typing as ty

import tregex

from abc import abstractmethod, ABC


class EmailAccessBase(ABC):
    @property
    @abstractmethod
    def sender(self) -> str:
        """This property must contain the sender_email for mailgun."""

    @property
    @abstractmethod
    def recipients(self) -> ty.List[str]:
        """This property must contain the sender_email for mailgun."""

    @property
    @abstractmethod
    def token(self) -> str:
        """This property must contain the token for mailgun."""

    @property
    @abstractmethod
    def api(self) -> str:
        """This property must contain the api address for mailgun."""


class EmailAccessEnvironmentVariables(EmailAccessBase):
    """Email access information fetched from environment_variables."""
    def __init__(self, api_var: str, sender_email_var: str, token_var: str, recipients_var: str = '') -> None:
        self.api_var = self.check_env_var(api_var)
        self.token_var = self.check_env_var(token_var)
        self.sender_email_var = self.check_env_var(sender_email_var)
        self.recipients_var = self.check_env_var(recipients_var) if recipients_var else recipients_var

    @staticmethod
    def check_env_var(var: str) -> str:
        if var not in os.environ:
            raise EnvironmentError(f"Can't find environment variable {var}. "
                                   f"Closest match is {tregex.find_best(var, [var for var in os.environ])}.")
        return var

    @property
    def sender(self) -> str:
        return os.environ[self.sender_email_var]

    @property
    def recipients(self) -> ty.List[str]:
        """A comma separated list of email recipients."""
        if self.recipients_var:
            return [recipient.strip() for recipient in os.environ[self.recipients_var].split(',')]
        else:
            return ['']

    @property
    def token(self) -> str:
        return os.environ[self.token_var]

    @property
    def api(self) -> str:
        return os.environ[self.api_var]