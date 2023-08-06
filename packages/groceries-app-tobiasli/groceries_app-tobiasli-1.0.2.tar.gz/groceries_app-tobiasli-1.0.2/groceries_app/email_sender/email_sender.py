import typing as ty
import requests

from groceries_app.email_sender.config import EmailAccessBase


def send_email(config: EmailAccessBase, subject: str, recipients: ty.Sequence[str], text: str):
    """Send email_sender via mailgun service:"""
    return requests.post(
        config.api,
        auth=("api", config.token),
        data={"from": config.sender,
              "to": recipients,
              "subject": subject,
              "text": 'Your mail client does not support html.',
              "html": text})