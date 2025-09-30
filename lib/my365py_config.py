"""
my365py_config.py

This module defines a dictionary CNF that captures the settings for the application used throughout the application.

Example
-------
Import the CNF like this:
from lib.my365py_config import CNF
"""

import os

CNF = {
    "OP_SERVICE_ACCOUNT_TOKEN": os.getenv("OP_SERVICE_ACCOUNT_TOKEN"),
    "OP_SERVICE_ACCOUNT_NAME": "1pwd-sdk-access",
    "OP_VAULT_NAME": "apps-secrets",
    "OP_SECRET_NAME": "my365py-smit-dean",
    "CRED_CACHE_FILENAME": ".cache/azure_creds.pickle",
    "LOG_FILE": "log/my365py.log",
    "LOG_RETENTION": 7,
    "TOKEN_MIN_SEC_TO_EXP": 5,
    "LOG_LEVEL": "INFO",
    "GRAPH_API_SCOPES": [
        "Calendars.ReadWrite",
        "Directory.ReadWrite.All",
        "Files.ReadWrite.All",
        "Tasks.ReadWrite.All",
        "User-Mail.ReadWrite.All",
        "User.ReadWrite.All"
        "User.Read"
    ]
}

# TODO 1: since I am logging in as an application (not a user) I might need to use endpoints without the /me (only valid for federated logins)???
# TODO 2: this list needs to be changed with what will be implemented ... below is just for a first go
GRAPH_ENDPOINTS = {
    ## ONE DRIVE ENDPOINTS
    "ONEDRIVE_ROOT": "https://graph.microsoft.com/v1.0/me/drive/root",
    "ONEDRIVE_CHILDREN": "https://graph.microsoft.com/v1.0/me/drive/root/children",
    "ONEDRIVE_SEARCH": "https://graph.microsoft.com/v1.0/me/drive/root/search(q='{search-text}')",
    "ONEDRIVE_ITEMS": "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/children",
    "ONEDRIVE_UPLOAD": "https://graph.microsoft.com/v1.0/me/drive/items/{parent-id}:/{filename}:/content",
    "ONEDRIVE_DOWNLOAD": "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/content",
    "ONEDRIVE_DELETE": "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}",
    ## OUTLOOK ENDPOINTS
    "OUTLOOK_MESSAGES": "https://graph.microsoft.com/v1.0/me/messages",
    "OUTLOOK_CALENDAR": "https://graph.microsoft.com/v1.0/me/events",
    "OUTLOOK_CONTACTS": "https://graph.microsoft.com/v1.0/me/contacts",
    ## GENERAL ENDPOINTS
    "USER_INFO": "https://graph.microsoft.com/v1.0/me",
    "USER_PHOTO": "https://graph.microsoft.com/v1.0/me/photo/$value"
}
