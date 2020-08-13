from __future__ import absolute_import, annotations

from typing import Optional

import requests
import logging

logger = logging.getLogger("uhopper.service_api_interface.oauth_client")


class Oauth2Client:

    def __init__(self, management_url: str, client_id: str, client_secret: str):
        self.management_url = management_url
        self.token = None
        self.refresh_token = None
        self._client_id = client_id
        self._client_secret = client_secret

    def with_token(self, token) -> Oauth2Client:
        self.token = token
        return self

    def wit_refresh_token(self, refresh_token) -> Oauth2Client:
        self.refresh_token = refresh_token
        return self

    @staticmethod
    def initialize_with_code(management_url: str, client_id: str, client_secret: str, code: str, redirect_url: str) -> Oauth2Client:
        client = Oauth2Client(management_url, client_id, client_secret)
        client._initialize(code, redirect_url)
        return client

    @staticmethod
    def initialize_with_token(management_url: str, client_id: str, client_secret: str, token: str, refresh_token: str) -> Oauth2Client:
        client = Oauth2Client(management_url, client_id, client_secret)
        client\
            .with_token(token)\
            .wit_refresh_token(refresh_token)

        return client

    def _refresh_access_token(self) -> None:
        body = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        response = requests.post(self.management_url, json=body)
        if response.status_code == 200:
            body = response.json()
            self.refresh_token = body["refresh_token"]
            self.token = body["access_token"]
        else:
            raise Exception("Unable to refresh the token")

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
            self.refresh_token = body["refresh_token"]
            self.token = body["access_token"]
        else:
            raise Exception(f"Unable to retrieve the token, server respond with: {response} {response.json}")

    def _get_authentication_headers(self) -> dict:
        return {
            "authorization": f"bearer {self.token}"
        }

    def get(self, url: str, query_params: Optional[dict] = None, headers: Optional[dict] = None):

        if headers is not None:
            headers.update(self._get_authentication_headers())
        else:
            headers = self._get_authentication_headers()

        def get_request(retry: bool):
            response = requests.get(url, params=query_params, headers=headers)
            if response.status_code == 401:
                if retry:
                    self._refresh_access_token()
                    return get_request(False)
                else:
                    return response
            else:
                return response

        return get_request(True)

    def post(self, url: str, body: dict, headers: Optional[dict] = None):
        if headers is not None:
            headers.update(self._get_authentication_headers())
        else:
            headers = self._get_authentication_headers()

        def post_request(retry: bool):
            response = requests.post(url, json=body, headers=headers)
            if response.status_code == 401:
                if retry:
                    self._refresh_access_token()
                    return post_request(False)
                else:
                    return response
            else:
                return response

        return post_request(True)

    def put(self, url: str, body: dict, headers: Optional[dict] = None):
        if headers is not None:
            headers.update(self._get_authentication_headers())
        else:
            headers = self._get_authentication_headers()

        def post_request(retry: bool):
            response = requests.put(url, json=body, headers=headers)
            if response.status_code == 401:
                if retry:
                    self._refresh_access_token()
                    return post_request(False)
                else:
                    return response
            else:
                return response

        return post_request(True)

