import requests


def test_new_session(client):
    """
    When I call Client.new_session
    Then the returned object is a requests.Session instance
    """
    result = client.new_session()
    assert isinstance(result, requests.Session)
