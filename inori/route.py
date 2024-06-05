import copy
from typing import Any, Dict, Mapping, Optional, TYPE_CHECKING, TypeVar, Union

import requests

import shibari

from .utils.headerdict import HeaderDict
from .utils.string_template import StringTemplate

if TYPE_CHECKING:
    from .client import Client


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

    def __init__(
        self, client: 'Client', url: str, trailing_slash: bool = False,
    ):
        self.client = client
        self.trailing_slash = trailing_slash

        _url = StringTemplate(url)
        if trailing_slash:
            _url = StringTemplate(f'{url}/')

        self.url: Union[str, StringTemplate] = _url

        self.headers = HeaderDict()

        self.callables: Dict[str, Route] = {}
        self.children: Dict[str, Route] = {}

        # Parameters from parent Route
        # ie: in /foo/${barId}/${bazId}, bazId stores barId's value
        # This gets overwritten if new values are given
        self.prev_kwargs: Mapping[str, str] = {}

        self.session = self.client.new_session()
        self.session.auth = self.client.auth

    def __repr__(self):  # NOQA
        return f"Route: <{str(self.url)}>"

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
        next_kwargs: Mapping[str, str] = {**self.prev_kwargs, **kwargs}

        # Always make a copy of the callable.
        # Else multiple calls to the same same Route will overwrite each other.
        copied_route = copy.deepcopy(next_route)
        # Update url with known arguments.
        copied_route.prev_kwargs = next_kwargs
        copied_route.url = copied_route.url.format(**next_kwargs)

        # Callable might have it's own callables.
        # Add info about used arguments
        for subcallable in copied_route.callables.values():
            subcallable.url = subcallable.url.format(**next_kwargs)

        # Children of this callable should know about the last arguments.
        for _, child_route in copied_route.children.items():
            copied_route._update_url(next_kwargs)

            for callable_route in child_route.callables.values():
                callable_route.url = callable_route.url.format(**next_kwargs)

        return copied_route

    def _update_url(self, new_kwargs: str) -> None:
        """Update this Route and it's children's urls with new values."""
        self.url = self.url.format(**new_kwargs)
        self.prev_kwargs = new_kwargs

        for _, child_route in self.children.items():
            child_route._update_url(new_kwargs)

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
                headers: Optional[Union[Dict[str, str], None]] = None,
                **kwargs: Any,
                ) -> requests.Response:
        """Send an HTTP Request.

        Accepts the same keyword arguments as requests.Session.request().

        Arguments:
            http_method: HTTP method to use for the request
        """
        self.client.rig.rigs['request'] = {}
        self.rig.rigs['request'] = {}

        local_headers = headers or {}

        request_metadata = {
            'http_method': http_method,
            'headers': local_headers,
            'route': self.url,
            'data': kwargs.get('data') or kwargs.get('json'),
            'params': kwargs.get('params'),
        }

        evaluated_headers: Dict[str, str] = {
            **self.client.headers.run_functions(self.client, request_metadata),
            **self.headers.run_functions(self, request_metadata),
            **local_headers,
        }

        request_metadata['headers'] = evaluated_headers

        for fn in self.client.hooks['request']:
            fn(request_metadata)

        evaluated_kwargs: Dict[str, Any] = {
            **kwargs,
            **self.client.request_kwargs,
        }

        response = self.session.request(
            http_method,
            self.url,
            headers=evaluated_headers,
            **evaluated_kwargs,
        )

        response_metadata = {
            'http_method': http_method,
            'route': self.url,
            'status_code': response.status_code,
            'text': response.text,
        }

        for fn in self.client.hooks['response']:
            fn(response_metadata)

        return response
