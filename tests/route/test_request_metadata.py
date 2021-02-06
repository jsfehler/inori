from unittest import mock

from inori import Client


@mock.patch('requests.Session', mock.Mock())
def test_build_endpoint_simple():
    client = Client('https://foo.com/v1/')
    route = client.add_route('bar')

    assert client.request_metadata == {}

    route.get()

    expected = {
        'http_method': 'GET',
        'route': route.url,
        'headers': {},
        'data': None,
        'params': None,
    }

    assert client.request_metadata == expected
