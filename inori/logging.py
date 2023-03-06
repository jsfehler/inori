from typing import Dict


class Logging:
    """Convenience class to control logging hooks for the Client.

    request_message: String that will be formatted with
        request_metadata and sent to the logger when a request is made.

    response_message: String that will be formatted with
        response_metadata and sent to the logger after a request is made.
    """

    def __init__(self, logger):
        self.logger = logger

        # Default logger messages
        self.request_message = (
            '\n{http_method} request to {route}'
            '\n Headers: {headers}'
            '\n Body: {data}'
            '\n Params: {params}'
        )

        self.response_message = (
            '\n{http_method} response from {route}'
            '\n Status Code {status_code}'
            '\n Body: {text}'
        )

    def log_request(self, metadata: Dict[str, str]) -> str:
        """Log request info.

        Arguments:
            metadata: The content of the metadata will be formatted into
            self.request_message.

        Returns: The formatted message.
        """
        message = self.request_message.format(**metadata)
        self.logger.info(message)
        return message

    def log_response(self, metadata: Dict[str, str]) -> str:
        """Log response info.

        Arguments:
            metadata: The content of the metadata will be formatted into
            self.response_message.

        Returns: The formatted message.
        """
        message = self.response_message.format(**metadata)
        self.logger.info(message)
        return message
