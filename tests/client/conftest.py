from inori import Client

import pytest


@pytest.fixture()
def client():
    return Client('https://foo.com/v1/')
