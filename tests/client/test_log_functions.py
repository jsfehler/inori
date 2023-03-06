from inori import Route


def test_log_request(client):
    fake_url = Route(client, "1/2/3").url
    fake_headers = {"auth": "001"}
    fake_data = {"doit": "true"}
    fake_params = {"name": "Jack"}

    metadata = {
        'http_method': 'FAKE',
        'route': fake_url,
        'headers': fake_headers,
        'data': fake_data,
        'params': fake_params,
    }

    expected_result = (
        '\nFAKE request to 1/2/3'
        "\n Headers: {'auth': '001'}"
        "\n Body: {'doit': 'true'}"
        "\n Params: {'name': 'Jack'}"
    )

    result = client.logging.log_request(metadata)
    assert result == expected_result


def test_log_response(client):
    fake_url = Route(client, "1/2/3").url

    metadata = {
        'http_method': 'FAKE',
        'route': fake_url,
        'status_code': 666,
        'text': "Hello World",
    }

    expected_result = (
        '\nFAKE response from 1/2/3'
        '\n Status Code 666'
        '\n Body: Hello World'
    )

    result = client.logging.log_response(metadata)
    assert result == expected_result
