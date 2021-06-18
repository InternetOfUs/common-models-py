from __future__ import absolute_import, annotations

from wenet.common.interface.client import ApikeyClient, Oauth2Client


class MockApikeyClient(ApikeyClient):

    def __init__(self):
        super().__init__(None)


class MockOauth2Client(Oauth2Client):

    def __init__(self):
        super().__init__(None, None, None, None, None)
