import logging
import os
from typing import Dict, List, Optional, Union

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger(__name__)


GoogleCredentialsInfoDict = Dict[str, Union[str, List[str]]]


def get_google_auth_flow(scopes: list[str]) -> Optional[InstalledAppFlow]:
    """Initializes and returns an OAuth2 flow instance for Google authentication.

    This function reads the Google credentials file from the path specified by the environment variables
    `SECRETS_PATH` and `GOOGLE_CREDENTIALS_FILE`. It creates an `InstalledAppFlow` instance with the provided scopes.

    Args:
        scopes (list[str]): A list of Google API scopes that the application requires.

    Returns:
        Optional[InstalledAppFlow]: An instance of `InstalledAppFlow` if successful, otherwise `None`.

    Raises:
        KeyError Raised if the required environment variables are not set.
        FileNotFoundError Raised if the Google credentials file is not found.
    """
    try:
        google_credentials_path = os.path.join(os.environ["SECRETS_PATH"], os.environ["GOOGLE_CREDENTIALS_FILE"])
        return InstalledAppFlow.from_client_secrets_file(
            google_credentials_path, scopes, redirect_uri="urn:ietf:wg:oauth:2.0:oob"
        )
    except KeyError:
        logger.error(
            "You need to set the environment variable **SECRETS_PATH** and **GOOGLE_CREDENTIALS_FILE** to be able to get the Google credentials file."
        )
    except FileNotFoundError:
        logger.error(
            "The Google credentials file was not found in the path specified by the environment variable **GOOGLE_CREDENTIALS_FILE**."
        )
    return None


def get_google_credentials(
    google_auth_credentials_info: GoogleCredentialsInfoDict, scopes: list[str], refresh: bool = False
) -> Optional[Credentials]:
    """Retrieves Google OAuth2 credentials from the user context and optionally refreshes them.

    This function retrieves the credentials stored in the user context under the key `google_auth_credentials_json`.
    If the `refresh` parameter is `True`, it attempts to refresh the credentials if they are expired.

    Args:
        google_auth_credentials_info (GoogleCredentialsInfoDict): The information of the credentials stored in string in a dict (result of json.loads).
        scopes (list[str]): A list of Google API scopes that the application requires.
        refresh (bool, optional): If `True`, the credentials will be refreshed if they are expired. Defaults to False.

    Returns:
        Optional[Credentials]: An instance of `Credentials` if valid credentials are found and (if required) refreshed, otherwise `None`.

    Raises:
        RefreshError: Raised if the credentials are expired and cannot be refreshed.
    """
    try:
        creds = Credentials.from_authorized_user_info(google_auth_credentials_info, scopes)
        if refresh:
            creds.refresh(Request())
        return creds
    except RefreshError:
        return None
