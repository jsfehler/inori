from unittest import mock

from inori import Client


def test_multiple_clients(client):
    """
    When I have multiple Client objects
    Then they should not share state.
    """
    client = Client('http://foo.bar/v1')
    client.headers['Accept'] = 'application/json'
    client.headers['Content-Type'] = 'application/json'

    another_client = Client('http://foo.bar/v1')

    assert 0 == len(another_client.headers.items())


@mock.patch('requests.Session', mock.Mock())
def test_function_headers(client):

    @client.headers("Accept")
    def complex_header(client, request_metadata):
        return "A complex value"

    route = client.add_route("bar")

    client.bar.get()

    expected = {
        'http_method': 'GET',
        'route': route.url,
        'headers': {'Accept': 'A complex value'},
        'data': None,
        'params': None,
    }

    assert client.metadata_recorder.request_metadata == expected
