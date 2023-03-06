from unittest import mock


@mock.patch('requests.Session', mock.Mock())
def test_build_endpoint_simple(client):
    route = client.add_route('bar')

    assert client.metadata_recorder.request_metadata == {}

    route.get()

    expected = {
        'http_method': 'GET',
        'route': route.url,
        'headers': {},
        'data': None,
        'params': None,
    }

    assert client.metadata_recorder.request_metadata == expected
