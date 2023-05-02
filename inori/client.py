import logging
import uuid
from typing import Any, Dict, List, Union

import requests

import shibari

from .logging import Logging
from .route import Route
from .utils.headerdict import HeaderDict
from .utils.sanitize import safe_illegal_character, safe_keyword


class Client:
    """Base for an API instance.

    Client takes a string to use as the base for the API.

    Route objects are built by calling Client.add_route() with
    a string template. Route objects then become attributes of the Client.

    Example:
        >>> client = Client('http://my.service/api/v777')
        >>> client.add_route('fruits/oranges')

        >>> result_1 = client.fruits.get()
        >>> result_2 = client.fruits.oranges.get()

    Routes can use any standard HTTP verb, or make a request directly:

    Example:
        >>> client = Client('http://my.service/api/v777')
        >>> client.add_route('fruits/oranges')

        >>> result = client.fruits.request('GET')

    Routes requiring attributes are declared using a template,
    then provided by calling the Route.

    Example:

        >>> client = Client('http://my.service/api/v777')
        >>> client.add_route('fruits')
        >>> client.add_route('fruits/${fruitId}')

        >>> response = client.fruits(fruitId='8').get()

    The string template doesn't need to be provided in pieces,
    every piece will be turned into an attribute:

    Example:

        >>> client = Client('http://my.service/api/v777')
        >>> client.add_route('fruits/${fruitId}')

        >>> response = client.fruits(fruitId='5').get()

    Python keywords get an underscore prefix.

    Example:

        >>> client = Client('http://my.service/api/v777')
        >>> client.add_route('import/${importId}')

        >>> response = client._import(importId='5').get()

    Arguments:
        base_uri: Base URI for the API.

    Attributes:
        headers: Dictionary containing all Client-level headers.

        request_kwargs: Dictionary of any arguments to send with every
            request. Applies to all registered Routes.

        logger: Unique logger instance for each Client instance.

    """

    rig = shibari.Rig('request')
    bind = rig.bind

    route_paths: List[str] = []

    def __init__(self, base_uri: str, auth=None):
        self.base_uri = base_uri
        self.auth = auth

        for route in self.route_paths:
            self.add_route(route)

        self.headers = HeaderDict()

        # Keyword args that will be sent on every request made by a Route.
        self.request_kwargs: Dict[str, Any] = {}

        self.logger = logging.getLogger(f'{__name__} {str(uuid.uuid4())}')
        self.logger.addHandler(logging.NullHandler())

        self.logging = Logging(self.logger)

        self.hooks = {
            "request": [
                self.logging.log_request,
            ],
            "response": [
                self.logging.log_response,
            ],
        }

    def new_session(self) -> requests.Session:
        """Get a new instance of requests.Session.

        Route objects will call this method during init.
        """
        return requests.Session()

    def add_route(self, path: str, trailing_slash: bool = False) -> Route:
        """Take a path string and create Route objects from it.

        Route objects are automatically set as attributes of
        the Client instance.

        Arguments:
            path: URI string.
            trailing_slash: Add a trailing slash to the Route URI.

        Returns:
            The last Route that was created.
        """
        # Remove empty strings from list of pieces.
        pieces = [i for i in path.split('/') if i != '']

        # Ensure first piece is safe to use as a python variable.
        route_name: str = safe_keyword(pieces[0])
        route_name = safe_illegal_character(route_name)

        # Check if a Route already exists.
        existing_route: Union[Route, None] = getattr(self, route_name, None)

        # Create new Route if none exists
        if not existing_route:
            r = Route(
                self,
                url=f'{self.base_uri}{pieces[0]}',
                trailing_slash=trailing_slash,
            )
            setattr(self, route_name, r)

        route: Route = getattr(self, route_name)

        # Remove first piece to get list of nested paths.
        nested_pieces = pieces[1:]

        # All the found routes.
        routes = [route]
        for item in nested_pieces:
            last_route = routes[-1]

            # Identify piece

            # Callable
            if item.startswith('${') and item.endswith('}'):
                kwarg = item[2:-1]

                # Check if callable already in the last Route.
                new_route = last_route.callables.get(kwarg)
                if not new_route:
                    new_route = Route(
                        self,
                        f"{last_route.url}/{item}",
                        trailing_slash,
                    )
                    last_route.callables[kwarg] = new_route

            # Children
            else:
                nested_route_name: str = safe_keyword(item)
                nested_route_name = safe_illegal_character(nested_route_name)

                # Check if route already exists
                new_route = getattr(last_route, nested_route_name, None)
                if not new_route:
                    new_route = Route(
                        self, f"{last_route.url}/{item}",
                    )
                    last_route.children[item] = new_route
                    setattr(last_route, nested_route_name, new_route)

            routes.append(new_route)

        return routes[-1]
