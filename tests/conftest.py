from typing import Dict

from inori import Client

import pytest


class MetadataRecorder:
    """This class controls recording hooks for the TestClient.

    request_metadata: Dictionary of relevant metadata from
        the last request.

    response_metadata: Dictionary of relevant metadata from
        the last response.
    """

    def __init__(self):
        # Gets reset every request
        self.request_metadata: Dict[str, str] = {}
        self.response_metadata: Dict[str, str] = {}

    def record_request_metadata(self, metadata):
        """Store metadata."""
        self.request_metadata = metadata

    def record_response_metadata(self, metadata):
        """Store metadata."""
        self.response_metadata = metadata


class TestClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.metadata_recorder = MetadataRecorder()

        self.hooks['request'].append(
            self.metadata_recorder.record_request_metadata,
        )

        self.hooks['response'].append(
            self.metadata_recorder.record_response_metadata,
        )


@pytest.fixture()
def client():
    return TestClient('https://foo.com/v1/')
