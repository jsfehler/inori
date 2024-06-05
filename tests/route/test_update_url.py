from inori import Route


def test_update_url(client):
    """
    Given a Route has children
    When Route._update_url is called
    Then the Route and it's children are updated
    And the children of the children are updated
    """
    route = Route(client, 'johnathan/${cId}/joseph/holly')
    child_route = Route(client, 'johnathan/${cId}/joseph/holly/jotaro')
    grandchild_route = Route(
        client, 'johnathan/${cId}/joseph/holly/jotaro/jolyne',
    )

    route.children = {'jotaro': child_route}
    child_route.children = {'jolyne': grandchild_route}

    route._update_url({'cId': '5'})

    assert route.url == 'johnathan/5/joseph/holly'
    assert child_route.url == 'johnathan/5/joseph/holly/jotaro'
    assert grandchild_route.url == 'johnathan/5/joseph/holly/jotaro/jolyne'
