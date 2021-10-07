import copy
from typing import Any, Dict, TypeVar

import requests

import shibari

from .utils.string_template import StringTemplate


T = TypeVar('T', bound='Route')


class Route:
    """Representation of a single route in an API.

    Route objects should be created via Client.add_route().

    Example:
        >>> client = Client('http://foo.bar/v1')
        >>> fruits = client.add_route('fruits')

        >>> # The following are equivalent statements:
        >>> fruits.get()
        >>> client.fruits.get()

    Arguments:
        url: A string resembling a URI.
        trailing_slash: Add a trailing slash to the Route URI.

    Attributes:
        headers: Dictionary containing all the Route-level headers

    """

    rig = shibari.Rig('request')
    bind = rig.bind

    def __init__(self, client, url: str, trailing_slash: bool = False):
        self.client = client
        self.trailing_slash = trailing_slash

        _url = StringTemplate(url)
        if trailing_slash:
            _url = StringTemplate(f'{url}/')

        self.url: StringTemplate = _url

        self.headers: Dict[str, str] = {}

        self.callables: Dict[str, Route] = {}
        self.children: Dict[str, Route] = {}

        # Parameters from parent Route
        # ie: in /foo/${barId}/${bazId}, bazId stores barId's value
        # This gets overwritten if new values are given
        self.prev_kwargs: Dict[str, str] = {}

        self.session = requests.Session()

    def __deepcopy__(self, memodict):
        """Copy in such a way as to avoid copying the client object."""
        new = type(self)(self.client, str(self.url), self.trailing_slash)
        new.callables = copy.deepcopy(self.callables)
        new.children = copy.deepcopy(self.children)
        new.prev_kwargs = copy.deepcopy(self.prev_kwargs)

        for k, v in new.children.items():
            setattr(new, k, v)

        return new

    def __call__(self, **kwargs: str) -> T:  # NOQA C90
        """If a Route has callables, it can be called with one argument.

        This argument will be placed into the URL of the callable.

        Returns:
            Route: A Route object with the url formatted by the argument.
        """
        if len(kwargs) < 1:
            raise ValueError('Expected one keyword argument, got zero.')

        if len(kwargs) > 1:
            raise ValueError('Expected one keyword argument, got multiple.')

        # Argument has a Route associated with it
        k = list(kwargs.keys())[0]
        next_route = self.callables.get(k)

        if not next_route:
            raise ValueError(
                f'Route "{self.url}" does not take arguments',
            )

        # Ensure all known arguments are preserved.
        next_kwargs = {**self.prev_kwargs, **kwargs}

        copied_route = copy.deepcopy(next_route)
        copied_route.prev_kwargs = next_kwargs
        copied_route.url = copied_route.url.format(**next_kwargs)

        # Callable might have it's own callables.
        # Add info about used arguments
        for subcallable in copied_route.callables.values():
            subcallable.url = subcallable.url.format(**next_kwargs)

        # Children of this callable should know about the last arguments.
        for _, child_route in copied_route.children.items():
            child_route.url = child_route.url.format(**next_kwargs)
            child_route.prev_kwargs = next_kwargs

            for callable_route in child_route.callables.values():
                callable_route.url = callable_route.url.format(**next_kwargs)

        return copied_route

    def post(self, *args: Any, **kwargs: Any) -> requests.Response:
        """Send a POST request."""
        return self.request('POST', self, *args, **kwargs)

    def put(self, *args: Any, **kwargs: Any) -> requests.Response:
        """Send a PUT request."""
        return self.request('PUT', self, *args, **kwargs)

    def get(self, *args: Any, **kwargs: Any) -> requests.Response:
        """Send a GET request."""
        return self.request('GET', self, *args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> requests.Response:
        """Send a DELETE request."""
        return self.request('DELETE', self, *args, **kwargs)

    def request(self,
                http_method: str,
                *args: Any,
                **kwargs: Any,
                ) -> requests.Response:
        """Send an HTTP Request.

        Accepts the same keyword arguments as requests.Session.request().

        Arguments:
            http_method: HTTP method to use for the request
        """
        self.rig.rigs['request'] = {}

        local_headers = kwargs.get('headers') or {}

        headers = {
            **self.client.headers,
            **self.headers,
            **local_headers,
        }

        request_metadata = {
            'http_method': http_method,
            'route': self.url,
            'headers': headers,
            'data': kwargs.get('data') or kwargs.get('json'),
            'params': kwargs.get('params'),
        }

        self.client.log_request(request_metadata)

        response = self.session.request(
            http_method,
            self.url,
            headers=headers,
            **kwargs,
        )

        response_metadata = {
            'http_method': http_method,
            'route': self.url,
            'status_code': response.status_code,
            'text': response.text,
        }

        self.client.log_response(response_metadata)

        return response
