import click
import httpx
from loguru import logger


@click.command()
@click.option("--to", prompt="To addresses", help="Comma separated string of recipient email addresses.")
@click.option("--subject", prompt="Subject", help="The subject of the email.")
@click.option("--body", prompt="Body", help="The body of the email.")
@click.option("--cc", prompt="CC addresses", help="Comma separated string of CC email addresses.", default=None)
@click.option("--attachment", prompt="Attachment paths", help="Comma separated string of attachment file paths.", default=None)
def send_email(to: str, subject: str, body: str, cc: str = None, attachment: str = None) -> list[dict]:
    """
    Sends an email.

    Parameters
    ----------
    to : str
        Comma separated string of recipient email addresses.
    subject : str
        The subject of the email.
    body : str
        The body of the email.
    cc : str
        Comma separated string of CC email addresses.
    bcc : str
        Comma separated string of BCC email addresses.
    attachments : str
        Comma separated string of attachment file paths.

    Returns
    -------
    list[dict]
        A one item list where the item is the dict representing the email item.
    """
    return []


@click.command()
@click.option("--query", prompt="Query String", help="The query string used to search emails.")
def search_emails(query: str) -> list[dict]:
    """
    Searches for emails matching the query.

    Parameters
    ----------
    query : str
        The search query.

    Returns
    -------
    list[dict]
        A list of emails matching the query.
    """
    return []


@click.command()
@click.option("--emails", prompt="List of emails", help="list of emails.")
@click.option("--body", prompt="Body", help="The body of the reply.")
def reply_emails(emails: list[dict], body: str) -> list[dict]:
    """
    Replies to an (set of) email(s).

    Parameters
    ----------
    emails : list[dict]
        The list of emails to reply to.
    body : str
        The body of the reply.

    Returns
    -------
    list[dict]
        List of dict representing the replies.
    """
    return []


@click.command()
@click.option("--emails", prompt="List of emails", help="list of emails.")
@click.option("--to", prompt="To address", help="The email address of the recipient to forward the emails to.")
def forward_emails(emails: list[dict], to: str) -> list[dict]:
    """
    Forwards an (set of) email(s) to a specified recipient.

    Parameters
    ----------
    emails : list[dict]
        The list of emails to forward.
    to : str
        The email address of the recipient to forward the emails to.

    Returns
    -------
    list[dict]
        A list of the forward messages.
    """
    return []


@click.command()
@click.option("--emails", prompt="List of emails", help="list of emails.")
def save_emails(emails: list[dict]) -> list[dict]:
    """
    Saves a list of emails.

    Parameters
    ----------
    emails : list[dict]
        The list of emails to save.

    Returns
    -------
    list[dict]
        A list of dict containing the paths where the emails were saved.
    """
    return []


@click.command()
@click.option("--query", prompt="Query String", help="The query string used to search attachments.")
def search_attachments(query: str) -> list[dict]:
    """
    Searches for attachments matching the query.

    Parameters
    ----------
    query : str
        The search query.

    Returns
    -------
    list[dict]
        A list of attachments matching the query.
    """
    return []


@click.command()
@click.option("--attachments", prompt="List of attachments", help="list of attachments.")
@click.option("--dst", prompt="Path to save the attachment", help="The file path to save the attachment.")
def save_attachments(attachments: list[dict], dst: str) -> list[dict]:
    """
    Saves an attachment from an email.

    Parameters
    ----------
    attachments : list[dict]
        The list of attachments to save.
    dst : str
        The file path to save the attachment.

    Returns
    -------
    list[dict]
        List of dict containing the paths where the attachments were saved.
    """
    return []