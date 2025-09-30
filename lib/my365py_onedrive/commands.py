import click
import httpx
from lib.my365py_logger import logger


@click.command()
@click.option("--folder", prompt="Parent Folder", help="The name of the parent folder.")
@click.option("--name", prompt="New Folder", help="The name of the new folder.")
def create_folder(folder: str, name: str) -> list[dict]:
    """
    Creates a new folder in OneDrive.

    Parameters
    ----------
    folder : str
        The name of the parent folder.
    name : str
        The name of the new folder.

    Returns
    -------
    list[dict]
        A one item list with the dict representing the created folder object.
    """
    logger.success(f"Creating folder '{name}' in parent folder '{folder}'")
    return [{}]


@click.command()
@click.option("--query", prompt="Search query", help="The search query string.")
def find_files(query: str) -> list[dict]:
    """
    Finds files in OneDrive based on a query string.

    Parameters
    ----------
    query : str
        The search query string.

    Returns
    -------
    list[dict]
        A list of files matching the search query.
    """
    logger.success(f"Searching for files with query: {query}")
    return [{}]


@click.command()
@click.option("--src", prompt="List Local Paths", help="Comma-separated list of file paths to upload.")
@click.option("--dst", prompt="OneDrive Destination Folder", help="The destination OneDrive folder.")
def upload_files(src: list[str], dst: str) -> list[dict]:
    """
    Uploads multiple files to a specified OneDrive folder.

    Parameters
    ----------
    src : list[str]
        The paths of the files to upload.
    dst : str
        The destination OneDrive folder object id.

    Returns
    -------
    list[dict]
        A list of dicts representing the uploaded files.
    """
    logger.success(f"Uploading files to folder '{dst}'")
    return [{}]


@click.command()
@click.option("--src", prompt="Comma Separated List OneDrive File IDs", help="List of OneDrive File IDs to download.")
@click.option("--dst", prompt="Local Destination Path", help="The local path to save the downloaded files.")
def download_files(src: list[dict], dst: str) -> list[dict]:
    """
    Downloads multiple files from OneDrive.

    Parameters
    ----------
    src : list[int]
        The IDs of the files to download.
    dst : str
        The path to save the downloaded files.

    Returns
    -------
    list[dict]
        A list of dicts representing file objects that did not succeed in downloading, should be empty if all went well.
    """
    logger.success(f"Downloading files '{src}' to '{dst}'")
    return []


@click.command()
@click.option("--files", prompt="List File Paths", help="Comma-separated list of files to delete.")
def delete_files(files: list[dict]) -> list[dict]:
    """
    Deletes multiple files from OneDrive.

    Parameters
    ----------
    files : list[str]
        Comma-separated list of files to delete.

    Returns
    -------
    list[dict]
        A list of dicts representing the files that were not deleted, should be an empty list if all files were deleted successfully.
    """
    logger.success(f"Deleting files with paths: {files}")
    return []
