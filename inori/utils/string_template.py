import string
from typing import Dict, Optional


class StringTemplate:
    """Create a string template to support partial string formatting.

    StringTemplate can compare to strings and other StringTemplate objects.

    Example:
        s = StringTemplate('${hello} ${world}')
        s.format(hello='Hello', world='World')
        'Hello World' == s
        >>> True
    """

    def __init__(self, template: str):
        self.template = string.Template(template)
        self.partial_substituted_str: str = ''

    def __eq__(self, other: object) -> bool:
        """Strings and StringTemplate can do an equality comparison."""
        return self.__repr__() == other

    def __repr__(self) -> str:
        """Return self.template.safe_substitute()."""
        return self.template.safe_substitute()

    def __str__(self) -> str:
        """Return self.template.safe_substitute()."""
        return self.__repr__()

    def format(self, mapping: Optional[Dict[str, str]]=None, **kwargs: str) -> str:  # NOQA A003
        """Format a string in such a way that a partial is allowed.

        Accepts the same arguments as string.Template.safe_substitute.

        Example:
            s = StringTemplate('${hello}' ${world}')
            s.format(world='World')
            s == '${hello} World'
            >>> True
        """
        mapping = mapping or {}

        self.partial_substituted_str = self.template.safe_substitute(
            mapping, **kwargs,
        )
        self.template = string.Template(self.partial_substituted_str)
        return self.__repr__()
