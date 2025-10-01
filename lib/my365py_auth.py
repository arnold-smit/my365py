"""
my365py_auth.py

This module provides the class M365BearerToken.
The class M365BearerToken takes care of obtaining and refreshing the access bearer token needed to authenticate with the Microsoft Graph API.

More specifically this module uses the Microsoft Authentication Library (MSAL) for Python.
In order to use this library some prerequisites are needed:
1) An Azure AD tenant. If you have a Microsoft 365 subscription, you already have!
2) An 'app registration' in your tenant. This is the identity of your app. You can register an app in the Azure portal.
3) A client secret for your app. This is essentially the password for your app. You can create a client secret in the Azure portal.
4) Aditionally you need:
   * The tenant ID of your Azure AD tenant
   * The application (client) ID of your app registration
5) In order to restrict / allow what the app registration can do, you need to assign API permissions to the app registration.
   For this application the following permissions are needed (a first go - may change in the future):
   * Calendars.ReadWrite: Read and write calendars in all mailboxes
   * Directory.ReadWrite.All: Read and write directory data
   * Files.ReadWrite.All: Read and write files in all site collections
   * Tasks.ReadWrite.All: Read and write all users’ tasks and tasklists
   * User-Mail.ReadWrite.All: Read and write all secondary mail addresses for users
   * User.ReadWrite.All: Read and write all users' full profiles
   * User.Read: Sign in and read user profile

Example
-------
from lib.my365py_auth import M365BearerToken
m365_token = M365BearerToken()
...
token = m365_token.get()
"""

import asyncio
import json
import pickle
from datetime import datetime, timedelta
from msal import PublicClientApplication
from onepassword import Client
from pathlib import Path

from lib.my365py_logger import logger
from lib.my365py_config import CNF


async def query_1password() -> dict[str, str]:
    """
    Query 1Password to obtain the id's needed to talk to the M365 Graph API

    Returns
    -------
    dictionary containing:
        'tenant_id': id of the Microsoft 365 tennant aka directory aka account
        'application_id': id of the application aka client that is going to query the graph API - need to register under App registrations in the Azure management portal: https://portal.azure.com/#home
        'secret_client_id': id of the client secret created in the Azure management portal
        'secret_values': value of the client secret created in the Azure management portal

    Raises
    ------
    OSError
        if the environment variable OP_SERVICE_ACCOUNT_TOKEN is not set
    RuntimeError
        if authentication with 1password failed
    ValueError
        if there is a problem with the secret obtained from 1password (f.i. not valid JSON)
    """

    # get the token used to talk to 1password (from environment variable set via the gnome-keyring -> in .bashrc: export OP_SERVICE_ACCOUNT_TOKEN=$(secret-tool lookup 1pwd_service_account_token  ...))
    token = CNF["OP_SERVICE_ACCOUNT_TOKEN"]
    if token is None:
        msg = "ERROR: could not find environment variable OP_SERVICE_ACCOUNT_TOKEN"
        logger.error(msg)
        raise OSError(msg)

    # authenticate with 1password using the token
    client = await Client.authenticate(
        auth=token,
        integration_name=CNF["OP_SERVICE_ACCOUNT_NAME"],
        integration_version="v1.0.0",
    )
    if client is None:
        msg = "ERROR: could not authenticate with 1password"
        logger.error(msg)
        raise RuntimeError(msg)

    # use client to get the secret -> see: https://developer.1password.com/docs/sdks/load-secrets/
    value = await client.secrets.resolve(f"op://{CNF['OP_VAULT_NAME']}/{CNF['OP_SECRET_NAME']}/notesPlain")
    if value is None:
        msg = "ERROR: could not obtain secret from 1password"
        logger.error(msg)
        raise RuntimeError(msg)

    # convert to json + check all data is available and return as dictionary
    try:
        value_as_dict = json.loads(value)
    except ValueError:
        # catching here to do some logging ... but simply re-throwing the error
        logger.error(msg)
        raise

    return value_as_dict


def get_azure_ids() -> dict[str, str]:
    """
    Get the Azure IDs needed in order to get a bearer token to authenticate with the Miscrosoft Graph API.
    These IDs do not change so caching ids in the .cache folder in a pickle file.
    If not found, query 1password and store the credentials in the pickle file for next time.
    Otherwise simply read the pickle file in the .cache folder and return the credentials.

    Returns
    -------
    dictionary containing:
        'tenant_id': id of the Microsoft 365 tennant aka directory aka account
        'application_id': id of the application aka client that is going to query the graph API - need to register under App registrations in the Azure management portal: https://portal.azure.com/#home
        'secret_client_id': id of the client secret created in the Azure management portal
        'secret_values': value of the client secret created in the Azure management portal
        'user_object_id': id of the user object for smit-dean in Azure AD
    """
    file = Path(CNF["CRED_CACHE_FILENAME"])
    if file.exists():
        # read the pickle file and return the credentials
        with file.open("rb") as f:
            creds = pickle.load(f)
    else:
        creds = asyncio.run(query_1password())
        with file.open("wb") as f:
            pickle.dump(creds, f)
    return creds


class M365Auth:
    """A class to provide autentication information needed with the Microsoft Graph API."""

    def __init__(self) -> None:
        """
        Initialize the M365BearerToken class.
        First get the tenant_id, application_id, and client_secret (stored in 1password).
        Subsequently use these to authenticate with Azure and obtain a bearer token.
        """
        creds = get_azure_ids()
        self._client_id = creds["application_id"]
        self._user_object_id = creds["user_object_id"]
        self._authority = f"https://login.microsoftonline.com/consumers" # in order for personal accounts to work -> do not use tenant_id
        self._scopes = CNF["GRAPH_API_SCOPES"]
        self._auth_token: str = None
        self._token_expiry: datetime.now()
        self._app = PublicClientApplication( client_id=self._client_id, authority=self._authority, )
        self._refresh_token()
        logger.success("Initialized M365Auth")

    def _refresh_token(self) -> None:
        """
        Make sure self.token_data contains a valid bearer token. 
        """
        if (self._auth_token is None) or ((self._token_expiry - datetime.now()).total_seconds() < CNF["TOKEN_MIN_SEC_TO_EXP"]):
            # Step 1: Initiate the device flow
            flow = self._app.initiate_device_flow(scopes=self._scopes)
            if "user_code" not in flow:
               msg = "Failed to create device flow. Check app registration."
               raise OSError(msg)
            print(flow["message"])  # This shows instructions with code and URL
            print("Code expires in", flow["expires_in"], "seconds")
            # Step 2: Poll until user signs in or code expires
            result = self._app.acquire_token_by_device_flow(flow)
            # Step 3: Check result
            if "access_token" in result:
                self._auth_token = result["access_token"]
                self._token_expiry = datetime.now() + timedelta(seconds=result["expires_in"])
                print("Access token acquired!")
            else:
                msg = "Failed to acquire token"
                raise OSError(msg)

    def get_user_object_id(self) -> str:
        """
        Get the user object id of the user in Azure AD.

        Returns
        -------
        str
            The user object id of the user in Azure AD.
        """
        return self._user_object_id

    def get_auth_header(self) -> str:
        """
        Get a valid authentication header containing a valid bearer token.

        Returns
        -------
        dict
            A dictionary that can be past as an authentication header to requests.
        """
        self._refresh_token()
        return { "Authorization": f"Bearer {self._auth_token}",
                 "Content-Type": "application/json"
               }
