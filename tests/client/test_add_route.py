from inori import Client, Route


def test_returned_object(client):
    """
    When I add a new route
    Then the returned object is a Route object
    """
    client.add_route('bar')
    assert isinstance(client.bar, Route)


def test_route_url(client):
    """
    When I add a new route
    Then the returned Route object has the correct URL
    """
    route = client.add_route('bar')
    assert route.url == 'https://foo.com/v1/bar'


def test_route_already_exists(client):
    """
    Given a Route has been created
    When I make subsequent calls to Client.add_route
    Then a new Route object is not created
    """
    route = client.add_route('bar')
    same_route = client.add_route('bar')
    assert route is same_route


def test_callable_already_existing(client):
    """
    Given a Route has been created
    When I make subsequent calls to Client.add_route
    Then a new Route object is not created
    """
    route = client.add_route('bar/${barId}')
    same_route = client.add_route('bar/${barId}')
    assert route is same_route


def test_child_already_existing(client):
    """
    Given a Route has been created
    When I make subsequent calls to Client.add_route
    Then a new Route object is not created
    """
    route = client.add_route('bar/foo')
    same_route = client.add_route('bar/foo')
    assert route is same_route


def test_route_children(client):
    """
    Given a Route has been created
    And the route path has children
    Then the Route object has child Route objects.
    """
    route = client.add_route('bar/findByStatus')

    assert route.url == 'https://foo.com/v1/bar/findByStatus'
    assert isinstance(client.bar.findByStatus, Route)


def test_add_route_args_url(client):
    """
    Given a Route has been created
    And the route path has variables
    Then the Route object has the unformatted url
    """
    route = client.add_route('bar/${barId}')
    assert route.url == 'https://foo.com/v1/bar/${barId}'


def test_add_route_args_format(client):
    """
    Given a Route has been created
    And the route path has variables
    Then the Route object accepts arguments for those variables
    """
    client.add_route('bar/${barId}')
    assert isinstance(client.bar(barId=1), Route)


def test_args_children_url(client):
    """
    Given a Route has been created
    And the route path has variables
    And the route path has children
    Then the Route object has the unformatted url
    """
    route = client.add_route('bar/${barId}/uploadImage')
    assert route.url == 'https://foo.com/v1/bar/${barId}/uploadImage'


def test_args_children_format(client):
    """
    Given a Route has been created
    And the route path has variables
    And the route path has children
    Then the Route object accepts arguments for those variables
    """
    client.add_route('bar/${barId}/uploadImage')
    assert isinstance(client.bar(barId=1).uploadImage, Route)


def test_multiple_args(client):
    """
    Given a Route has been created
    And the route path has multiple variables
    Then the Route object accepts arguments for those variables
    """
    route = client.add_route('bar/${barId}/${bazId}')

    assert route.url == 'https://foo.com/v1/bar/${barId}/${bazId}'
    assert isinstance(client.bar(barId=1)(bazId=10), Route)


def test_args_reuse(client):
    client.add_route('bar/${barId}')

    a = client.bar(barId=1)
    b = client.bar(barId=2)

    assert a.url != b.url
    assert a.url == 'https://foo.com/v1/bar/1'
    assert b.url == 'https://foo.com/v1/bar/2'


def test_multiple_args_reuse(client):
    client.add_route('bar/${barId}/${bazId}')

    a = client.bar(barId=1)(bazId=10)
    b = client.bar(barId=2)(bazId=20)

    assert a.url != b.url
    assert a.url == 'https://foo.com/v1/bar/1/10'
    assert b.url == 'https://foo.com/v1/bar/2/20'


def test_chaining():
    client = Client('https://foo.com/v1/')
    client.add_route('bar/${potatoId}/biz/${tomatoId}')

    result = client.bar(potatoId=10).biz(tomatoId=55)
    assert result.url == 'https://foo.com/v1/bar/10/biz/55'


def test_long_chaining(client):
    client.add_route('bar/${barId}/${bazId}/${binId}')

    a = client.bar(barId=1)
    b = a(bazId=10)(binId=500)
    c = a(bazId=20)(binId=100)
    d = b

    assert a.url != b.url
    assert a.url != c.url
    assert b.url != c.url
    assert d.url == b.url

    assert a.url == 'https://foo.com/v1/bar/1'
    assert b.url == 'https://foo.com/v1/bar/1/10/500'
    assert c.url == 'https://foo.com/v1/bar/1/20/100'


def test_long_chaining_children(client):
    client.add_route('bar/${barId}/${bazId}/bin/${binId}/bao')

    route = client.bar(barId=10)(bazId=20).bin(binId=30).bao
    assert route.url == 'https://foo.com/v1/bar/10/20/bin/30/bao'
