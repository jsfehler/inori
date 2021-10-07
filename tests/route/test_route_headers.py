from unittest import mock

from inori import Client


import pytest


@pytest.fixture()
def client():
    return Client('https://foo.com/v1/')


@mock.patch('requests.Session', mock.Mock())
def test_function_headers(client):

    route = client.add_route("bar")

    @route.headers("Accept")
    def complex_header(client):
        return "A complex value"

    client.bar.get()

    expected = {
        'http_method': 'GET',
        'route': route.url,
        'headers': {'Accept': 'A complex value'},
        'data': None,
        'params': None,
    }

    assert client.request_metadata == expected
