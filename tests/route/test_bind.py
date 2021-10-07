import random
import time
from unittest import mock

from inori import Client

import pytest


@pytest.fixture()
def client():
    return Client('https://foo.com/v1/')


@mock.patch('requests.Session', mock.Mock())
def test_bind(client):
    route = client.add_route('foo')

    @route.bind('request')
    def dummy():
        # Get a relatively randomly string.
        return str(random.random()) + str(time.time())

    a = dummy()
    b = dummy()

    assert a == b

    route.get()

    c = dummy()

    assert a != c
