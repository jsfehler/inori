from unittest import mock


@mock.patch('requests.Session', mock.Mock())
def test_function_headers(client):

    route = client.add_route("bar")

    @route.headers("Accept")
    def complex_header(client, request_metadata):
        return "A complex value"

    client.bar.get()

    expected = {
        'http_method': 'GET',
        'route': route.url,
        'headers': {'Accept': 'A complex value'},
        'data': None,
        'params': None,
    }

    assert client.metadata_recorder.request_metadata == expected
