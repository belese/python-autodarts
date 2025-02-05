import aiohttp
import asyncio
import atexit
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
import time

import logging

logger = logging.getLogger(__name__)

class AutoDartException(Exception):
    pass

class AutoDartAuthenticationException(AutoDartException):
    """Exception raised for authentication errors in AutoDartSession."""
    pass

class AutoDartSession:
    """Represents a session for interacting with AutoDARTS services."""

    AUTODART_AUTH_URL: str = "https://login.autodarts.io/"
    
    def __init__(self, email: str, password: str, client_id: str, realm_name: str, client_secret_key: str,
                 server_url: str = AUTODART_AUTH_URL, *args, **kwargs) -> None:
        """
        Initialize an AutoDartSession instance.

        Parameters:
        - email (str): The email address for authentication.
        - password (str): The password for authentication.
        - client_id (str): The client ID for Keycloak.
        - realm_name (str): The realm name for Keycloak.
        - client_secret_key (str): The client secret key for Keycloak.
        - server_url (str): The URL of the Keycloak server.
        - args, kwargs: Additional parameters for ClientSession.

        Returns:
        None
        """
        self.email: str = email
        self.password: str = password
        self.keycloak_openid: KeycloakOpenID = KeycloakOpenID(
            server_url=server_url,
            client_id=client_id,
            realm_name=realm_name,
            client_secret_key=client_secret_key,
            #verify=False,
        )

        self.session: aiohttp.ClientSession = aiohttp.ClientSession(*args, **kwargs)
        self._token: dict = None
        self.next_refresh = 0
        # Register to close the session when the program ends (for atexit)
        atexit.register(self.session.close)

    def close(self):
        """Explicitly close the session."""
        if self.session:
            # Close the session explicitly when unloading or stopping
            asyncio.create_task(self.session.close())
            self.session = None  # Ensure the session is cleaned up

    async def refresh_token(self) :
        if time.time() < self.next_refresh  : 
            try:
                self._token = await asyncio.to_thread(self.keycloak_openid.refresh_token,self._token['refresh_token'])
            except KeycloakAuthenticationError as err:
                raise AutoDartAuthenticationException("Authentication failed") from err
        else :
            try:
                self._token = await asyncio.to_thread(self.keycloak_openid.token,self.email, self.password)
            except KeycloakAuthenticationError as err:
                raise AutoDartAuthenticationException("Authentication failed") from err
        self.next_refresh = time.time() + self._token["expires_in"]
    
    async def token(self) -> dict:
        """
        Get the authentication token.

        Returns:
        dict: The authentication token.

        Raises:
        AutoDartAuthenticationException: If authentication fails.
        """
        if time.time() - 10 > self.next_refresh  :
            await self.refresh_token() 
            
        return self._token["access_token"]
    
    async def is_authenticated(self) -> bool:
        """
        Check if the session is authenticated.

        Returns:
        bool: True if authenticated, False otherwise.
        """
        try:
            token: dict = await self.token()
        except KeycloakAuthenticationError:
            return False
        except KeycloakGetError:
            return False
        return token is not None
        
    async def headers(self) -> dict:
        """
        Get the headers for API requests.

        Returns:
        dict: The headers with the authentication token.
        """
        return {
            "Authorization": "Bearer " + await self.token(),
        }

    async def get(self, url: str, headers: dict = {}, *args, **kwargs) -> aiohttp.ClientResponse:
        """
        Perform a GET request.

        Parameters:
        - url (str): The URL for the GET request.
        - headers (dict): Additional headers.
        - args, kwargs: Additional parameters for session.get.

        Returns:
        aiohttp.ClientResponse: The response object.
        """
        headers.update(await self.headers())
        return await self.session.get(url, *args, headers=headers, **kwargs)
        
    async def post(self, url: str, headers: dict = {}, *args, **kwargs) -> aiohttp.ClientResponse:
        """
        Perform a POST request.

        Parameters:
        - url (str): The URL for the POST request.
        - headers (dict): Additional headers.
        - args, kwargs: Additional parameters for session.post.

        Returns:
        aiohttp.ClientResponse: The response object.
        """
        headers.update(await self.headers())
        return await self.session.post(url, *args, headers=headers, **kwargs)
    
    async def put(self, url: str, headers: dict = {}, *args, **kwargs) -> aiohttp.ClientResponse:
        """
        Perform a PUT request.

        Parameters:
        - url (str): The URL for the PUT request.
        - headers (dict): Additional headers.
        - args, kwargs: Additional parameters for session.put.

        Returns:
        aiohttp.ClientResponse: The response object.
        """
        headers.update(await self.headers())
        return await self.session.put(url, *args, headers=headers, **kwargs)
    
    async def delete(self, url: str, headers: dict = {}, *args, **kwargs) -> aiohttp.ClientResponse:
        """
        Perform a DELETE request.

        Parameters:
        - url (str): The URL for the DELETE request.
        - headers (dict): Additional headers.
        - args, kwargs: Additional parameters for session.delete.

        Returns:
        aiohttp.ClientResponse: The response object.
        """
        headers.update(await self.headers())
        return await self.session.delete(url, *args, headers=headers, **kwargs)
    
    async def patch(self, url: str, headers: dict = {}, *args, **kwargs) -> aiohttp.ClientResponse:
        """
        Perform a PATCH request.

        Parameters:
        - url (str): The URL for the PATCH request.
        - headers (dict): Additional headers.
        - args, kwargs: Additional parameters for session.patch.

        Returns:
        aiohttp.ClientResponse: The response object.
        """
        headers.update(await self.headers())
        return await self.session.patch(url, *args, headers=headers, **kwargs)
