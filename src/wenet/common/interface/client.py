from __future__ import absolute_import, annotations

from typing import Optional

import requests
import logging

from requests import Response

from wenet.common.interface.exceptions import RefreshTokenExpiredError
from wenet.common.storage.cache import RedisCache

logger = logging.getLogger("uhopper.oauth_client")


class Oauth2Client:

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

    def __init__(self, management_url: str, cache: RedisCache, resource_id: str, client_id: str, client_secret: str):
        self.management_url = management_url
        self._cache = cache
        self._resource_id = resource_id
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def _client_credential(self) -> Oauth2Client.ClientCredentials:
        raw_credentials = self._cache.get(self._resource_id)
        if raw_credentials is not None:
            return Oauth2Client.ClientCredentials.from_repr(raw_credentials)
        raise Exception(f"Credential for resource [{self._resource_id}] does not exist")

    @property
    def token(self) -> str:
        return self._client_credential.access_token

    @property
    def refresh_token(self) -> str:
        return self._client_credential.refresh_token

    @staticmethod
    def initialize_with_code(management_url: str, cache: RedisCache, resource_id: str, client_id: str, client_secret: str, code: str, redirect_url: str) -> Oauth2Client:
        client = Oauth2Client(management_url, cache, resource_id, client_id, client_secret)
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

        response = requests.post(self.management_url, json=body)
        logger.debug(f"Refresh token endpoint returned a code [{response.status_code}]")
        logger.debug(f"Refresh token endpoint returned: {response.text}")
        if response.status_code == 200:
            body = response.json()
            refresh_token = body["refresh_token"]
            token = body["access_token"]

            credentials = Oauth2Client.ClientCredentials(token, refresh_token)
            self._cache.cache(
                data=credentials.to_repr(),
                key=self._resource_id
            )
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

        response = requests.post(self.management_url, json=body)
        if response.status_code == 200:
            body = response.json()
            refresh_token = body["refresh_token"]
            token = body["access_token"]

            client_credentials = Oauth2Client.ClientCredentials(token, refresh_token)

            self._cache.cache(
                data=client_credentials.to_repr(),
                key=self._resource_id
            )
        else:
            raise Exception(f"Unable to retrieve the token, server respond with: {response} {response.json}")

    @staticmethod
    def get_authentication_headers(token: str) -> dict:
        return {
            "authorization": f"bearer {token}"
        }

    def get(self, url: str, query_params: Optional[dict] = None, headers: Optional[dict] = None) -> Response:

        if headers is None:
            headers = {}

        def get_request(client: Optional, retry: bool):
            logger.debug(f"Performing get request with token {client.token} {client.refresh_token}")
            headers.update(client.get_authentication_headers(client.token))
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

    def post(self, url: str, body: dict, headers: Optional[dict] = None) -> Response:
        if headers is None:
            headers = {}

        def post_request(client: Optional, retry: bool):
            headers.update(client.get_authentication_headers(client.token))
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

    def put(self, url: str, body: dict, headers: Optional[dict] = None) -> Response:
        if headers is None:
            headers = {}

        def put_request(client: Optional, retry: bool):
            headers.update(client.get(client.token))
            response = requests.put(url, json=body, headers=headers)
            if response.status_code == 401:
                if retry:
                    self.refresh_access_token()
                    return put_request(client, False)
                else:
                    return response
            else:
                return response

        return put_request(self, True)

