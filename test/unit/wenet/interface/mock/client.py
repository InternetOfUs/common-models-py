from __future__ import absolute_import, annotations

from wenet.interface.client import ApikeyClient, Oauth2Client


class MockApikeyClient(ApikeyClient):

    def __init__(self):
        super().__init__("apikey")


class MockOauth2Client(Oauth2Client):

    def __init__(self):
        super().__init__("clientId", "clientSecret", "resourceId", None, token_endpoint_url="tokenEndpointUrl")
