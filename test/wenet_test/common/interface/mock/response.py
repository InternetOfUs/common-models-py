from __future__ import absolute_import, annotations

from typing import Union, Optional

from requests import Response


class MockResponse(Response):

    def __init__(self, response_content: Optional[Union[dict, list]]):
        super().__init__()
        self.response_content = response_content

    @property
    def text(self):
        return f"{self.response_content}"

    def json(self, **kwargs):
        return self.response_content
