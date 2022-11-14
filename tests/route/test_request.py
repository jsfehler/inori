from dataclasses import dataclass
from unittest import mock

from inori import Client


@dataclass
class MockResponse:
    http_method: str
    url: str
    headers: dict
    status_code: str
    text: str


class MockSession:
    def __init__(self, *args, **kwargs):
        pass

    def request(self, http_method, url, headers, **kwargs):
        return MockResponse(
            http_method, url, headers, 200, f'Mock Response: kwargs={kwargs}',
        )


@mock.patch('requests.Session', MockSession)
def test_client_request_kwargs():
    """
    Given a client has request_kwargs defined
    When a request is made
    Then request_kwargs are used in the request
    """
    client = Client('https://foo.com/v1/')
    client.request_kwargs = {'verify': False}

    route = client.add_route('bar')

    result = route.get()
    assert result.text == f'Mock Response: kwargs={client.request_kwargs}'


@mock.patch('requests.Session', MockSession)
def test_request_client_headers():
    """
    When a request is made
    Then route headers are sent in the request.
    """
    client = Client('https://foo.com/v1/')
    client.headers['TestHeader'] = 'Client Header Test'

    route = client.add_route('bar')

    result = route.get()

    expected = {'TestHeader': 'Client Header Test'}

    assert result.headers == expected


@mock.patch('requests.Session', MockSession)
def test_request_route_headers():
    """
    When a request is made
    Then route headers are sent in the request.
    """
    client = Client('https://foo.com/v1/')
    route = client.add_route('bar')
    route.headers['TestHeader'] = 'Route Header Test'

    result = route.get()

    expected = {'TestHeader': 'Route Header Test'}

    assert result.headers == expected
