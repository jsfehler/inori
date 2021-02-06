from inori import Client


def test_multiple_clients():
    """
    When I have multiple Client objects
    Then they should not share state.
    """
    client = Client('http://foo.bar/api/v1')
    client.headers['Accept'] = 'application/json'
    client.headers['Content-Type'] = 'application/json'

    another_client = Client('http://foo.bar/api/v1')

    assert 0 == len(another_client.headers.items())
