from __future__ import absolute_import, annotations

import logging
from abc import ABC, abstractmethod
from typing import Optional, Union

import requests
from requests import Response

from wenet.interface.exceptions import RefreshTokenExpiredError
from wenet.storage.cache import BaseCache


logger = logging.getLogger("wenet.interface.client")


class RestClient(ABC):

    @abstractmethod
    def get_authentication(self, *args) -> dict:
        pass

    @abstractmethod
    def post(self, url: str, body: Union[dict, list], headers: Optional[dict] = None) -> Response:
        pass

    @abstractmethod
    def get(self, url: str, query_params: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        pass

    @abstractmethod
    def put(self, url: str, body: Union[dict, list], headers: Optional[dict] = None) -> Response:
        pass

    @abstractmethod
    def delete(self, url: str, query_params: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        pass


class NoAuthenticationClient(RestClient):

    def get_authentication(self) -> dict:
        pass

    def post(self, url: str, body: Union[dict, list], headers: Optional[dict] = None) -> Response:
        return requests.post(url, json=body, headers=headers)

    def get(self, url: str, query_params: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        return requests.get(url, params=query_params, headers=headers)

    def put(self, url: str, body: Union[dict, list], headers: Optional[dict] = None) -> Response:
        return requests.put(url, json=body, headers=headers)

    def delete(self, url: str, query_params: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        return requests.delete(url, params=query_params, headers=headers)


class ApikeyClient(RestClient):

    def __init__(self, apikey: str, component_authorization_apikey_header: str = "x-wenet-component-apikey") -> None:
        """
        Create a new apikey client

        Args:
            apikey: the apikey to authenticate the requests
            component_authorization_apikey_header: the component authorization header for the apikey
        """
        self._apikey = apikey
        self._component_authorization_apikey_header = component_authorization_apikey_header

    def get_authentication(self) -> dict:
        return {
            self._component_authorization_apikey_header: self._apikey
        }

    def post(self, url: str, body: Union[dict, list], headers: Optional[dict] = None) -> Response:
        if headers is None:
            headers = {}

        headers.update(self.get_authentication())

        return requests.post(url, json=body, headers=headers)

    def get(self, url: str, query_params: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        if headers is None:
            headers = {}

        headers.update(self.get_authentication())

        return requests.get(url, params=query_params, headers=headers)

    def put(self, url: str, body: Union[dict, list], headers: Optional[dict] = None) -> Response:
        if headers is None:
            headers = {}

        headers.update(self.get_authentication())

        return requests.put(url, json=body, headers=headers)

    def delete(self, url: str, query_params: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        if headers is None:
            headers = {}

        headers.update(self.get_authentication())

        return requests.delete(url, params=query_params, headers=headers)


class Oauth2Client(RestClient):

    class ClientCredentials:

        def __init__(self, access_token: str, refresh_token: str):
            self.access_token = access_token
            self.refresh_token = refresh_token

        def to_repr(self) -> dict:
            return {
                "accessToken": self.access_token,
                "refreshToken": self.refresh_token
            }

        @staticmethod
        def from_repr(raw_data: dict) -> Oauth2Client.ClientCredentials:
            return Oauth2Client.ClientCredentials(raw_data["accessToken"], raw_data["refreshToken"])

    def __init__(self, client_id: str, client_secret: str, resource_id: str, cache: Optional[BaseCache] = None,
                 token_endpoint_url: str = "https://internetofus.u-hopper.com/prod/api/oauth2/token"):
        """
        Create a new oauth2 client

        Args:
            client_id: the identifier of the client
            client_secret: the client secret
            resource_id: the identifier of the resource
            cache: a cache to be used for storing client credentials, if not specified dedicated in memory cache is going to be used
            token_endpoint_url: the oauth2 token endpoint URL of the platform
        """
        self.token_endpoint_url = token_endpoint_url
        self._cache = cache
        self._resource_id = resource_id
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def _client_credential(self) -> Oauth2Client.ClientCredentials:
        raw_credentials = self._cache.get(self._resource_id)
        if raw_credentials is not None:
            return Oauth2Client.ClientCredentials.from_repr(raw_credentials)
        raise Exception(f"Credentials for resource [{self._resource_id}] does not exist")

    @property
    def token(self) -> str:
        return self._client_credential.access_token

    @property
    def refresh_token(self) -> str:
        return self._client_credential.refresh_token

    @staticmethod
    def initialize_with_code(client_id: str, client_secret: str, code: str, redirect_url: str, resource_id: str, cache: BaseCache,
                             token_endpoint_url: str = "https://internetofus.u-hopper.com/prod/api/oauth2/token") -> Oauth2Client:
        """
        Initialize a new oauth2 client with code

        Args:
            client_id: the identifier of the client
            client_secret: the client secret
            code: the oauth2 code of the client
            redirect_url: the redirect URL
            resource_id: the identifier of the resource
            cache: a cache
            token_endpoint_url: the oauth2 token endpoint URL of the platform

        Returns:
            an oauth2 client
        """
        client = Oauth2Client(client_id, client_secret, resource_id, cache, token_endpoint_url=token_endpoint_url)
        client._initialize(code, redirect_url)
        return client

    def refresh_access_token(self) -> None:
        logger.info(f"Refresh token for client [{self._client_id}]")
        body = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        response = requests.post(self.token_endpoint_url, json=body)
        logger.debug(f"Refresh token endpoint returned a code [{response.status_code}]")
        logger.debug(f"Refresh token endpoint returned: {response.text}")
        if response.status_code == 200:
            body = response.json()
            refresh_token = body["refresh_token"]
            token = body["access_token"]

            credentials = Oauth2Client.ClientCredentials(token, refresh_token)
            self._cache.cache(data=credentials.to_repr(), key=self._resource_id)
            logger.info(f"Refreshed oauth2 token for resource [{self._resource_id}]")
        else:
            logger.error(f"Unable to refresh the token for client ID [{self._client_id}]")
            raise RefreshTokenExpiredError("Unable to refresh the token")

    def _initialize(self, code: str, redirect_url: str):
        body = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_url,
            "code": code
        }

        response = requests.post(self.token_endpoint_url, json=body)
        if response.status_code == 200:
            body = response.json()
            refresh_token = body["refresh_token"]
            token = body["access_token"]

            client_credentials = Oauth2Client.ClientCredentials(token, refresh_token)

            self._cache.cache(data=client_credentials.to_repr(), key=self._resource_id)
        else:
            raise Exception(f"Unable to retrieve the token, server respond with: [{response.status_code}], [{response.text}]")

    @staticmethod
    def get_authentication(token: str) -> dict:
        return {
            "authorization": f"bearer {token}"
        }

    def post(self, url: str, body: Union[dict, list], headers: Optional[dict] = None) -> Response:
        if headers is None:
            headers = {}

        def post_request(client: Optional, retry: bool):
            logger.debug(f"Performing post request with token {client.token} {client.refresh_token}")
            headers.update(client.get_authentication(client.token))
            response = requests.post(url, json=body, headers=headers)
            if response.status_code in [400, 401, 403]:
                if retry:
                    client.refresh_access_token()
                    return post_request(client, False)
                else:
                    return response
            else:
                return response

        return post_request(self, True)

    def get(self, url: str, query_params: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        if headers is None:
            headers = {}

        def get_request(client: Optional, retry: bool):
            logger.debug(f"Performing get request with token {client.token} {client.refresh_token}")
            headers.update(client.get_authentication(client.token))
            response = requests.get(url, params=query_params, headers=headers)
            if response.status_code in [400, 401, 403]:
                if retry:
                    client.refresh_access_token()
                    return get_request(client, False)
                else:
                    return response
            else:
                return response

        return get_request(self, True)

    def put(self, url: str, body: Union[dict, list], headers: Optional[dict] = None) -> Response:
        if headers is None:
            headers = {}

        def put_request(client: Optional, retry: bool):
            logger.debug(f"Performing put request with token {client.token} {client.refresh_token}")
            headers.update(client.get(client.token))
            response = requests.put(url, json=body, headers=headers)
            if response.status_code in [400, 401, 403]:
                if retry:
                    self.refresh_access_token()
                    return put_request(client, False)
                else:
                    return response
            else:
                return response

        return put_request(self, True)

    def delete(self, url: str, query_params: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        if headers is None:
            headers = {}

        def delete_request(client: Optional, retry: bool):
            logger.debug(f"Performing delete request with token {client.token} {client.refresh_token}")
            headers.update(client.get_authentication(client.token))
            response = requests.delete(url, params=query_params, headers=headers)
            if response.status_code in [400, 401, 403]:
                if retry:
                    client.refresh_access_token()
                    return delete_request(client, False)
                else:
                    return response
            else:
                return response

        return delete_request(self, True)
