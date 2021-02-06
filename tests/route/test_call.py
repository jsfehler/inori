from inori import Client

import pytest


@pytest.fixture()
def client():
    return Client('https://foo.com/v1/')


def test_callable_multiple_kwargs(client):
    client.add_route('bar/${barId}')

    with pytest.raises(ValueError) as e:
        client.bar(barId=10, wrong=100)

    assert str(e.value) == 'Expected one keyword argument, got multiple.'


def test_takes_no_kwargs(client):
    client.add_route('bar')

    with pytest.raises(ValueError) as e:
        client.bar(barId=10)

    expected = 'Route "https://foo.com/v1/bar" does not take arguments'
    assert str(e.value) == expected


def test_trailing_slash():
    """When trailing_slash is True, trailing slashes are preserved."""
    client = Client('https://foo.com/v1/')
    route = client.add_route('bar/', trailing_slash=True)

    assert route.url == 'https://foo.com/v1/bar/'


def test_no_trailing_slash():
    """By default, trailing slashes are removed."""
    client = Client('https://foo.com/v1/')
    route = client.add_route('bar/')

    assert route.url == 'https://foo.com/v1/bar'


def test_trailing_slash_added():
    """
    When trailing_slash is True
    And there is no trailing slash
    Then one is added.
    """
    client = Client('https://foo.com/v1/')
    route = client.add_route('bar', trailing_slash=True)
    assert route.url == 'https://foo.com/v1/bar/'
