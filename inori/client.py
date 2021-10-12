import logging
import uuid
from typing import Dict, Union

from .route import Route
from .utils.headerdict import HeaderDict
from .utils.safe_keyword import safe_keyword


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

        logger: Unique logger instance for each Client instance.

        request_metadata: Dictionary of relevant metadata from
            the last request.

        response_metadata: Dictionary of relevant metadata from
            the last response.

    """

    def __init__(self, base_uri: str):
        self.base_uri = base_uri

        self.headers: Dict[str, str] = {}

        self.headers = HeaderDict()

        self.logger = logging.getLogger(f'{__name__} {str(uuid.uuid4())}')
        self.logger.addHandler(logging.NullHandler())

        # Gets reset every request
        self.request_metadata: Dict[str, str] = {}
        self.response_metadata: Dict[str, str] = {}

        # Default logger messages
        self.logger_request_message = (
            '\n{http_method} request to {route}'
            '\n Headers: {headers}'
            '\n Body: {data}'
            '\n Params: {params}'
        )

        self.logger_response_message = (
            '\n{http_method} response from {route}'
            '\n Status Code {status_code}'
            '\n Body: {text}'
        )

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
        pieces[0] = safe_keyword(pieces[0])

        # Check if a Route already exists.
        existing_route: Union[Route, None] = getattr(self, pieces[0], None)

        # Create new Route if none exists
        if not existing_route:
            r = Route(
                self,
                url=f'{self.base_uri}{pieces[0]}',
                trailing_slash=trailing_slash,
            )
            setattr(self, pieces[0], r)

        route: Route = getattr(self, pieces[0])

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
                item = safe_keyword(item)
                new_route = getattr(last_route, item, None)
                if not new_route:
                    new_route = Route(self, f"{last_route.url}/{item}")
                    last_route.children[item] = new_route
                    setattr(last_route, item, new_route)

            routes.append(new_route)

        return routes[-1]

    def log_request(self, metadata: Dict[str, str]) -> str:
        """Log request info.

        Arguments:
            metadata: The content of the metadata will be formatted into
            self.logger_request_message.

        Returns: The formatted message.
        """
        self.request_metadata = metadata

        message = self.logger_request_message.format(**metadata)
        self.logger.info(message)
        return message

    def log_response(self, metadata: Dict[str, str]) -> str:
        """Log response info.

        Arguments:
            metadata: The content of the metadata will be formatted into
            self.logger_response_message.

        Returns: The formatted message.
        """
        self.response_metadata = metadata

        message = self.logger_response_message.format(**metadata)
        self.logger.info(message)
        return message
